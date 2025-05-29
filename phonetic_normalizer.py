#!/usr/bin/env python3
"""
Phonetic normalization utility
Converts Folkets Lexikon phonetic notation to standard IPA
"""


class PhoneticNormalizer:
    """Normalizes phonetic transcription to standard IPA"""
    
    def __init__(self):
        # Folkets Lexikon to IPA mappings
        self.ipa_mappings = {
            # Vowels
            "@": "ə",  # schwa
            "A": "ɑ",  # open back unrounded
            "E": "ɛ",  # open-mid front unrounded
            "I": "ɪ",  # near-close near-front unrounded
            "O": "ɔ",  # open-mid back rounded
            "U": "ʊ",  # near-close near-back rounded
            "Y": "y",  # close front rounded
            "Å": "ɔ̊",  # Swedish rounded back vowel
            "Ä": "æ",  # near-open front unrounded
            "Ö": "øː", # Swedish rounded front vowel
            "ä": "ɛ",  # similar to E but distinct
            "ö": "œ",  # Swedish unrounded front vowel
            # Consonants
            "$": "ʃ",  # voiceless postalveolar fricative
            # Stress and length markers
            "²": "ˌ",  # secondary stress
            ":": "ː",  # length marker
            "+": "ʰ",  # aspiration
            # Remove only actual noise characters, preserve dictionary markings
            "2": "",
            "?": "",
            "4": "",
            "9": "",
            "1": "",
            "el.": "",
        }
    
    def normalize(self, phonetic: str) -> str:
        """Normalize phonetic transcription to standard IPA"""
        if not phonetic:
            return ""
        
        normalized = phonetic
        
        # Apply mappings in order (longer strings first to avoid partial matches)
        sorted_mappings = sorted(
            self.ipa_mappings.items(), key=lambda x: len(x[0]), reverse=True
        )
        for folkets, ipa in sorted_mappings:
            if folkets in normalized:
                normalized = normalized.replace(folkets, ipa)
        
        # Clean up any remaining whitespace and multiple colons
        normalized = normalized.strip()
        normalized = normalized.replace("ːː", "ː")
        
        return normalized
