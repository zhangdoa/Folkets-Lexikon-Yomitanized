#!/usr/bin/env python3
"""
Header section builder for Yomitan dictionary entries
Handles: headword <pos> formatting
"""

from typing import Dict
from models import FolketsEntry
from pos_mapper import POSMapper


class HeaderBuilder:
    """Builds header section with headword and POS tag"""
    
    def __init__(self, pos_mapper: POSMapper):
        self.pos_mapper = pos_mapper
    
    def build_header(self, entry: FolketsEntry) -> Dict:
        """Build header section: headword <pos>"""
        header_content = []
        
        # Headword
        header_content.append({
            "tag": "span",
            "content": [entry.headword],
            "style": {"fontWeight": "bold", "fontSize": "1.3em"}
        })
        
        # POS tag
        pos_tag = self.pos_mapper.detect_pos(entry)
        header_content.append({
            "tag": "span",
            "content": [f" ⟨{pos_tag}⟩"],
            "style": {
                "color": "DarkBlue",
                "fontSize": "1.0em",
                "fontWeight": "bold"
            }
        })
        
        return {
            "tag": "div",
            "content": header_content,
            "style": {"fontSize": "1.0em", "marginBottom": "0.5em"}
        }