#!/usr/bin/env python3
"""
Entry processor - transforms raw XML entries into enhanced dictionary data
"""

import copy
from typing import List, Dict, Optional
from collections import defaultdict
from dataclasses import dataclass
from models import FolketsEntry


@dataclass
class EntryNode:
    """A node in the entry relationship graph"""
    entry: FolketsEntry
    base_form: Optional['EntryNode'] = None


class EntryProcessor:
    """Processes raw entries into enhanced dictionary data"""
    
    def process_entries(self, raw_entries: List[FolketsEntry]) -> Dict[str, List[EntryNode]]:
        """Transform raw XML entries into enhanced dictionary entries with object references"""
        print(f"Processing {len(raw_entries)} raw entries...")
        
        # Build entry nodes map - start with original entries
        entry_nodes_map = defaultdict(list)
        for raw_entry in raw_entries:
            # Normalize the entry before processing
            normalized_entry = copy.deepcopy(raw_entry)
            self._normalize_entry(normalized_entry)
            
            node = EntryNode(entry=normalized_entry)
            entry_nodes_map[normalized_entry.headword].append(node)
        
        # Single pass: create missing inflections and set base_form references
        generated_count = 0
        for headword, node_list in list(entry_nodes_map.items()):
            for node in node_list:
                if not node.entry.inflections:
                    continue
                
                for inflection in node.entry.inflections:
                    if inflection == node.entry.headword:
                        continue
                    
                    if inflection not in entry_nodes_map:
                        # Create new inflection entry node
                        inflection_node = self._create_inflection_node(inflection, node)
                        entry_nodes_map[inflection].append(inflection_node)
                        generated_count += 1
                    else:
                        # Set base_form for existing inflection nodes with matching or compatible word class
                        for inflection_node in entry_nodes_map[inflection]:
                            # Match if word classes are the same, or if inflection has empty/unknown class
                            word_class_match = (
                                inflection_node.entry.word_class == node.entry.word_class or
                                inflection_node.entry.word_class in ["", "unknown"]
                            )
                            if word_class_match and inflection_node.base_form is None:
                                inflection_node.base_form = node
                                # Add usage info
                                inflection_info = f"inflected form of \"{node.entry.headword}\""
                                if inflection_node.entry.usage:
                                    # Clean up before appending
                                    existing = inflection_node.entry.usage.strip().rstrip(';').strip()
                                    inflection_node.entry.usage = f"{existing}; {inflection_info}"
                                else:
                                    inflection_node.entry.usage = inflection_info
        
        total_entries = sum(len(nodes) for nodes in entry_nodes_map.values())
        print(f"Built {len(entry_nodes_map)} headwords with {total_entries} total entries (generated {generated_count} missing)")
        return dict(entry_nodes_map)
    
    def _normalize_entry(self, entry: FolketsEntry) -> None:
        """Normalize entry data - only handle missing word_class"""
        if not entry.word_class:
            entry.word_class = "unknown"
    
    def _create_inflection_node(self, inflection: str, base_node: EntryNode) -> EntryNode:
        """Create a new inflection entry node"""
        generated_entry = FolketsEntry(
            headword=inflection,
            word_class=base_node.entry.word_class,
            lang=base_node.entry.lang
        )
        
        generated_entry.usage = f"inflected form of \"{base_node.entry.headword}\""
        generated_entry.inflections = []  # Inflections don't have inflections
        
        # Create node with reference to base
        inflection_node = EntryNode(
            entry=generated_entry,
            base_form=base_node
        )
        
        return inflection_node
