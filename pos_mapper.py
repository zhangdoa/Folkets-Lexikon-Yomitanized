#!/usr/bin/env python3
"""
POS mapper - handles word class to POS tag conversion
"""

from typing import Dict, Set
from models import FolketsEntry


class POSMapper:
    """Maps word classes to standardized POS tags"""
    
    def __init__(self):
        self.unknown_classes: Set[str] = set()
        self.pos_mapping = {
            # Full names
            'noun': 'noun',
            'verb': 'verb', 
            'adjective': 'adj',
            'adverb': 'adv',
            'preposition': 'prep',
            'pronoun': 'pron',
            'conjunction': 'conj',
            'interjection': 'interj',
            'numeral': 'num',
            'particle': 'part',
            'article': 'art',
            'prefix': 'prefix',
            'suffix': 'suffix',
            
            # Common abbreviations
            'nn': 'noun',        # noun
            'vb': 'verb',        # verb
            'jj': 'adj',         # adjective  
            'ab': 'adv',         # adverb
            'pp': 'prep',        # preposition
            'pn': 'pron',        # pronoun
            'kn': 'conj',        # conjunction
            'in': 'interj',      # interjection
            'sn': 'num',         # numeral
            'pm': 'part',        # particle
            'rg': 'num',         # cardinal number
            'ps': 'pron',        # possessive pronoun
            'ie': 'adv',         # adverb of location/time
            'hp': 'pron',        # interrogative pronoun
            
            # Special cases
            'abbrev': 'abbr',    # abbreviation
            'misc': 'misc',      # miscellaneous
        }
    
    def detect_pos(self, entry: FolketsEntry) -> str:
        """Detect POS tag from entry"""
        word_class = entry.word_class.lower().strip()
        
        # Handle known mappings
        if word_class in self.pos_mapping:
            return self.pos_mapping[word_class]
        
        # Handle 'unknown' specially - keep it as-is
        if word_class == 'unknown':
            return 'unknown'
        
        # Log truly unknown classes and return misc
        if word_class:  # Skip empty strings
            self.unknown_classes.add(word_class)
        
        return 'misc'
    
    def get_pos_descriptions(self) -> Dict[str, str]:
        """Get POS tag descriptions"""
        return {
            'noun': 'Noun',
            'verb': 'Verb',
            'adj': 'Adjective', 
            'adv': 'Adverb',
            'prep': 'Preposition',
            'pron': 'Pronoun',
            'conj': 'Conjunction',
            'interj': 'Interjection',
            'num': 'Numeral',
            'part': 'Particle',
            'art': 'Article',
            'prefix': 'Prefix',
            'suffix': 'Suffix',
            'abbr': 'Abbreviation',
            'unknown': 'Unknown',
            'misc': 'Other'
        }
    
    def report_unknown_classes(self) -> None:
        """Report unknown word classes (excluding our 'unknown' placeholder)"""
        if self.unknown_classes:
            print(f"Found {len(self.unknown_classes)} unknown word classes:")
            for cls in sorted(self.unknown_classes):
                print(f"  - '{cls}'")
        else:
            print("All word classes were recognized or handled.")