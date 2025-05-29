#!/usr/bin/env python3
"""
Yomitan format converter - simplified and focused on conversion logic
"""

import json
import zipfile
import os
from pathlib import Path
from typing import List, Dict, Set
import shutil
import concurrent.futures
import time

from models import FolketsEntry
from pos_mapper import POSMapper
from content_builder import StructuredContentBuilder
from entry_processor import EntryProcessor, EntryNode


class YomitanConverter:
    """Converts enhanced dictionary entries to Yomitan format"""
    
    def __init__(self):
        self.sequence_number = 1
        self.pos_mapper = POSMapper()
        self.content_builder = StructuredContentBuilder(self.pos_mapper)
        self.pos_tags: Set[str] = set()
        self.entry_processor = EntryProcessor()
    
    def convert_to_yomitan_entry(self, node: EntryNode) -> List[List]:
        """Convert an entry node to Yomitan format"""
        entry = node.entry
        headword = entry.headword
        pos_tag = self.pos_mapper.detect_pos(entry)
        self.pos_tags.add(pos_tag)
        
        # Build structured content
        definition_content = self.content_builder.build_structured_content(node)
        
        # Skip entries with no content
        if definition_content is None:
            return []
        
        definitions = [{
            "type": "structured-content",
            "content": definition_content
        }]
        
        # Yomitan term format
        yomitan_entry = [
            headword,
            "",  # reading (empty for Swedish)
            pos_tag,
            "",  # rules (empty for Swedish)
            0,   # score
            definitions,
            self.sequence_number,
            ""   # term_tags
        ]
        
        self.sequence_number += 1
        return [yomitan_entry]
    
    def generate_tag_bank(self) -> List[List]:
        """Generate tag bank with POS tags"""
        tag_bank = []
        pos_descriptions = self.pos_mapper.get_pos_descriptions()
        
        for pos_tag in self.pos_tags:
            description = pos_descriptions.get(pos_tag, pos_tag)
            tag_bank.append([pos_tag, 'pos', 0, description, 0])
        
        return tag_bank
    
    def generate_index_json(self) -> Dict:
        """Generate index.json metadata"""
        from datetime import datetime
        
        return {
            "title": "Folkets Lexikon Yomitanized",
            "format": 3,
            "version": 2,
            "revision": datetime.now().strftime("%Y.%m.%d"),
            "sequenced": True,
            "author": "Community",
            "url": "https://github.com/zhangdoa/Folkets-Lexikon-Yomitanized",
            "description": "Swedish-English dictionary converted from Folkets Lexikon XML data with enhanced inflection processing.",
            "attribution": "Original data: Folkets Lexikon (https://folkets-lexikon.csc.kth.se/)",
            "sourceLanguage": "sv",
            "targetLanguage": "en"
        }
    
    def write_dictionary_files(self, raw_entries: List[FolketsEntry], output_dir: str):
        """Write all dictionary files"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Stage 1: Process raw entries into enhanced dictionary data
        entry_nodes_map = self.entry_processor.process_entries(raw_entries)
        
        # Flatten for Yomitan conversion
        all_nodes = []
        for headword, node_list in entry_nodes_map.items():
            all_nodes.extend(node_list)
        
        # Stage 2: Convert to Yomitan format
        print("Converting to Yomitan format...")
        all_term_entries = []
        total = len(all_nodes)
        
        for i, node in enumerate(all_nodes):
            if i % 2000 == 0:
                progress = (i / total) * 100
                print(f"Conversion progress: {i}/{total} ({progress:.1f}%)")
            
            yomitan_entries = self.convert_to_yomitan_entry(node)
            all_term_entries.extend(yomitan_entries)
        
        print(f"Conversion complete: {len(all_term_entries)} Yomitan entries created")
        
        # Write files
        self._write_term_banks(all_term_entries, output_dir)
        self._write_tag_bank(output_dir)
        self._write_index_json(output_dir)
        
        print("All dictionary files written successfully")
    
    def _write_term_banks(self, all_term_entries: List, output_dir: str) -> None:
        """Write term bank files with parallel processing"""
        print("Writing term bank files...")
        bank_size = 10000
        total_banks = (len(all_term_entries) + bank_size - 1) // bank_size
        print(f"Preparing {total_banks} banks with {len(all_term_entries)} total entries...")
        
        start_time = time.time()
        completed_count = [0]
        
        def write_single_bank(bank_info):
            bank_number, start_idx = bank_info
            end_idx = min(start_idx + bank_size, len(all_term_entries))
            bank_entries = all_term_entries[start_idx:end_idx]
            filename = f"{output_dir}/term_bank_{bank_number}.json"
            
            file_start = time.time()
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(bank_entries, f, ensure_ascii=False, separators=(',', ':'))
            file_time = time.time() - file_start
            
            completed_count[0] += 1
            progress = (completed_count[0] / total_banks) * 100
            
            print(f"Completed term_bank_{bank_number}.json ({completed_count[0]}/{total_banks}) - {progress:.1f}% - {file_time:.2f}s")
            
            return bank_number
        
        bank_tasks = [(i + 1, i * bank_size) for i in range(total_banks)]
        
        print(f"Starting parallel write with {min(8, total_banks)} threads...")
        
        max_workers = min(8, total_banks)
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(write_single_bank, task) for task in bank_tasks]
            print(f"Submitted {len(futures)} write tasks...")
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    bank_number = future.result()
                except Exception as exc:
                    print(f'Bank write generated an exception: {exc}')
        
        total_time = time.time() - start_time
        print(f"Completed writing {total_banks} term bank files in {total_time:.2f}s")
    
    def _write_tag_bank(self, output_dir: str) -> None:
        """Write tag bank file"""
        print("Writing tag bank...")
        tag_bank = self.generate_tag_bank()
        with open(f"{output_dir}/tag_bank_1.json", 'w', encoding='utf-8') as f:
            json.dump(tag_bank, f, ensure_ascii=False, separators=(',', ':'))
    
    def _write_index_json(self, output_dir: str) -> None:
        """Write index.json file"""
        print("Writing index.json...")
        index_data = self.generate_index_json()
        with open(f"{output_dir}/index.json", 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)
    
    def create_zip_dictionary(self, output_dir: str, zip_path: str):
        """Create the final ZIP dictionary file"""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
            for file_path in Path(output_dir).rglob('*.json'):
                zipf.write(file_path, file_path.name)
    
    def convert_dictionary(self, raw_entries: List[FolketsEntry], output_zip_path: str):
        """Main conversion function"""
        print(f"Starting conversion of {len(raw_entries)} raw entries to Yomitan format...")
        
        temp_dir = "temp_dict_files"
        self.write_dictionary_files(raw_entries, temp_dir)
        
        print(f"Creating ZIP dictionary: {output_zip_path}")
        self.create_zip_dictionary(temp_dir, output_zip_path)
        
        # Clean up
        shutil.rmtree(temp_dir)
        
        print(f"Conversion complete! Dictionary saved as: {output_zip_path}")
        print(f"Found POS tags: {sorted(self.pos_tags)}")
        
        self.pos_mapper.report_unknown_classes()
