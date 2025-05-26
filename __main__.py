#!/usr/bin/env python3
"""
Folkets Lexikon XML to Yomitan Dictionary Converter
Main entry point for the conversion process
"""

import os
import sys
from xml_parser import FolketsXMLParser
from yomitan_converter import YomitanConverter


def main():
    """Main conversion process"""
    # Default XML file path
    xml_file = "folkets_sv_en_public.xml"
    
    if not os.path.exists(xml_file):
        print(f"XML file not found: {xml_file}")
        print("Please ensure the XML file is in the current working directory.")
        return 1
    
    print(f"=== Creating Folkets Lexikon Dictionary ===")
    
    # Initialize components
    parser = FolketsXMLParser()
    converter = YomitanConverter()
    
    try:
        # Parse XML file
        print(f"Parsing XML file: {xml_file}")
        entries = parser.parse_xml(xml_file)
        print(f"Found {len(entries)} entries")
        
        # Convert to Yomitan format
        output_name = "Folkets_Lexikon.zip"
        converter.convert_dictionary(entries, output_name)
        
        print(f"\n=== Conversion Summary ===")
        print(f"Dictionary created: {output_name}")
        print("✅ Includes built-in structured styling - ready to import into Yomitan!")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())