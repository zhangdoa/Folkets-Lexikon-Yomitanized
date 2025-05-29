#!/usr/bin/env python3
"""
Definition section builder for Yomitan dictionary entries
Handles: translations with their examples (already associated in XML)
"""

from typing import List, Dict
from models import FolketsEntry
from text_cleaner import TextCleaner


class DefinitionBuilder:
    """Builds definition section with translations and their examples"""
    
    def __init__(self):
        self.text_cleaner = TextCleaner()
    
    def build_definitions_section(self, entry: FolketsEntry) -> List[Dict]:
        """Build definitions section - each entry has one translation with its examples"""
        content_items = []
        
        if not entry.translations:
            return content_items
        
        # Handle multiple translations - combine them into one definition
        if len(entry.translations) > 1:
            # Multiple translations - create one combined definition
            combined_translation = ", ".join(entry.translations)
            content_items.append(self._create_definition_item(
                0, combined_translation, entry.definitions
            ))
        else:
            # Single translation
            content_items.append(self._create_definition_item(
                0, entry.translations[0], entry.definitions
            ))
        
        # Examples for this entry (directly associated) - deduplicated
        if entry.examples:
            seen_examples = set()
            for example in entry.examples:
                example_text = self.text_cleaner.clean_text(example.swedish)
                if example_text and example_text not in seen_examples:
                    seen_examples.add(example_text)
                    content_items.append(self._create_example_item(example))
        
        return content_items
    
    def build_idioms_section(self, entry: FolketsEntry) -> List[Dict]:
        """Build idioms section"""
        if not entry.idioms:
            return []
        
        return self._create_idioms_section(entry.idioms)
    
    def _create_definition_item(self, index: int, translation: str, definitions: List) -> Dict:
        """Create a single definition item with bullet point"""
        definition_parts = []
        
        # Swedish definition (if available)
        if index < len(definitions) and definitions[index] and definitions[index].swedish:
            definition_parts.append(self.text_cleaner.clean_text(definitions[index].swedish))
            
            # English definition  
            if definitions[index].english:
                definition_parts.append(
                    f" / {self.text_cleaner.clean_text(definitions[index].english)}"
                )
        
        # Main English translation
        definition_parts.append(f" → {self.text_cleaner.clean_text(translation)}")
        
        # Combine all definition parts
        full_definition = "".join(definition_parts)
        
        return {
            "tag": "div",
            "content": [full_definition],
            "style": {
                "fontSize": "1.0em",
                "marginBottom": "0.2em",
                "fontWeight": "bold"
            }
        }
    
    def _create_example_item(self, example) -> Dict:
        """Create a single example item (indented under definition)"""
        content_parts = [f"「{self.text_cleaner.clean_text(example.swedish)}」"]
        
        if example.english:
            content_parts.append(f" {self.text_cleaner.clean_text(example.english)}")
        
        return {
            "tag": "div",
            "content": ["".join(content_parts)],
            "style": {
                "color": "darkgreen",
                "fontSize": "0.9em",
                "marginBottom": "0.2em"
            }
        }
    
    def _create_idioms_section(self, idioms: List, max_idioms: int = 5) -> List[Dict]:
        """Create idioms section with header"""
        if not idioms:
            return []
            
        idiom_items = []
        seen_idioms = set()
        idiom_count = 0
        
        # Add section header
        idiom_items.append({
            "tag": "div",
            "content": ["Idioms:"],
            "style": {
                "color": "darkorange",
                "fontSize": "0.9em",
                "fontWeight": "bold",
                "marginTop": "0.3em",
                "marginBottom": "0.1em"
            }
        })
        
        for idiom in idioms:
            if idiom_count >= max_idioms:
                break
                
            idiom_text = self.text_cleaner.clean_text(idiom.swedish)
            if idiom_text and idiom_text not in seen_idioms:
                seen_idioms.add(idiom_text)
                idiom_count += 1
                
                content_parts = [f"「{idiom_text}」"]
                
                if idiom.english:
                    content_parts.append(f" {self.text_cleaner.clean_text(idiom.english)}")
                
                idiom_items.append({
                    "tag": "div",
                    "content": ["".join(content_parts)],
                    "style": {
                        "color": "darkorange",
                        "fontSize": "0.9em",
                        "marginBottom": "0.2em"
                    }
                })
        
        return idiom_items
