#!/usr/bin/env python3
"""
DialogFlow Flow Analyzer
A modular Python program to analyze DialogFlow flows using Gemini LLM.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add the modules directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from file_loader import DialogFlowFileLoader
from flow_analyzer import FlowAnalyzer
from gemini_client import GeminiClient
from utils import setup_logging, create_output_directories

class DialogFlowAnalyzer:
    """
    Main class for analyzing DialogFlow flows using Gemini LLM.
    """
    
    def __init__(self, flow_path: str, output_path: str = "output", api_key: Optional[str] = None, env_file: Optional[str] = None):
        """
        Initialize the DialogFlow analyzer.
        
        Args:
            flow_path: Path to the DialogFlow export directory
            output_path: Path for output files
            api_key: Gemini API key (if not provided, will look for environment variable)
            env_file: Path to .env file (default: looks for .env in current directory)
        """
        self.flow_path = Path(flow_path)
        self.output_path = Path(output_path)
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.env_file = env_file
        
        # Setup logging
        setup_logging(self.output_path / "logs")
        self.logger = logging.getLogger(__name__)
        
        # Create output directories
        create_output_directories(self.output_path)
        
        # Create staging directory for LLM context review
        self.staging_dir = self.output_path / "staging"
        self.staging_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Staging directory created: {self.staging_dir}")
        
        # Initialize components
        self.file_loader = DialogFlowFileLoader()
        self.gemini_client = GeminiClient(self.api_key, str(self.staging_dir), self.env_file)
        self.flow_analyzer = FlowAnalyzer(self.gemini_client)
        
        # Store loaded data
        self.intents_data = {}
        self.flows_data = {}
        self.entity_types_data = {}
        self.agent_data = {}
        
    def load_dialogflow_data(self) -> str:
        """
        Load all DialogFlow data and create a consolidated file.
        
        Returns:
            Path to the consolidated file
        """
        self.logger.info("Loading DialogFlow data and creating consolidated file...")
        
        try:
            # Create consolidated file
            consolidated_file_path = self.file_loader.create_consolidated_file(
                self.flow_path, 
                self.output_path
            )
            
            # Save consolidated file info to staging
            self._save_consolidated_file_info(consolidated_file_path)
            
            self.logger.info(f"Consolidated file created: {consolidated_file_path}")
            return consolidated_file_path
            
        except Exception as e:
            self.logger.error(f"Error creating consolidated file: {e}")
            raise
    
    def _save_consolidated_file_info(self, consolidated_file_path: str) -> None:
        """
        Save information about the consolidated file to staging.
        """
        try:
            info_file = self.staging_dir / "consolidated_file_info.txt"
            
            with open(info_file, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("CONSOLIDATED FILE INFORMATION\n")
                f.write("=" * 80 + "\n\n")
                
                f.write(f"Consolidated File Path: {consolidated_file_path}\n")
                f.write(f"Flow Path: {self.flow_path}\n")
                f.write(f"Output Path: {self.output_path}\n")
                f.write(f"Staging Directory: {self.staging_dir}\n\n")
                
                # Get file size
                file_size = Path(consolidated_file_path).stat().st_size
                f.write(f"File Size: {file_size:,} bytes ({file_size/1024:.1f} KB)\n\n")
                
                f.write("=" * 80 + "\n")
                f.write("END OF CONSOLIDATED FILE INFO\n")
                f.write("=" * 80 + "\n")
            
            self.logger.info(f"Consolidated file info saved: {info_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving consolidated file info: {e}")
    
    def analyze_flow(self, consolidated_file_path: str) -> str:
        """
        Analyze the DialogFlow flow using consolidated data.
        
        Args:
            consolidated_file_path: Path to the consolidated file
            
        Returns:
            Path to the analysis report
        """
        self.logger.info("Analyzing DialogFlow flow with consolidated data...")
        
        try:
            # Load consolidated data
            consolidated_data = self.file_loader.load_consolidated_data(consolidated_file_path)
            
            # Generate analysis using consolidated data
            analysis_report = self.flow_analyzer.analyze_flow(consolidated_data)
            
            # Save analysis report
            report_file = self.output_path / "reports" / "flow_analysis_report.md"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(analysis_report)
            
            self.logger.info(f"Analysis report saved to: {report_file}")
            return str(report_file)
            
        except Exception as e:
            self.logger.error(f"Error analyzing flow: {e}")
            raise
    
    def run_full_analysis(self) -> Dict[str, str]:
        """
        Run the complete analysis pipeline using consolidated data.
        
        Returns:
            Dictionary with paths to generated files
        """
        self.logger.info("Starting full DialogFlow analysis with consolidated data...")
        
        try:
            # Load data and create consolidated file
            consolidated_file_path = self.load_dialogflow_data()
            
            # Analyze flow
            analysis_file = self.analyze_flow(consolidated_file_path)
            
            results = {
                'consolidated_file': consolidated_file_path,
                'analysis_report': analysis_file,
                'output_directory': str(self.output_path),
                'staging_directory': str(self.staging_dir)
            }
            
            self.logger.info("Analysis completed successfully!")
            self.logger.info(f"Results: {results}")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Analysis failed: {e}")
            raise


def main():
    """
    Main entry point for the DialogFlow analyzer.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze DialogFlow flows using Gemini LLM')
    parser.add_argument('flow_path', help='Path to DialogFlow export directory')
    parser.add_argument('--output', '-o', default='output', help='Output directory (default: output)')
    parser.add_argument('--api-key', help='Gemini API key (or set GEMINI_API_KEY environment variable)')
    parser.add_argument('--env-file', help='Path to .env file (default: looks for .env in current directory)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Initialize analyzer
        analyzer = DialogFlowAnalyzer(
            flow_path=args.flow_path,
            output_path=args.output,
            api_key=args.api_key,
            env_file=args.env_file
        )
        
        # Run analysis
        results = analyzer.run_full_analysis()
        
        print("\n" + "="*50)
        print("ANALYSIS COMPLETED SUCCESSFULLY!")
        print("="*50)
        print(f"Consolidated File: {results['consolidated_file']}")
        print(f"Analysis Report: {results['analysis_report']}")
        print(f"Output Directory: {results['output_directory']}")
        print(f"Staging Directory: {results['staging_directory']}")
        print("\n" + "="*50)
        print("CONSOLIDATED DATA APPROACH:")
        print("✓ All DialogFlow data combined into single file")
        print("✓ No chunking - preserves complete context")
        print("✓ Full transparency through staging files")
        print("✓ Better analysis quality with complete data")
        print("\n" + "="*50)
        print("STAGING FILES CREATED:")
        print("Check the staging directory to review:")
        print("- Consolidated file information")
        print("- Context data sent to Gemini")
        print("- Prompts used for analysis")
        print("- Gemini responses")
        print("="*50)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
