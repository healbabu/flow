"""
DialogFlow Flow Analyzer Module
Analyzes DialogFlow flows using Gemini LLM.
"""

import json
import logging
from typing import Dict, Any
from gemini_client import GeminiClient

class FlowAnalyzer:
    """
    Analyzes DialogFlow flows using Gemini LLM.
    """
    
    def __init__(self, gemini_client: GeminiClient):
        """
        Initialize the flow analyzer.
        
        Args:
            gemini_client: Gemini client instance
        """
        self.logger = logging.getLogger(__name__)
        self.gemini_client = gemini_client
        self.analysis_prompt = self._load_analysis_prompt()
    
    def analyze_flow(self, consolidated_data: str) -> str:
        """
        Analyze a DialogFlow flow using consolidated data.
        
        Args:
            consolidated_data: Complete consolidated DialogFlow data as string
            
        Returns:
            Analysis report
        """
        try:
            # Analyze using Gemini with consolidated data
            analysis_result = self.gemini_client.analyze_consolidated_data(
                self.analysis_prompt, 
                consolidated_data,
                request_id="flow_analysis"
            )
            
            return analysis_result
            
        except Exception as e:
            self.logger.error(f"Error analyzing flow: {e}")
            raise
    
    def analyze_flow_from_dict(self, flow_data: Dict[str, Any]) -> str:
        """
        Analyze a DialogFlow flow from dictionary data (legacy method for backward compatibility).
        
        Args:
            flow_data: DialogFlow data dictionary
            
        Returns:
            Analysis report
        """
        try:
            # Prepare data for analysis
            context_data = self._prepare_analysis_data(flow_data)
            
            # Analyze using consolidated approach
            return self.analyze_flow(context_data)
            
        except Exception as e:
            self.logger.error(f"Error analyzing flow from dict: {e}")
            raise
    
    def _prepare_analysis_data(self, flow_data: Dict[str, Any]) -> str:
        """
        Prepare flow data for analysis.
        
        Args:
            flow_data: Raw flow data
            
        Returns:
            Formatted data for analysis
        """
        try:
            # Convert to JSON for better formatting
            formatted_data = {
                'intents': self._format_intents(flow_data.get('intents', {})),
                'flows': self._format_flows(flow_data.get('flows', {})),
                'entity_types': self._format_entity_types(flow_data.get('entity_types', {})),
                'agent': flow_data.get('agent', {})
            }
            
            return json.dumps(formatted_data, indent=2, ensure_ascii=False)
            
        except Exception as e:
            self.logger.error(f"Error preparing analysis data: {e}")
            raise
    
    def _format_intents(self, intents: Dict[str, Any]) -> Dict[str, Any]:
        """Format intents data for analysis."""
        formatted_intents = {}
        
        for intent_name, intent_data in intents.items():
            formatted_intent = {
                'name': intent_name,
                'config': intent_data.get('config', {}),
                'training_phrases': intent_data.get('training_phrases', {})
            }
            formatted_intents[intent_name] = formatted_intent
        
        return formatted_intents
    
    def _format_flows(self, flows: Dict[str, Any]) -> Dict[str, Any]:
        """Format flows data for analysis."""
        formatted_flows = {}
        
        for flow_name, flow_data in flows.items():
            formatted_flow = {
                'name': flow_name,
                'config': flow_data.get('config', {}),
                'pages': flow_data.get('pages', {})
            }
            formatted_flows[flow_name] = formatted_flow
        
        return formatted_flows
    
    def _format_entity_types(self, entity_types: Dict[str, Any]) -> Dict[str, Any]:
        """Format entity types data for analysis."""
        formatted_entities = {}
        
        for entity_name, entity_data in entity_types.items():
            formatted_entity = {
                'name': entity_name,
                'config': entity_data.get('config', {}),
                'entities': entity_data.get('entities', {})
            }
            formatted_entities[entity_name] = formatted_entity
        
        return formatted_entities
    
    def _load_analysis_prompt(self) -> str:
        """Load the analysis prompt."""
        return """
# DialogFlow Flow Analysis Prompt

## Context
You are an expert google DialogFlow architect tasked with analyzing a conversational flow for potential issues, dead ends, and user experience problems. Your goal is to identify architectural weaknesses and provide actionable recommendations for improvement.
The observations should be specific with pointer to the problem and the solution.

## Analysis Framework

### 1. Flow Structure Analysis
- **Entry Points**: Identify all possible ways users can enter the flow
- **Exit Points**: Map all termination points and session endings
- **Navigation Paths**: Trace all possible user journeys through the flow
- **Decision Points**: Identify where users make choices and what happens for each option

### 2. Dead End Detection
- **Terminal Pages**: Find pages that end sessions without providing continuation options
- **Exception Handling**: Identify scenarios where users might get stuck due to errors
- **Missing Handlers**: Look for user inputs that aren't handled
- **Incomplete Flows**: Find paths that don't lead to logical conclusions


### 3. User Experience Assessment
- **Flexibility**: Can users navigate freely or are they forced into linear paths?
- **Error Recovery**: How well does the flow handle user mistakes or unclear inputs?
- **Information Flow**: Do users have enough information to make decisions?
- **Confirmation Patterns**: Are confirmations clear and allow for corrections?

### 4. Intent Coverage Analysis
- **Missing Intents**: What user intents might not be covered?
- **Intent Conflicts**: Are there overlapping or conflicting intents?
- **Fallback Handling**: How are unrecognized inputs handled?
- **Context Management**: How well does the flow maintain context?

### 5. Technical Architecture Review
- **Form Validation**: Are required fields properly validated?
- **Parameter Management**: How are user inputs stored and used?
- **Event Handling**: Are system events properly managed?
- **Session Management**: How is user state maintained?

## Specific Questions to Answer

### Flow Continuity
1. Can users easily navigate back to previous steps?
2. Are there "start over" or "cancel" options available?
3. What happens if users want to modify earlier decisions?
4. Are there graceful exits at every major decision point?

### Error Handling
1. What happens when users provide invalid inputs?
2. Are error messages helpful and actionable?
3. Do users get stuck in error loops?
4. Are there fallback options when the flow fails?

### User Intent Coverage
1. What common user requests might not be handled?
2. Are there edge cases that could confuse users?
3. How well does the flow handle ambiguous inputs?
4. Are there missing confirmation or clarification steps?

### Information Architecture
1. Do users have enough context to make decisions?
2. Is information presented in logical order?
3. Are there opportunities for users to ask questions?
4. Is pricing and availability information clear?

## Output Format

+--------------------------------------------------------------------------------------
|Priority|Issue\Observation|Where the issue is located in |Solution|
|--------|-----------------|----------------------------|--------|
|High|Dead End|Flow <flow_name> without an exit option|Add an exit option to the flow|
|Medium|Incomplete Flow|User journey is not complete in <page_name>|Add missing pages to the flow|
|Low|Missing Error Handler|User gets stuck in an error loop in <page_name>|Add an error handler to the flow|
|Low|Missing Navigation Option|User gets stuck in a flow without a navigation option in <intent_name>|Add a navigation option to the intent|


Please analyze the provided DialogFlow data and provide a comprehensive report following this framework.
""" 