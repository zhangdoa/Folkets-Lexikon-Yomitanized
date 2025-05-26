#!/usr/bin/env python3
"""
Yomitan format converter and dictionary generator
"""

import json
import zipfile
import os
from pathlib import Path
from typing import List, Dict, Any, Set
import shutil

from models import FolketsEntry
from pos_mapper import POSMapper
from content_builder import StructuredContentBuilder


class YomitanConverter:
    """Converts Folkets entries to Yomitan dictionary format"""
    
    def __init__(self):
        self.sequence_number = 1
        self.pos_mapper = POSMapper()
        self.content_builder = StructuredContentBuilder(self.pos_mapper)
        self.pos_tags: Set[str] = set()
    
    def convert_to_yomitan_entry(self, entry: FolketsEntry) -> List[List]:
        """Convert a parsed entry to Yomitan format"""
        headword = entry.headword
        pos_tag = self.pos_mapper.detect_pos(entry)
        self.pos_tags.add(pos_tag)
        
        # Build structured content for definitions
        definitions = []
        
        # Main definition using structured content
        definition_content = self.content_builder.build_structured_content(entry)
        definitions.append({
            "type": "structured-content",
            "content": definition_content
        })
        
        # Yomitan term format: [term, reading, tags, rules, score, definitions, sequence, term_tags]
        yomitan_entry = [
            headword,                    # term
            "",                         # reading (empty for Swedish)
            pos_tag,                    # tags (POS tag)
            "",                         # rules (empty)
            0,                          # score
            definitions,                # definitions array
            self.sequence_number,       # sequence number
            ""                          # term_tags (empty)
        ]
        
        self.sequence_number += 1
        return [yomitan_entry]
    
    def generate_tag_bank(self) -> List[List]:
        """Generate tag bank with POS and other tags"""
        tag_bank = []
        pos_descriptions = self.pos_mapper.get_pos_descriptions()
        
        for pos_tag in self.pos_tags:
            description = pos_descriptions.get(pos_tag, pos_tag)
            # Tag format: [name, category, order, notes, score]
            tag_bank.append([
                pos_tag,        # tag name
                'pos',          # category
                0,              # order
                description,    # notes/description
                0               # score
            ])
        
        return tag_bank
    
    def generate_index_json(self) -> Dict:
        """Generate index.json metadata"""
        from datetime import datetime
        
        return {
            "title": "Folkets Lexikon Yomitanized",
            "format": 3,
            "version": 1,
            "revision": datetime.now().strftime("%Y.%m.%d"),
            "sequenced": True,
            "author": "Community",
            "url": "https://github.com/zhangdoa/Folkets-Lexikon-Yomitanized",
            "description": "Swedish-English dictionary converted from Folkets Lexikon XML data. Original dictionary created by Folkets Lexikon team at KTH Royal Institute of Technology.",
            "attribution": "Original data: Folkets Lexikon (https://folkets-lexikon.csc.kth.se/)",
            "sourceLanguage": "sv",
            "targetLanguage": "en"
        }
    
    def write_dictionary_files(self, entries: List[FolketsEntry], output_dir: str):
        """Write all dictionary files"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Convert entries to Yomitan format
        all_term_entries = []
        for entry in entries:
            yomitan_entries = self.convert_to_yomitan_entry(entry)
            all_term_entries.extend(yomitan_entries)
        
        # Split into banks (max 10000 entries per file)
        bank_size = 10000
        for i in range(0, len(all_term_entries), bank_size):
            bank_number = (i // bank_size) + 1
            bank_entries = all_term_entries[i:i + bank_size]
            
            with open(f"{output_dir}/term_bank_{bank_number}.json", 'w', encoding='utf-8') as f:
                json.dump(bank_entries, f, ensure_ascii=False, separators=(',', ':'))
        
        # Write tag bank
        tag_bank = self.generate_tag_bank()
        with open(f"{output_dir}/tag_bank_1.json", 'w', encoding='utf-8') as f:
            json.dump(tag_bank, f, ensure_ascii=False, separators=(',', ':'))
        
        # Write index.json
        index_data = self.generate_index_json()
        with open(f"{output_dir}/index.json", 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)
    
    def create_zip_dictionary(self, output_dir: str, zip_path: str):
        """Create the final ZIP dictionary file"""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
            for file_path in Path(output_dir).rglob('*.json'):
                zipf.write(file_path, file_path.name)
    
    def convert_dictionary(self, entries: List[FolketsEntry], output_zip_path: str):
        """Main conversion function"""
        print(f"Converting {len(entries)} entries to Yomitan format...")
        
        # Create temporary directory for dictionary files
        temp_dir = "temp_dict_files"
        
        self.write_dictionary_files(entries, temp_dir)
        
        print(f"Creating ZIP dictionary: {output_zip_path}")
        self.create_zip_dictionary(temp_dir, output_zip_path)
        
        # Clean up temp files
        shutil.rmtree(temp_dir)
        
        print(f"Conversion complete! Dictionary saved as: {output_zip_path}")
        print(f"Found POS tags: {sorted(self.pos_tags)}")
        
        # Report unknown word classes if any
        self.pos_mapper.report_unknown_classes()