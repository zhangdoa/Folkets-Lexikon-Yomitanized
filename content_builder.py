#!/usr/bin/env python3
"""
Structured content builder for Yomitan dictionary entries
"""

from typing import List, Dict, Any
from models import FolketsEntry
from pos_mapper import POSMapper


class StructuredContentBuilder:
    """Builds structured content for Yomitan dictionary entries"""

    def __init__(self, pos_mapper: POSMapper):
        self.pos_mapper = pos_mapper

    def build_structured_content(self, entry: FolketsEntry) -> Dict:
        """Build structured content following Yomitan schema exactly"""
        content = {"tag": "div", "content": [], "style": {"marginLeft": "1.0em"}}

        # Header with headword and POS
        self._add_header(content, entry)

        # All other information in simple format
        self._add_additional_info(content, entry)

        # Main translations
        self._add_translations(content, entry)

        return content

    def _add_header(self, content: Dict, entry: FolketsEntry):
        """Add header with headword and POS tag"""
        header_content = []

        # Headword
        header_content.append(
            {
                "tag": "span",
                "content": [entry.headword],
                "style": {"fontWeight": "bold", "fontSize": "1.3em"},
            }
        )

        # POS tag
        pos_tag = self.pos_mapper.detect_pos(entry)
        header_content.append(
            {
                "tag": "span",
                "content": [f" ⟨{pos_tag}⟩"],
                "style": {
                    "color": "DarkBlue",
                    "fontSize": "1.0em",
                    "fontWeight": "bold",
                },
            }
        )

        header_div = {
            "tag": "div",
            "content": header_content,
            "style": {"fontSize": "1.0em", "marginLeft": "-1.0em"},
        }
        content["content"].append(header_div)

    def _add_additional_info(self, content: Dict, entry: FolketsEntry):
        """Add all additional information in simple format"""
        info_parts = []

        # Phonetic
        if entry.phonetic:
            cleaned_phonetic = self._normalize_phonetic(entry.phonetic)
            info_parts.append(f"[{cleaned_phonetic}]")

        # Grammar
        if entry.grammar:
            info_parts.append(f"Grammar: {self._clean_text(entry.grammar)}")

        # Inflections
        if entry.inflections:
            info_parts.append(f"Forms: {', '.join(entry.inflections)}")

        # Variants
        if entry.variants:
            variants_text = []
            for variant in entry.variants:
                variant_text = variant.value
                if variant.alt:
                    variant_text += f" ({variant.alt})"
                variants_text.append(variant_text)
            info_parts.append(f"Also: {', '.join(variants_text)}")

        # Usage
        if entry.usage:
            info_parts.append(f"Usage: {self._clean_text(entry.usage)}")

        # Add all info parts as simple divs
        for info in info_parts:
            info_div = {
                "tag": "div",
                "content": [
                    {
                        "tag": "span",
                        "content": [info],
                        "style": {
                            "fontSize": "0.9em",
                            "color": "#64748b",
                            "fontStyle": "italic",
                        },
                    }
                ],
                "style": {"marginBottom": "0.3em"},
            }
            content["content"].append(info_div)

    def _add_translations(self, content: Dict, entry: FolketsEntry):
        """Add main translations and definitions"""
        for i, translation in enumerate(entry.translations):
            trans_content = []

            # Definition number
            number = "① " if i == 0 else f"{chr(0x2460 + i)} "
            trans_content.append(
                {
                    "tag": "span",
                    "content": [number],
                    "style": {
                        "color": "DarkRed",
                        "fontWeight": "bold",
                        "marginLeft": "-1.0em",
                    },
                }
            )

            # Build translation text
            translation_parts = []

            # Swedish definition first if available
            if (
                i < len(entry.definitions)
                and entry.definitions[i]
                and entry.definitions[i].swedish
            ):
                translation_parts.append(self._clean_text(entry.definitions[i].swedish))

                # English definition
                if entry.definitions[i].english:
                    translation_parts.append(
                        f" / {self._clean_text(entry.definitions[i].english)}"
                    )

            # Main English translation
            translation_parts.append(f" → {self._clean_text(translation)}")

            # Combine all translation parts
            full_translation = "".join(translation_parts)

            trans_content.append(
                {
                    "tag": "span",
                    "content": [full_translation],
                    "style": {"fontSize": "1.0em"},
                }
            )

            trans_div = {
                "tag": "div",
                "content": trans_content,
                "style": {"fontSize": "1.0em", "marginBottom": "0.5em"},
            }
            content["content"].append(trans_div)

        # Add examples after all translations (only once per entry)
        if entry.examples:
            seen_examples = set()
            example_count = 0
            max_examples = 5  # Show more examples since they're not per translation

            for example in entry.examples:
                example_text = self._clean_text(example.swedish)
                if (
                    example_text
                    and example_text not in seen_examples
                    and example_count < max_examples
                ):
                    seen_examples.add(example_text)
                    example_count += 1

                    example_content = [
                        {
                            "tag": "span",
                            "content": [f"Ex: 「{example_text}」"],
                            "style": {"color": "darkgreen", "fontSize": "0.9em"},
                        }
                    ]

                    if example.english:
                        example_content.append(
                            {
                                "tag": "span",
                                "content": [f" {self._clean_text(example.english)}"],
                                "style": {
                                    "color": "LimeGreen",
                                    "fontSize": "0.9em",
                                    "fontStyle": "italic",
                                },
                            }
                        )

                    example_div = {
                        "tag": "div",
                        "content": example_content,
                        "style": {
                            "fontSize": "0.9em",
                            "marginBottom": "0.3em",
                            "marginLeft": "0.5em",
                        },
                    }
                    content["content"].append(example_div)

        # Add idioms after examples (only once per entry)
        if entry.idioms:
            seen_idioms = set()
            idiom_count = 0
            max_idioms = 3  # Show more idioms

            for idiom in entry.idioms:
                idiom_text = self._clean_text(idiom.swedish)
                if (
                    idiom_text
                    and idiom_text not in seen_idioms
                    and idiom_count < max_idioms
                ):
                    seen_idioms.add(idiom_text)
                    idiom_count += 1

                    idiom_content = [
                        {
                            "tag": "span",
                            "content": [f"Idiom: 「{idiom_text}」"],
                            "style": {"color": "darkorange", "fontSize": "0.9em"},
                        }
                    ]

                    if idiom.english:
                        idiom_content.append(
                            {
                                "tag": "span",
                                "content": [f" {self._clean_text(idiom.english)}"],
                                "style": {
                                    "color": "Orange",
                                    "fontSize": "0.9em",
                                    "fontStyle": "italic",
                                },
                            }
                        )

                    idiom_div = {
                        "tag": "div",
                        "content": idiom_content,
                        "style": {
                            "fontSize": "0.9em",
                            "marginBottom": "0.3em",
                            "marginLeft": "0.5em",
                        },
                    }
                    content["content"].append(idiom_div)

        # Add synonyms at the end
        if entry.synonyms:
            synonym_items = []
            for synonym in entry.synonyms:
                synonym_text = synonym.value
                if synonym.level:
                    synonym_text += f" ({synonym.level})"
                synonym_items.append(synonym_text)

            synonym_div = {
                "tag": "div",
                "content": [
                    {
                        "tag": "span",
                        "content": [f"Synonyms: {', '.join(synonym_items)}"],
                        "style": {"color": "#22c55e", "fontSize": "0.85em"},
                    }
                ],
                "style": {"marginTop": "0.5em"},
            }
            content["content"].append(synonym_div)

        # Add see also at the end (filter out meaningless references)
        if entry.see_also:
            see_items = []
            for see in entry.see_also:
                # Skip saldo references and animation files
                if (
                    see.type == "saldo"
                    or see.value.endswith(".swf")
                    or "||" in see.value
                ):  # Skip complex internal references
                    continue

                see_text = see.value
                if see.type and see.type not in ["saldo", "animation"]:
                    see_text += f" ({see.type})"
                see_items.append(see_text)

            if see_items:  # Only show if we have meaningful references
                see_div = {
                    "tag": "div",
                    "content": [
                        {
                            "tag": "span",
                            "content": [f"See also: {', '.join(see_items)}"],
                            "style": {
                                "color": "#64748b",
                                "fontSize": "0.8em",
                                "fontStyle": "italic",
                            },
                        }
                    ],
                    "style": {"marginTop": "0.3em"},
                }
                content["content"].append(see_div)

    def _normalize_phonetic(self, phonetic: str) -> str:
        """Normalize phonetic transcription to standard IPA"""
        if not phonetic:
            return ""

        # Folkets Lexikon to IPA mappings based on character analysis
        ipa_mappings = {
            # Vowels
            "@": "ə",  # schwa (appears 2214 times)
            "A": "ɑ",  # open back unrounded (appears 3826 times)
            "E": "ɛ",  # open-mid front unrounded (appears 3853 times)
            "I": "ɪ",  # near-close near-front unrounded (appears 2855 times)
            "O": "ɔ",  # open-mid back rounded (appears 1483 times)
            "U": "ʊ",  # near-close near-back rounded (appears 1981 times)
            "Y": "y",  # close front rounded (appears 755 times)
            "Å": "ɔ̊",  # Swedish rounded back vowel (appears 1923 times)
            "Ä": "æ",  # near-open front unrounded (appears 1005 times)
            "Ö": "øː",  # Swedish rounded front vowel (appears 1189 times)
            "ä": "ɛ",  # similar to E but distinct (appears 926 times)
            "ö": "œ",  # Swedish unrounded front vowel (appears 1500 times)
            # Consonants
            "$": "ʃ",  # voiceless postalveolar fricative (appears 1210 times)
            # Stress and length markers
            "²": "ˌ",  # secondary stress (appears 11839 times)
            ":": "ː",  # length marker (appears 30779 times)
            "+": "ʰ",  # aspiration (appears 2431 times)
            # Remove noise characters
            "2": "",  # secondary stress variant
            "?": "",  # uncertain pronunciation marker
            ";": "",  # separator
            "4": "",  # reference number
            "9": "",  # reference number
            "1": "",  # reference number
            ",": "",  # separator
            "el.": "",  # Swedish word for or
            "(": "",  # optional sound markers
            ")": "",  # optional sound markers
            " ": "",  # spaces within phonetic transcription
            ".": "",  # dots used for separation
            "-": "",  # hyphens
        }

        normalized = phonetic

        # Apply mappings in order (longer strings first to avoid partial matches)
        sorted_mappings = sorted(
            ipa_mappings.items(), key=lambda x: len(x[0]), reverse=True
        )
        for folkets, ipa in sorted_mappings:
            if folkets in normalized:
                normalized = normalized.replace(folkets, ipa)

        # Clean up any remaining whitespace and multiple colons
        normalized = normalized.strip()
        # Replace multiple length markers with single
        normalized = normalized.replace("ːː", "ː")

        return normalized

    def _clean_text(self, text: str) -> str:
        """Clean up text by handling HTML entities and formatting"""
        if not text:
            return ""

        # Handle common HTML entities
        text = text.replace("&quot;", '"')
        text = text.replace("&#39;", "'")  # Handle apostrophe
        text = text.replace("&apos;", "'")  # Alternative apostrophe entity
        text = text.replace("&amp;", "&")  # Must be last to avoid double conversion
        text = text.replace("&lt;", "<")
        text = text.replace("&gt;", ">")
        text = text.replace("&nbsp;", " ")

        # Handle numeric character references
        import re

        # Handle &#number; format
        text = re.sub(r"&#(\d+);", lambda m: chr(int(m.group(1))), text)
        # Handle &#xhex; format
        text = re.sub(r"&#x([0-9a-fA-F]+);", lambda m: chr(int(m.group(1), 16)), text)

        # Clean up extra whitespace
        text = " ".join(text.split())

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
