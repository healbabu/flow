"""
DialogFlow File Loader Module
Handles loading and parsing of DialogFlow export files.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

class DialogFlowFileLoader:
    """
    Loads and parses DialogFlow export files.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def create_consolidated_file(self, flow_path: Path, output_path: Path) -> str:
        """
        Create a consolidated file containing all DialogFlow data.
        
        Args:
            flow_path: Path to the DialogFlow export directory
            output_path: Path where the consolidated file should be saved
            
        Returns:
            Path to the created consolidated file
        """
        try:
            consolidated_file = output_path / "consolidated_dialogflow_data.txt"
            
            with open(consolidated_file, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("CONSOLIDATED DIALOGFLOW DATA\n")
                f.write("=" * 80 + "\n\n")
                
                # Load and write agent configuration
                agent_file = flow_path / "agent.json"
                if agent_file.exists():
                    f.write("-" * 50 + "<agent.json Begins>" + "-" * 50 + "\n")
                    with open(agent_file, 'r', encoding='utf-8') as agent_f:
                        f.write(agent_f.read())
                    f.write("\n" + "-" * 50 + "<agent.json Ends>" + "-" * 50 + "\n\n")
                
                # Load and write intents
                intents_path = flow_path / "intents"
                if intents_path.exists():
                    f.write("-" * 50 + "<intents Begins>" + "-" * 50 + "\n")
                    for intent_dir in intents_path.iterdir():
                        if intent_dir.is_dir():
                            self._write_intent_to_file(f, intent_dir)
                    f.write("-" * 50 + "<intents Ends>" + "-" * 50 + "\n\n")
                
                # Load and write flows
                flows_path = flow_path / "flows"
                if flows_path.exists():
                    f.write("-" * 50 + "<flows Begins>" + "-" * 50 + "\n")
                    for flow_dir in flows_path.iterdir():
                        if flow_dir.is_dir():
                            self._write_flow_to_file(f, flow_dir)
                    f.write("-" * 50 + "<flows Ends>" + "-" * 50 + "\n\n")
                
                # Load and write entity types
                entity_types_path = flow_path / "entityTypes"
                if entity_types_path.exists():
                    f.write("-" * 50 + "<entityTypes Begins>" + "-" * 50 + "\n")
                    for entity_dir in entity_types_path.iterdir():
                        if entity_dir.is_dir():
                            self._write_entity_type_to_file(f, entity_dir)
                    f.write("-" * 50 + "<entityTypes Ends>" + "-" * 50 + "\n\n")
                
                f.write("=" * 80 + "\n")
                f.write("END OF CONSOLIDATED DATA\n")
                f.write("=" * 80 + "\n")
            
            self.logger.info(f"Consolidated file created: {consolidated_file}")
            return str(consolidated_file)
            
        except Exception as e:
            self.logger.error(f"Error creating consolidated file: {e}")
            raise
    
    def _write_intent_to_file(self, file_handle, intent_dir: Path) -> None:
        """Write a single intent to the consolidated file."""
        try:
            intent_name = intent_dir.name
            file_handle.write(f"\n---<intent: {intent_name} Begins>---\n")
            
            # Write intent configuration
            intent_config_file = intent_dir / f"{intent_name}.json"
            if intent_config_file.exists():
                file_handle.write(f"\n---<{intent_name}.json Begins>---\n")
                with open(intent_config_file, 'r', encoding='utf-8') as config_f:
                    file_handle.write(config_f.read())
                file_handle.write(f"\n---<{intent_name}.json Ends>---\n")
            
            # Write training phrases
            training_phrases_dir = intent_dir / "trainingPhrases"
            if training_phrases_dir.exists():
                for lang_file in training_phrases_dir.glob("*.json"):
                    lang = lang_file.stem
                    file_handle.write(f"\n---<{intent_name}/trainingPhrases/{lang}.json Begins>---\n")
                    with open(lang_file, 'r', encoding='utf-8') as lang_f:
                        file_handle.write(lang_f.read())
                    file_handle.write(f"\n---<{intent_name}/trainingPhrases/{lang}.json Ends>---\n")
            
            file_handle.write(f"\n---<intent: {intent_name} Ends>---\n")
            
        except Exception as e:
            self.logger.error(f"Error writing intent {intent_dir.name} to consolidated file: {e}")
    
    def _write_flow_to_file(self, file_handle, flow_dir: Path) -> None:
        """Write a single flow to the consolidated file."""
        try:
            flow_name = flow_dir.name
            file_handle.write(f"\n---<flow: {flow_name} Begins>---\n")
            
            # Write flow configuration
            flow_config_file = flow_dir / f"{flow_name}.json"
            if flow_config_file.exists():
                file_handle.write(f"\n---<{flow_name}.json Begins>---\n")
                with open(flow_config_file, 'r', encoding='utf-8') as config_f:
                    file_handle.write(config_f.read())
                file_handle.write(f"\n---<{flow_name}.json Ends>---\n")
            
            # Write pages
            pages_dir = flow_dir / "pages"
            if pages_dir.exists():
                for page_file in pages_dir.glob("*.json"):
                    page_name = page_file.stem
                    file_handle.write(f"\n---<{flow_name}/pages/{page_name}.json Begins>---\n")
                    with open(page_file, 'r', encoding='utf-8') as page_f:
                        file_handle.write(page_f.read())
                    file_handle.write(f"\n---<{flow_name}/pages/{page_name}.json Ends>---\n")
            
            file_handle.write(f"\n---<flow: {flow_name} Ends>---\n")
            
        except Exception as e:
            self.logger.error(f"Error writing flow {flow_dir.name} to consolidated file: {e}")
    
    def _write_entity_type_to_file(self, file_handle, entity_dir: Path) -> None:
        """Write a single entity type to the consolidated file."""
        try:
            entity_name = entity_dir.name
            file_handle.write(f"\n---<entityType: {entity_name} Begins>---\n")
            
            # Write entity type configuration
            entity_config_file = entity_dir / f"{entity_name}.json"
            if entity_config_file.exists():
                file_handle.write(f"\n---<{entity_name}.json Begins>---\n")
                with open(entity_config_file, 'r', encoding='utf-8') as config_f:
                    file_handle.write(config_f.read())
                file_handle.write(f"\n---<{entity_name}.json Ends>---\n")
            
            # Write entities
            entities_dir = entity_dir / "entities"
            if entities_dir.exists():
                for lang_file in entities_dir.glob("*.json"):
                    lang = lang_file.stem
                    file_handle.write(f"\n---<{entity_name}/entities/{lang}.json Begins>---\n")
                    with open(lang_file, 'r', encoding='utf-8') as lang_f:
                        file_handle.write(lang_f.read())
                    file_handle.write(f"\n---<{entity_name}/entities/{lang}.json Ends>---\n")
            
            file_handle.write(f"\n---<entityType: {entity_name} Ends>---\n")
            
        except Exception as e:
            self.logger.error(f"Error writing entity type {entity_dir.name} to consolidated file: {e}")

    def load_consolidated_data(self, consolidated_file_path: str) -> str:
        """
        Load the consolidated DialogFlow data file.
        
        Args:
            consolidated_file_path: Path to the consolidated file
            
        Returns:
            Content of the consolidated file as string
        """
        try:
            with open(consolidated_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.logger.info(f"Loaded consolidated data from: {consolidated_file_path}")
            return content
            
        except Exception as e:
            self.logger.error(f"Error loading consolidated data: {e}")
            raise

    def load_intents(self, intents_path: Path) -> Dict[str, Any]:
        """
        Load all intents from the intents directory.
        
        Args:
            intents_path: Path to the intents directory
            
        Returns:
            Dictionary of intent data
        """
        intents_data = {}
        
        for intent_dir in intents_path.iterdir():
            if intent_dir.is_dir():
                intent_name = intent_dir.name
                intent_data = self._load_intent(intent_dir)
                if intent_data:
                    intents_data[intent_name] = intent_data
        
        return intents_data
    
    def _load_intent(self, intent_dir: Path) -> Optional[Dict[str, Any]]:
        """
        Load a single intent from its directory.
        
        Args:
            intent_dir: Path to the intent directory
            
        Returns:
            Intent data dictionary
        """
        try:
            intent_data = {}
            
            # Load intent configuration
            intent_config_file = intent_dir / f"{intent_dir.name}.json"
            if intent_config_file.exists():
                with open(intent_config_file, 'r', encoding='utf-8') as f:
                    intent_data['config'] = json.load(f)
            
            # Load training phrases
            training_phrases_dir = intent_dir / "trainingPhrases"
            if training_phrases_dir.exists():
                intent_data['training_phrases'] = {}
                for lang_file in training_phrases_dir.glob("*.json"):
                    lang = lang_file.stem
                    with open(lang_file, 'r', encoding='utf-8') as f:
                        intent_data['training_phrases'][lang] = json.load(f)
            
            return intent_data
            
        except Exception as e:
            self.logger.error(f"Error loading intent {intent_dir.name}: {e}")
            return None
    
    def load_flows(self, flows_path: Path) -> Dict[str, Any]:
        """
        Load all flows from the flows directory.
        
        Args:
            flows_path: Path to the flows directory
            
        Returns:
            Dictionary of flow data
        """
        flows_data = {}
        
        for flow_dir in flows_path.iterdir():
            if flow_dir.is_dir():
                flow_name = flow_dir.name
                flow_data = self._load_flow(flow_dir)
                if flow_data:
                    flows_data[flow_name] = flow_data
        
        return flows_data
    
    def _load_flow(self, flow_dir: Path) -> Optional[Dict[str, Any]]:
        """
        Load a single flow from its directory.
        
        Args:
            flow_dir: Path to the flow directory
            
        Returns:
            Flow data dictionary
        """
        try:
            flow_data = {}
            
            # Load flow configuration
            flow_config_file = flow_dir / f"{flow_dir.name}.json"
            if flow_config_file.exists():
                with open(flow_config_file, 'r', encoding='utf-8') as f:
                    flow_data['config'] = json.load(f)
            
            # Load pages
            pages_dir = flow_dir / "pages"
            if pages_dir.exists():
                flow_data['pages'] = {}
                for page_file in pages_dir.glob("*.json"):
                    page_name = page_file.stem
                    with open(page_file, 'r', encoding='utf-8') as f:
                        flow_data['pages'][page_name] = json.load(f)
            
            return flow_data
            
        except Exception as e:
            self.logger.error(f"Error loading flow {flow_dir.name}: {e}")
            return None
    
    def load_entity_types(self, entity_types_path: Path) -> Dict[str, Any]:
        """
        Load all entity types from the entityTypes directory.
        
        Args:
            entity_types_path: Path to the entityTypes directory
            
        Returns:
            Dictionary of entity type data
        """
        entity_types_data = {}
        
        for entity_dir in entity_types_path.iterdir():
            if entity_dir.is_dir():
                entity_name = entity_dir.name
                entity_data = self._load_entity_type(entity_dir)
                if entity_data:
                    entity_types_data[entity_name] = entity_data
        
        return entity_types_data
    
    def _load_entity_type(self, entity_dir: Path) -> Optional[Dict[str, Any]]:
        """
        Load a single entity type from its directory.
        
        Args:
            entity_dir: Path to the entity type directory
            
        Returns:
            Entity type data dictionary
        """
        try:
            entity_data = {}
            
            # Load entity type configuration
            entity_config_file = entity_dir / f"{entity_dir.name}.json"
            if entity_config_file.exists():
                with open(entity_config_file, 'r', encoding='utf-8') as f:
                    entity_data['config'] = json.load(f)
            
            # Load entities
            entities_dir = entity_dir / "entities"
            if entities_dir.exists():
                entity_data['entities'] = {}
                for lang_file in entities_dir.glob("*.json"):
                    lang = lang_file.stem
                    with open(lang_file, 'r', encoding='utf-8') as f:
                        entity_data['entities'][lang] = json.load(f)
            
            return entity_data
            
        except Exception as e:
            self.logger.error(f"Error loading entity type {entity_dir.name}: {e}")
            return None
    
    def load_agent_config(self, agent_file: Path) -> Dict[str, Any]:
        """
        Load agent configuration from agent.json.
        
        Args:
            agent_file: Path to agent.json
            
        Returns:
            Agent configuration data
        """
        try:
            with open(agent_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading agent config: {e}")
            return {} 