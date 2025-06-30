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
from flow_designer import FlowDesigner
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
        self.flow_designer = FlowDesigner(self.gemini_client)
        self.flow_analyzer = FlowAnalyzer(self.gemini_client)
        
        # Store loaded data
        self.intents_data = {}
        self.flows_data = {}
        self.entity_types_data = {}
        self.agent_data = {}
        
    def load_dialogflow_data(self) -> Dict[str, Any]:
        """
        Load all DialogFlow data from the export directory.
        
        Returns:
            Dictionary containing all loaded data
        """
        self.logger.info("Loading DialogFlow data...")
        
        try:
            # Load intents
            intents_path = self.flow_path / "intents"
            if intents_path.exists():
                self.intents_data = self.file_loader.load_intents(intents_path)
                self.logger.info(f"Loaded {len(self.intents_data)} intents")
            
            # Load flows
            flows_path = self.flow_path / "flows"
            if flows_path.exists():
                self.flows_data = self.file_loader.load_flows(flows_path)
                self.logger.info(f"Loaded {len(self.flows_data)} flows")
            
            # Load entity types
            entity_types_path = self.flow_path / "entityTypes"
            if entity_types_path.exists():
                self.entity_types_data = self.file_loader.load_entity_types(entity_types_path)
                self.logger.info(f"Loaded {len(self.entity_types_data)} entity types")
            
            # Load agent configuration
            agent_file = self.flow_path / "agent.json"
            if agent_file.exists():
                self.agent_data = self.file_loader.load_agent_config(agent_file)
                self.logger.info("Loaded agent configuration")
            
            # Save loaded data to staging file for review
            self._save_loaded_data_to_staging()
            
            return {
                'intents': self.intents_data,
                'flows': self.flows_data,
                'entity_types': self.entity_types_data,
                'agent': self.agent_data
            }
            
        except Exception as e:
            self.logger.error(f"Error loading DialogFlow data: {e}")
            raise
    
    def _save_loaded_data_to_staging(self) -> None:
        """
        Save loaded DialogFlow data to staging file for review.
        """
        try:
            staging_file = self.staging_dir / "loaded_data_summary.txt"
            
            with open(staging_file, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("LOADED DIALOGFLOW DATA SUMMARY\n")
                f.write("=" * 80 + "\n\n")
                
                f.write(f"Flow Path: {self.flow_path}\n")
                f.write(f"Output Path: {self.output_path}\n")
                f.write(f"Staging Directory: {self.staging_dir}\n\n")
                
                f.write("-" * 40 + "\n")
                f.write("AGENT CONFIGURATION\n")
                f.write("-" * 40 + "\n")
                f.write(json.dumps(self.agent_data, indent=2, ensure_ascii=False))
                f.write("\n\n")
                
                f.write("-" * 40 + "\n")
                f.write("INTENTS SUMMARY\n")
                f.write("-" * 40 + "\n")
                f.write(f"Total Intents: {len(self.intents_data)}\n")
                for intent_name, intent_data in self.intents_data.items():
                    config = intent_data.get('config', {})
                    f.write(f"- {intent_name}: {config.get('displayName', 'N/A')} (Priority: {config.get('priority', 'N/A')})\n")
                f.write("\n")
                
                f.write("-" * 40 + "\n")
                f.write("FLOWS SUMMARY\n")
                f.write("-" * 40 + "\n")
                f.write(f"Total Flows: {len(self.flows_data)}\n")
                for flow_name, flow_data in self.flows_data.items():
                    config = flow_data.get('config', {})
                    pages = flow_data.get('pages', {})
                    f.write(f"- {flow_name}: {config.get('displayName', 'N/A')} ({len(pages)} pages)\n")
                f.write("\n")
                
                f.write("-" * 40 + "\n")
                f.write("ENTITY TYPES SUMMARY\n")
                f.write("-" * 40 + "\n")
                f.write(f"Total Entity Types: {len(self.entity_types_data)}\n")
                for entity_name, entity_data in self.entity_types_data.items():
                    config = entity_data.get('config', {})
                    f.write(f"- {entity_name}: {config.get('displayName', 'N/A')}\n")
                f.write("\n")
                
                f.write("=" * 80 + "\n")
                f.write("END OF DATA SUMMARY\n")
                f.write("=" * 80 + "\n")
            
            self.logger.info(f"Loaded data summary saved: {staging_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving loaded data summary: {e}")
    
    def generate_puml_diagram(self) -> str:
        """
        Generate a PlantUML diagram from the loaded DialogFlow data using LLM.
        
        Returns:
            Path to the generated PUML file
        """
        self.logger.info("Generating PlantUML diagram using LLM...")
        
        try:
            puml_content = self.flow_designer.create_diagram_with_llm(
                intents=self.intents_data,
                flows=self.flows_data,
                entity_types=self.entity_types_data,
                agent=self.agent_data
            )
            
            # Save PUML file
            puml_file = self.output_path / "diagrams" / "dialogflow_flow.puml"
            with open(puml_file, 'w', encoding='utf-8') as f:
                f.write(puml_content)
            
            self.logger.info(f"PUML diagram saved to: {puml_file}")
            return str(puml_file)
            
        except Exception as e:
            self.logger.error(f"Error generating PUML diagram: {e}")
            raise
    
    def analyze_flow(self) -> str:
        """
        Analyze the DialogFlow flow using Gemini LLM.
        
        Returns:
            Path to the analysis report
        """
        self.logger.info("Analyzing DialogFlow flow with Gemini...")
        
        try:
            # Prepare data for analysis
            analysis_data = {
                'intents': self.intents_data,
                'flows': self.flows_data,
                'entity_types': self.entity_types_data,
                'agent': self.agent_data
            }
            
            # Generate analysis
            analysis_report = self.flow_analyzer.analyze_flow(analysis_data)
            
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
        Run the complete analysis pipeline.
        
        Returns:
            Dictionary with paths to generated files
        """
        self.logger.info("Starting full DialogFlow analysis...")
        
        try:
            # Load data
            self.load_dialogflow_data()
            
            # Generate PUML diagram
            puml_file = self.generate_puml_diagram()
            
            # Analyze flow
            analysis_file = self.analyze_flow()
            
            results = {
                'puml_diagram': puml_file,
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
        print(f"PUML Diagram: {results['puml_diagram']}")
        print(f"Analysis Report: {results['analysis_report']}")
        print(f"Output Directory: {results['output_directory']}")
        print(f"Staging Directory: {results['staging_directory']}")
        print("\n" + "="*50)
        print("STAGING FILES CREATED:")
        print("Check the staging directory to review:")
        print("- Context data sent to Gemini")
        print("- Prompts used for analysis")
        print("- Gemini responses")
        print("- Chunked data processing info")
        print("="*50)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
