#!/usr/bin/env python3
"""
XML parser for Folkets Lexikon data
"""

import xml.etree.ElementTree as ET
from typing import List, Optional
from models import FolketsEntry, Example, Idiom, Definition, Synonym, Variant, SeeAlso


class FolketsXMLParser:
    """Parser for Folkets Lexikon XML format"""
    
    def parse_xml(self, xml_file_path: str) -> List[FolketsEntry]:
        """Parse Folkets Lexikon XML file and extract word entries"""
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        entries = []
        for word in root.findall('word'):
            entry = self.parse_word_entry(word)
            if entry:
                entries.append(entry)
                
        return entries
    
    def parse_word_entry(self, word_element) -> Optional[FolketsEntry]:
        """Parse a single word entry from XML"""
        # Basic info
        headword = word_element.get('value')
        word_class = word_element.get('class', '')  # e.g., 'rg', 'vb', 'nn', 'jj', 'ab'
        lang = word_element.get('lang', 'sv')
        
        if not headword:
            return None
            
        entry = FolketsEntry(
            headword=headword,
            word_class=word_class,
            lang=lang
        )
        
        # Parse child elements
        for child in word_element:
            if child.tag == 'translation':
                entry.translations.append(child.get('value', ''))
                
            elif child.tag == 'phonetic':
                entry.phonetic = child.get('value', '')
                # Also store sound file if available
                sound_file = child.get('soundFile')
                if sound_file:
                    entry.sound_file = sound_file
                    
            elif child.tag == 'paradigm':
                # Parse inflections
                for inflection in child.findall('inflection'):
                    infl_value = inflection.get('value')
                    if infl_value:
                        entry.inflections.append(infl_value)
                        
            elif child.tag == 'example':
                example = Example(
                    swedish=child.get('value', '')
                )
                # Look for translation child
                translation = child.find('translation')
                if translation is not None:
                    example.english = translation.get('value', '')
                entry.examples.append(example)
                
            elif child.tag == 'idiom':
                idiom = Idiom(
                    swedish=child.get('value', '')
                )
                # Look for translation child
                translation = child.find('translation')
                if translation is not None:
                    idiom.english = translation.get('value', '')
                entry.idioms.append(idiom)
                
            elif child.tag == 'definition':
                definition = Definition(
                    swedish=child.get('value', '')
                )
                # Look for translation child in definition
                translation = child.find('translation')
                if translation is not None:
                    definition.english = translation.get('value', '')
                entry.definitions.append(definition)
                
            elif child.tag == 'use':
                entry.usage = child.get('value', '')
                
            elif child.tag == 'synonym':
                synonym = Synonym(
                    value=child.get('value', ''),
                    level=child.get('level', '')
                )
                entry.synonyms.append(synonym)
                
            elif child.tag == 'variant':
                variant = Variant(
                    value=child.get('value', ''),
                    alt=child.get('alt', '')  # "also", etc.
                )
                entry.variants.append(variant)
                
            elif child.tag == 'see':
                see_also = SeeAlso(
                    value=child.get('value', ''),
                    type=child.get('type', '')  # "saldo", etc.
                )
                entry.see_also.append(see_also)
                
            elif child.tag == 'grammar':
                entry.grammar = child.get('value', '')
                
        return entry