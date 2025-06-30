#!/usr/bin/env python3
"""
Test script to demonstrate the staging functionality.
This script shows how the context and prompts are saved to staging files for review.
"""

import os
import sys
from pathlib import Path

# Add the modules directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from gemini_client import GeminiClient
from file_loader import DialogFlowFileLoader

def test_staging_functionality():
    """
    Test the staging functionality by loading some DialogFlow data and making a simple LLM call.
    """
    print("Testing DialogFlow Flow Analyzer Staging Functionality")
    print("=" * 60)
    
    # Create staging directory
    staging_dir = Path("test_staging")
    staging_dir.mkdir(exist_ok=True)
    
    # Initialize components with staging and .env support
    gemini_client = GeminiClient(
        api_key=os.getenv('GEMINI_API_KEY'),
        staging_dir=str(staging_dir),
        env_file=".env"  # Will look for .env file in current directory
    )
    
    # Load some DialogFlow data
    flow_path = Path("../Flow")  # Adjust path as needed
    file_loader = DialogFlowFileLoader()
    
    print(f"Loading DialogFlow data from: {flow_path}")
    
    # Load intents (just a few for testing)
    intents_path = flow_path / "intents"
    if intents_path.exists():
        intents_data = file_loader.load_intents(intents_path)
        print(f"Loaded {len(intents_data)} intents")
        
        # Take first intent for testing
        if intents_data:
            first_intent_name = list(intents_data.keys())[0]
            first_intent_data = intents_data[first_intent_name]
            
            # Create a simple test prompt
            test_prompt = """
            Analyze this DialogFlow intent and provide insights about:
            1. The intent's purpose and functionality
            2. Training phrase quality and coverage
            3. Parameter handling
            4. Potential improvements
            
            Provide a brief analysis in 2-3 paragraphs.
            """
            
            # Prepare context data
            context_data = f"""
            Intent Name: {first_intent_name}
            Intent Data: {first_intent_data}
            """
            
            print(f"\nTesting with intent: {first_intent_name}")
            print("Making LLM call with staging enabled...")
            
            try:
                # This will create staging files
                result = gemini_client.analyze_text(
                    prompt=test_prompt,
                    context=context_data,
                    request_id="test_intent_analysis"
                )
                
                print("\n" + "=" * 60)
                print("ANALYSIS COMPLETED!")
                print("=" * 60)
                print(f"Result: {result[:200]}...")
                
                print(f"\nStaging files created in: {staging_dir}")
                print("\nStaging files to review:")
                
                # List staging files
                for file_path in staging_dir.glob("*"):
                    if file_path.is_file():
                        print(f"  - {file_path.name}")
                
                print(f"\nCheck the staging directory to review:")
                print(f"  - Context data sent to Gemini")
                print(f"  - Prompts used for analysis")
                print(f"  - Gemini responses")
                print(f"  - Full conversation context")
                
            except Exception as e:
                print(f"Error during LLM call: {e}")
                print("This might be due to missing API key or network issues.")
                print("The staging files should still be created for review.")
        
    else:
        print(f"Intents directory not found at: {intents_path}")
        print("Please ensure the DialogFlow export is in the correct location.")

def show_staging_file_contents():
    """
    Show the contents of staging files for demonstration.
    """
    staging_dir = Path("test_staging")
    
    if not staging_dir.exists():
        print("No staging directory found. Run the test first.")
        return
    
    print("\n" + "=" * 60)
    print("STAGING FILE CONTENTS PREVIEW")
    print("=" * 60)
    
    for file_path in staging_dir.glob("staging_*.txt"):
        print(f"\n--- {file_path.name} ---")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Show first 500 characters
                print(content[:500] + "..." if len(content) > 500 else content)
        except Exception as e:
            print(f"Error reading file: {e}")

def test_env_file_functionality():
    """
    Test the .env file functionality.
    """
    print("\n" + "=" * 60)
    print("TESTING .ENV FILE FUNCTIONALITY")
    print("=" * 60)
    
    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        print(f"✓ .env file found: {env_file}")
        
        # Try to read the API key from .env
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key and api_key != "your_gemini_api_key_here":
                print("✓ API key loaded from .env file")
            else:
                print("⚠ API key in .env file appears to be placeholder")
        except ImportError:
            print("⚠ python-dotenv not installed. Install with: pip install python-dotenv")
        except Exception as e:
            print(f"✗ Error loading .env file: {e}")
    else:
        print("✗ .env file not found")
        print("  Create one by copying env_example.txt to .env and adding your API key")
    
    # Check for env_example.txt
    example_file = Path("env_example.txt")
    if example_file.exists():
        print(f"✓ Environment template found: {example_file}")
        print("  Copy this to .env and configure your API key")
    else:
        print("✗ Environment template not found")

if __name__ == "__main__":
    # Test .env functionality first
    test_env_file_functionality()
    
    # Check if API key is available
    if not os.getenv('GEMINI_API_KEY'):
        print("\nWARNING: GEMINI_API_KEY environment variable not set.")
        print("The LLM call will fail, but staging files will still be created.")
        print("Set your API key in one of these ways:")
        print("1. Environment variable: export GEMINI_API_KEY='your-api-key-here'")
        print("2. .env file: Copy env_example.txt to .env and add your API key")
        print("3. Command line: --api-key 'your-api-key-here'")
        print()
    
    # Run the test
    test_staging_functionality()
    
    # Show staging file contents
    show_staging_file_contents()
    
    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)
    print("Review the staging files to see exactly what was sent to Gemini!")
    print("\nFor .env file support, install python-dotenv:")
    print("pip install python-dotenv") 