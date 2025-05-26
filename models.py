#!/usr/bin/env python3
"""
Data models for Folkets Lexikon entries
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class Example:
    """Example sentence with translation"""
    swedish: str
    english: str = ""


@dataclass
class Idiom:
    """Idiom with translation"""
    swedish: str
    english: str = ""


@dataclass
class Definition:
    """Definition with optional translation"""
    swedish: str
    english: str = ""


@dataclass
class Synonym:
    """Synonym with optional level"""
    value: str
    level: str = ""


@dataclass
class Variant:
    """Word variant with alternative form"""
    value: str
    alt: str = ""


@dataclass
class SeeAlso:
    """See also reference"""
    value: str
    type: str = ""


@dataclass
class FolketsEntry:
    """Complete Folkets Lexikon entry"""
    headword: str
    word_class: str = ""
    lang: str = "sv"
    translations: List[str] = field(default_factory=list)
    phonetic: Optional[str] = None
    sound_file: Optional[str] = None
    inflections: List[str] = field(default_factory=list)
    examples: List[Example] = field(default_factory=list)
    idioms: List[Idiom] = field(default_factory=list)
    definitions: List[Definition] = field(default_factory=list)
    usage: Optional[str] = None
    synonyms: List[Synonym] = field(default_factory=list)
    variants: List[Variant] = field(default_factory=list)
    see_also: List[SeeAlso] = field(default_factory=list)
    grammar: Optional[str] = None