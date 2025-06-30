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