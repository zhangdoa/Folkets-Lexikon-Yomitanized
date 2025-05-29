#!/usr/bin/env python3
"""
Usage section builder for Yomitan dictionary entries
Handles: phonetic, usage info, grammar, paradigm, variants
"""

from typing import List, Dict
from models import FolketsEntry
from text_cleaner import TextCleaner
from phonetic_normalizer import PhoneticNormalizer


class UsageBuilder:
    """Builds usage section with phonetic, usage, grammar info"""
    
    def __init__(self):
        self.text_cleaner = TextCleaner()
        self.phonetic_normalizer = PhoneticNormalizer()
    
    def build_pronunciation_section(self, entry: FolketsEntry) -> List[Dict]:
        """Build pronunciation section separately"""
        pronunciation_items = []
        
        # Phonetic
        if entry.phonetic:
            cleaned_phonetic = self.phonetic_normalizer.normalize(entry.phonetic)
            pronunciation_items.append(self._create_pronunciation_item(f"[{cleaned_phonetic}]"))
        
        return pronunciation_items
    
    def build_usage_section(self, entry: FolketsEntry) -> List[Dict]:
        """Build usage section with multiple lines (excluding pronunciation)"""
        usage_items = []
        
        # Usage info (split by semicolon, but not inside quotes)
        if entry.usage:
            usage_parts = self._smart_split_usage(entry.usage)
            for usage_part in usage_parts:
                if usage_part:
                    usage_items.append(self._create_usage_item(
                        self.text_cleaner.clean_text(usage_part)
                    ))
        
        # Grammar
        if entry.grammar:
            usage_items.append(self._create_usage_item(
                f"Grammar: {self.text_cleaner.clean_text(entry.grammar)}"
            ))
        
        # Paradigm (inflections)
        if entry.inflections:
            usage_items.append(self._create_usage_item(
                f"Paradigm: {', '.join(entry.inflections)}"
            ))
        
        # Variants
        if entry.variants:
            variants_text = []
            for variant in entry.variants:
                variant_text = variant.value
                if variant.alt:
                    variant_text += f" ({variant.alt})"
                variants_text.append(variant_text)
            usage_items.append(self._create_usage_item(
                f"Also: {', '.join(variants_text)}"
            ))
        
        return usage_items
    
    def _create_pronunciation_item(self, text: str) -> Dict:
        """Create a pronunciation item div"""
        return {
            "tag": "div",
            "content": [text],
            "style": {
                "fontSize": "1.0em",
                "color": "#2563eb",
                "fontWeight": "bold",
                "marginBottom": "0.3em"
            }
        }
    
    def _smart_split_usage(self, usage_text: str) -> List[str]:
        """Split usage text by semicolon + space, but not inside quotes. Removes leading/trailing semicolons and spaces from each part."""
        parts = []
        current_part = ""
        in_quotes = False
        i = 0
        
        while i < len(usage_text):
            char = usage_text[i]
            
            if char == '"':
                in_quotes = not in_quotes
                current_part += char
            elif char == ';' and not in_quotes:
                # Check if next character is a space
                if i + 1 < len(usage_text) and usage_text[i + 1] == ' ':
                    # Split on "; "
                    cleaned = current_part.strip().lstrip(';').strip()
                    if cleaned:
                        parts.append(cleaned)
                    current_part = ""
                    i += 1  # Skip the space after semicolon
                else:
                    # Keep the semicolon as part of the text
                    current_part += char
            else:
                current_part += char
            
            i += 1
        
        cleaned = current_part.strip().lstrip(';').strip()
        if cleaned:
            parts.append(cleaned)
        
        return parts
    
    def _create_usage_item(self, text: str) -> Dict:
        """Create a single usage item div"""
        return {
            "tag": "div",
            "content": [text],
            "style": {
                "fontSize": "0.9em",
                "color": "#64748b",
                "fontStyle": "italic",
                "marginBottom": "0.2em"
            }
        }
