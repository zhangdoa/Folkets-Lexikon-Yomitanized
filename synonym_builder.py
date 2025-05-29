#!/usr/bin/env python3
"""
Synonym section builder for Yomitan dictionary entries
Handles: synonyms formatting
"""

from typing import List, Dict, Optional
from models import FolketsEntry


class SynonymBuilder:
    """Builds synonym section"""
    
    def build_synonyms_section(self, entry: FolketsEntry) -> Optional[Dict]:
        """Build synonyms section"""
        if not entry.synonyms:
            return None
            
        synonym_items = []
        for synonym in entry.synonyms:
            synonym_text = synonym.value
            if synonym.level:
                synonym_text += f" ({synonym.level})"
            synonym_items.append(synonym_text)
        
        return {
            "tag": "div",
            "content": [f"Synonyms: {', '.join(synonym_items)}"],
            "style": {
                "color": "#22c55e",
                "fontSize": "0.9em",
                "marginTop": "0.5em",
                "marginBottom": "0.5em"
            }
        }
    
    def build_base_synonyms_section(self, synonyms: List, max_synonyms: int = 5) -> Optional[Dict]:
        """Build base form synonyms section"""
        if not synonyms:
            return None
            
        synonym_items = []
        for synonym in synonyms[:max_synonyms]:
            synonym_text = synonym.value
            if synonym.level:
                synonym_text += f" ({synonym.level})"
            synonym_items.append(synonym_text)
        
        if not synonym_items:
            return None
        
        return {
            "tag": "div",
            "content": [f"Base synonyms: {', '.join(synonym_items)}"],
            "style": {
                "color": "#16a34a",
                "fontSize": "0.85em",
                "marginTop": "0.3em"
            }
        }