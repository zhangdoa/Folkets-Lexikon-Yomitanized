#!/usr/bin/env python3
"""
Part-of-speech mapper for Folkets Lexikon word classes
"""

from typing import Set, Tuple
from models import FolketsEntry


class POSMapper:
    """Maps Folkets Lexikon word classes to standard POS tags"""
    
    def __init__(self):
        self.unknown_classes: Set[Tuple[str, str]] = set()
        
        # Map Folkets Lexikon classes to POS tags
        self.class_to_pos = {
            'rg': 'adj',        # regular (often adjectives)
            'vb': 'verb',       # verb
            'nn': 'noun',       # noun  
            'jj': 'adj',        # adjective
            'ab': 'adv',        # adverb
            'av': 'adv',        # adverb
            'pp': 'prep',       # preposition
            'kn': 'conj',       # conjunction
            'in': 'interj',     # interjection
            'pn': 'pron',       # pronoun
            'rn': 'num',        # numeral
            'pl': 'part',       # particle
            'abbrev': 'abbrev', # abbreviation
            'article': 'art',   # article (den, en)
            'hp': 'pron',       # interrogative pronoun (vilket, vad)
            'ie': 'part',       # infinitive particle (att)
            'pm': 'noun',       # proper noun/name (places, people, organizations)
            'prefix': 'prefix', # prefix (anti-, bi-, etc.)
            'ps': 'pron',       # possessive pronoun (någons)
            'sn': 'conj',       # subordinating conjunction (utifall)
            'suffix': 'suffix', # suffix (-procentig, -tonnare, etc.)
        }
    
    def detect_pos(self, entry: FolketsEntry) -> str:
        """Detect part of speech from word class"""
        word_class = entry.word_class
        
        if word_class in self.class_to_pos:
            return self.class_to_pos[word_class]
        elif word_class:  # Non-empty class but not in our mapping
            print(f"⚠️  Unknown word class '{word_class}' for word '{entry.headword}' - please add to mapping!")
            self.unknown_classes.add((word_class, entry.headword))
            
        # Default to noun if no class or unknown class
        return 'noun'
    
    def get_pos_descriptions(self) -> dict:
        """Get descriptions for POS tags"""
        return {
            'noun': 'noun',
            'verb': 'verb', 
            'adj': 'adjective',
            'adv': 'adverb',
            'prep': 'preposition',
            'conj': 'conjunction',
            'interj': 'interjection',
            'pron': 'pronoun',
            'num': 'numeral',
            'part': 'particle',
            'abbrev': 'abbreviation',
            'art': 'article',
            'prefix': 'prefix',
            'suffix': 'suffix'
        }
    
    def report_unknown_classes(self):
        """Report any unknown word classes encountered"""
        if self.unknown_classes:
            print(f"\n⚠️  Found {len(self.unknown_classes)} unknown word classes:")
            for class_name, example_word in sorted(self.unknown_classes):
                print(f"   • '{class_name}' (example: {example_word})")
            print("Please add these to the class_to_pos mapping in pos_mapper.py")
        else:
            print("✅ All word classes recognized!")