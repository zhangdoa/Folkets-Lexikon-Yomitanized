#!/usr/bin/env python3
"""
Main structured content builder for Yomitan dictionary entries
Orchestrates all section builders
"""

from typing import Dict, Optional
from models import FolketsEntry
from pos_mapper import POSMapper
from header_builder import HeaderBuilder
from usage_builder import UsageBuilder
from definition_builder import DefinitionBuilder
from synonym_builder import SynonymBuilder
from base_form_builder import BaseFormBuilder
from entry_processor import EntryNode


class StructuredContentBuilder:
    """Main builder that orchestrates all section builders"""
    
    def __init__(self, pos_mapper: POSMapper):
        self.pos_mapper = pos_mapper
        self.header_builder = HeaderBuilder(pos_mapper)
        self.usage_builder = UsageBuilder()
        self.definition_builder = DefinitionBuilder()
        self.synonym_builder = SynonymBuilder()
        self.base_form_builder = BaseFormBuilder()
    
    def build_structured_content(self, node: EntryNode) -> Optional[Dict]:
        """Build complete structured content for an entry node"""
        entry = node.entry
        content = {"tag": "div", "content": []}
        
        # Skip entries that have no meaningful content
        if not entry.translations and not node.base_form:
            # Entry has no translations and no base form - skip it
            return None
        
        # 1. Header with word and part of speech
        header = self.header_builder.build_header(entry)
        content["content"].append(header)
        
        # 2. Part of speech - already included in header
        
        # 3. Pronunciation
        pronunciation_items = self.usage_builder.build_pronunciation_section(entry)
        content["content"].extend(pronunciation_items)
        
        # 4. Usage - phonetic, usage, grammar, etc.
        usage_items = self.usage_builder.build_usage_section(entry)
        content["content"].extend(usage_items)
        
        # 5. Own definitions section
        if entry.translations:
            definition_items = self.definition_builder.build_definitions_section(entry)
            content["content"].extend(definition_items)
        
        # 6. Base form definitions - if applicable
        if node.base_form:
            base_form_items = self.base_form_builder.build_base_form_section(node.base_form.entry)
            content["content"].extend(base_form_items)
        
        # 7. Idioms
        if entry.translations:  # Only show idioms if we have translations
            idiom_items = self.definition_builder.build_idioms_section(entry)
            content["content"].extend(idiom_items)
        
        # 8. Related vocabulary - synonyms
        if entry.translations:  # Only show synonyms if we have translations
            synonyms = self.synonym_builder.build_synonyms_section(entry)
            if synonyms:
                content["content"].append(synonyms)
        
        return content
