#!/usr/bin/env python3
"""
Test script to demonstrate the consolidated file approach.
This script shows how all DialogFlow data is combined into a single file
and sent to Gemini without chunking to preserve context.
"""

import os
import sys
from pathlib import Path

# Add the modules directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from file_loader import DialogFlowFileLoader
from gemini_client import GeminiClient

def test_consolidated_approach():
    """
    Test the consolidated file approach by creating a consolidated file
    and making a simple LLM call with the complete data.
    """
    print("Testing DialogFlow Flow Analyzer - Consolidated Approach")
    print("=" * 70)
    
    # Create output directory
    output_dir = Path("test_consolidated")
    output_dir.mkdir(exist_ok=True)
    
    # Initialize components
    file_loader = DialogFlowFileLoader()
    gemini_client = GeminiClient(
        api_key=os.getenv('GEMINI_API_KEY'),
        staging_dir=str(output_dir / "staging"),
        env_file=".env"
    )
    
    # Load DialogFlow data
    flow_path = Path("../Flow")  # Adjust path as needed
    
    print(f"Loading DialogFlow data from: {flow_path}")
    
    if not flow_path.exists():
        print(f"❌ DialogFlow directory not found at: {flow_path}")
        print("Please ensure the DialogFlow export is in the correct location.")
        return
    
    try:
        # Create consolidated file
        print("\n📁 Creating consolidated file...")
        consolidated_file_path = file_loader.create_consolidated_file(flow_path, output_dir)
        print(f"✅ Consolidated file created: {consolidated_file_path}")
        
        # Load consolidated data
        print("\n📖 Loading consolidated data...")
        consolidated_data = file_loader.load_consolidated_data(consolidated_file_path)
        print(f"✅ Consolidated data loaded: {len(consolidated_data):,} characters")
        
        # Test with a simple analysis prompt
        test_prompt = """
        Analyze this consolidated DialogFlow data and provide insights about:
        1. The overall structure and organization
        2. Key intents and their purposes
        3. Flow patterns and user journeys
        4. Entity types and their usage
        5. Potential improvements or issues
        
        Provide a brief analysis in 3-4 paragraphs.
        """
        
        print("\n🤖 Making LLM call with consolidated data (no chunking)...")
        
        # This will create staging files with the complete data
        result = gemini_client.analyze_consolidated_data(
            prompt=test_prompt,
            consolidated_data=consolidated_data,
            request_id="consolidated_test"
        )
        
        print("\n" + "=" * 70)
        print("ANALYSIS COMPLETED!")
        print("=" * 70)
        print(f"Result preview: {result[:300]}...")
        
        print(f"\n📁 Files created in: {output_dir}")
        print("\n📋 Files to review:")
        
        # List all created files
        for file_path in output_dir.rglob("*"):
            if file_path.is_file():
                rel_path = file_path.relative_to(output_dir)
                print(f"  - {rel_path}")
        
        print(f"\n🔍 Check the staging directory to review:")
        print(f"  - Complete consolidated data sent to Gemini")
        print(f"  - No chunking - full context preserved")
        print(f"  - Prompts and responses for transparency")
        print(f"  - File size and processing information")
        
        # Show file size information
        file_size = Path(consolidated_file_path).stat().st_size
        print(f"\n📊 File Statistics:")
        print(f"  - Consolidated file size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        print(f"  - Character count: {len(consolidated_data):,}")
        print(f"  - No chunking required - sent as single request")
        
    except Exception as e:
        print(f"❌ Error during consolidated test: {e}")
        print("This might be due to missing API key or network issues.")
        print("The consolidated file should still be created for review.")

def show_consolidated_file_structure():
    """
    Show the structure of the consolidated file.
    """
    output_dir = Path("test_consolidated")
    consolidated_file = output_dir / "consolidated_dialogflow_data.txt"
    
    if not consolidated_file.exists():
        print("No consolidated file found. Run the test first.")
        return
    
    print("\n" + "=" * 70)
    print("CONSOLIDATED FILE STRUCTURE")
    print("=" * 70)
    
    try:
        with open(consolidated_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Show file structure
        sections = [
            "agent.json",
            "intents",
            "flows", 
            "entityTypes"
        ]
        
        for section in sections:
            if f"<{section} Begins>" in content:
                start = content.find(f"<{section} Begins>")
                end = content.find(f"<{section} Ends>")
                if end > start:
                    section_content = content[start:end+len(f"<{section} Ends>")]
                    print(f"\n--- {section.upper()} SECTION ---")
                    print(f"Length: {len(section_content):,} characters")
                    print(f"Preview: {section_content[:200]}...")
        
        print(f"\n📄 Total file size: {len(content):,} characters")
        print(f"📄 No chunking - complete context preserved")
        
    except Exception as e:
        print(f"Error reading consolidated file: {e}")

if __name__ == "__main__":
    # Check if API key is available
    if not os.getenv('GEMINI_API_KEY'):
        print("\n⚠️  WARNING: GEMINI_API_KEY environment variable not set.")
        print("The LLM call will fail, but the consolidated file will still be created.")
        print("Set your API key in one of these ways:")
        print("1. Environment variable: export GEMINI_API_KEY='your-api-key-here'")
        print("2. .env file: Copy env_example.txt to .env and add your API key")
        print("3. Command line: --api-key 'your-api-key-here'")
        print()
    
    # Run the test
    test_consolidated_approach()
    
    # Show file structure
    show_consolidated_file_structure()
    
    print("\n" + "=" * 70)
    print("CONSOLIDATED APPROACH BENEFITS")
    print("=" * 70)
    print("✅ No chunking - preserves complete context")
    print("✅ Better analysis quality with full data")
    print("✅ Simpler processing pipeline")
    print("✅ Full transparency through staging")
    print("✅ Easier debugging and review")
    print("✅ Maintains relationships between components")
    print("\n" + "=" * 70)
    print("TEST COMPLETED")
    print("=" * 70)
    print("Review the consolidated file to see the complete DialogFlow data!")
    print("Check staging files to see exactly what was sent to Gemini!") 