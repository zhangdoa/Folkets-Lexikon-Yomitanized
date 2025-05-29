#!/usr/bin/env python3
"""
Base form section builder for Yomitan dictionary entries
Handles: base form content display for inflected entries
"""

from typing import List, Dict, Optional
from models import FolketsEntry
from definition_builder import DefinitionBuilder
from synonym_builder import SynonymBuilder


class BaseFormBuilder:
    """Builds base form section for inflected entries"""
    
    def __init__(self):
        self.definition_builder = DefinitionBuilder()
        self.synonym_builder = SynonymBuilder()
    
    def build_base_form_section(self, base_entry: FolketsEntry) -> List[Dict]:
        """Build base form section with relevant content"""
        if not base_entry:
            return []
        
        content_items = []
        
        # Section separator
        content_items.append(self._create_separator(base_entry.headword))
        
        # Base form definitions (limited for relevance)
        if base_entry.translations:
            for i, translation in enumerate(base_entry.translations[:3]):
                content_items.append(self.definition_builder._create_definition_item(
                    i, translation, base_entry.definitions
                ))
        
        # Base form examples (limited and separate)
        if base_entry.examples:
            for example in base_entry.examples[:3]:  # Limit to 3 examples
                content_items.append(self.definition_builder._create_example_item(example))
        
        # Base form idioms (limited and separate)
        if base_entry.idioms:
            idiom_items = self.definition_builder.build_idioms_section(base_entry)
            content_items.extend(idiom_items)
        
        # Base form synonyms
        base_synonyms = self.synonym_builder.build_base_synonyms_section(base_entry.synonyms)
        if base_synonyms:
            content_items.append(base_synonyms)
        
        return content_items
    
    def _create_separator(self, headword: str) -> Dict:
        """Create visual separator for base form section"""
        return {
            "tag": "div",
            "content": [f"━━━ Base form: \"{headword}\" ━━━"],
            "style": {
                "fontSize": "1.0em",
                "color": "#059669",
                "fontWeight": "bold",
                "marginTop": "1.0em",
                "marginBottom": "0.5em",
                "textAlign": "center"
            }
        }
