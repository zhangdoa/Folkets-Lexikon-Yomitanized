#!/usr/bin/env python3
"""
Text cleaning utility for dictionary entries
Handles HTML entities and text formatting
"""

import re


class TextCleaner:
    """Utility for cleaning and formatting text content"""
    
    def clean_text(self, text: str) -> str:
        """Clean up text by handling HTML entities and formatting"""
        if not text:
            return ""
        
        # Handle common HTML entities
        # Handle compound entities first (like &amp;quot)
        text = text.replace("&amp;quot;", '"')
        text = text.replace("&amp;apos;", "'")
        text = text.replace("&amp;lt;", "<")
        text = text.replace("&amp;gt;", ">")
        text = text.replace("&amp;nbsp;", " ")
        
        # Handle malformed entities
        text = text.replace("&quot", '"')  # Missing semicolon
        text = text.replace("&apos", "'")  # Missing semicolon
        
        # Then handle simple entities
        text = text.replace("&quot;", '"')
        text = text.replace("&#39;", "'")
        text = text.replace("&apos;", "'")
        text = text.replace("&amp;", "&")
        text = text.replace("&lt;", "<")
        text = text.replace("&gt;", ">")
        text = text.replace("&nbsp;", " ")
        
        # Handle numeric character references
        text = re.sub(r"&#(\d+);", lambda m: chr(int(m.group(1))), text)
        text = re.sub(r"&#x([0-9a-fA-F]+);", lambda m: chr(int(m.group(1), 16)), text)
        
        # Clean up extra whitespace but preserve intentional structure
        text = " ".join(text.split())
        
        # Fix specific formatting issues
        # Handle quoted words that got split incorrectly
        text = re.sub(r'"\s*([^"]+)\s*"', r'"\1"', text)
        
        # Fix common punctuation issues
        text = text.replace(" ,", ",")
        text = text.replace(" .", ".")
        text = text.replace(" ;", ";")
        text = text.replace(" :", ":")
        text = text.replace(" !", "!")
        text = text.replace(" ?", "?")
        text = text.replace("( ", "(")
        text = text.replace(" )", ")")
        text = text.replace("[ ", "[")
        text = text.replace(" ]", "]")
        
        return text.strip()
