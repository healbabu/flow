"""
Flow Designer Module
Handles the creation of PlantUML diagrams from DialogFlow data using LLM.
"""

import json
import logging
from typing import Dict, Any, List
from gemini_client import GeminiClient

class FlowDesigner:
    """
    Creates PlantUML diagrams from DialogFlow flow data using LLM.
    """
    
    def __init__(self, gemini_client: GeminiClient):
        """
        Initialize the flow designer.
        
        Args:
            gemini_client: Gemini client instance
        """
        self.logger = logging.getLogger(__name__)
        self.gemini_client = gemini_client
        self.puml_prompt = self._load_puml_prompt()
    
    def create_diagram_with_llm(self, intents: Dict[str, Any], flows: Dict[str, Any], 
                               entity_types: Dict[str, Any], agent: Dict[str, Any]) -> str:
        """
        Create a PlantUML diagram from DialogFlow data using LLM.
        
        Args:
            intents: Intent data
            flows: Flow data
            entity_types: Entity type data
            agent: Agent configuration
            
        Returns:
            PlantUML diagram content
        """
        self.logger.info("Creating PlantUML diagram with LLM...")
        
        try:
            # Prepare data for LLM
            flow_data = self._prepare_flow_data(intents, flows, entity_types, agent)
            
            # Generate PUML using LLM
            puml_content = self.gemini_client.analyze_text(self.puml_prompt, flow_data, request_id="puml_diagram_generation")
            
            # Clean and validate PUML content
            cleaned_puml = self._clean_puml_content(puml_content)
            
            self.logger.info("PlantUML diagram generated successfully")
            return cleaned_puml
            
        except Exception as e:
            self.logger.error(f"Error creating PUML diagram with LLM: {e}")
            # Fallback to basic diagram
            return self._create_fallback_diagram(intents, flows, entity_types, agent)
    
    def _prepare_flow_data(self, intents: Dict[str, Any], flows: Dict[str, Any], 
                          entity_types: Dict[str, Any], agent: Dict[str, Any]) -> str:
        """
        Prepare flow data for LLM processing.
        
        Args:
            intents: Intent data
            flows: Flow data
            entity_types: Entity type data
            agent: Agent configuration
            
        Returns:
            Formatted data for LLM
        """
        try:
            # Create a structured summary of the flow
            flow_summary = {
                'agent_info': {
                    'name': agent.get('displayName', 'Unknown Agent'),
                    'language': agent.get('defaultLanguageCode', 'en'),
                    'start_flow': agent.get('startFlow', 'Default Start Flow')
                },
                'intents': self._summarize_intents(intents),
                'flows': self._summarize_flows(flows),
                'entity_types': self._summarize_entity_types(entity_types),
                'flow_connections': self._extract_flow_connections(flows),
                'page_details': self._extract_page_details(flows)
            }
            
            return json.dumps(flow_summary, indent=2, ensure_ascii=False)
            
        except Exception as e:
            self.logger.error(f"Error preparing flow data: {e}")
            raise
    
    def _summarize_intents(self, intents: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary of intents."""
        summary = {}
        
        for intent_name, intent_data in intents.items():
            config = intent_data.get('config', {})
            summary[intent_name] = {
                'display_name': config.get('displayName', intent_name),
                'priority': config.get('priority', 500000),
                'is_fallback': config.get('isFallback', False),
                'parameters': config.get('parameters', []),
                'training_phrases_count': config.get('numTrainingPhrases', 0)
            }
        
        return summary
    
    def _summarize_flows(self, flows: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary of flows."""
        summary = {}
        
        for flow_name, flow_data in flows.items():
            config = flow_data.get('config', {})
            pages = flow_data.get('pages', {})
            
            summary[flow_name] = {
                'display_name': config.get('displayName', flow_name),
                'description': config.get('description', ''),
                'pages_count': len(pages),
                'pages': list(pages.keys()),
                'transition_routes': config.get('transitionRoutes', []),
                'event_handlers': config.get('eventHandlers', [])
            }
        
        return summary
    
    def _summarize_entity_types(self, entity_types: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary of entity types."""
        summary = {}
        
        for entity_name, entity_data in entity_types.items():
            config = entity_data.get('config', {})
            entities = entity_data.get('entities', {})
            
            summary[entity_name] = {
                'display_name': config.get('displayName', entity_name),
                'kind': config.get('kind', 'KIND_MAP'),
                'entities_count': len(entities.get('en', {}).get('entities', [])),
                'entities': entities.get('en', {}).get('entities', [])
            }
        
        return summary
    
    def _extract_flow_connections(self, flows: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract flow connections and transitions."""
        connections = []
        
        for flow_name, flow_data in flows.items():
            config = flow_data.get('config', {})
            
            # Extract transition routes
            for route in config.get('transitionRoutes', []):
                connections.append({
                    'type': 'transition_route',
                    'flow': flow_name,
                    'intent': route.get('intent'),
                    'target_page': route.get('targetPage'),
                    'condition': route.get('condition')
                })
            
            # Extract event handlers
            for handler in config.get('eventHandlers', []):
                connections.append({
                    'type': 'event_handler',
                    'flow': flow_name,
                    'event': handler.get('event'),
                    'target_page': handler.get('targetPage')
                })
            
            # Extract page-to-page connections
            pages = flow_data.get('pages', {})
            for page_name, page_data in pages.items():
                for route in page_data.get('transitionRoutes', []):
                    connections.append({
                        'type': 'page_transition',
                        'flow': flow_name,
                        'page': page_name,
                        'intent': route.get('intent'),
                        'target_page': route.get('targetPage'),
                        'condition': route.get('condition')
                    })
        
        return connections
    
    def _extract_page_details(self, flows: Dict[str, Any]) -> Dict[str, Any]:
        """Extract detailed page information."""
        page_details = {}
        
        for flow_name, flow_data in flows.items():
            pages = flow_data.get('pages', {})
            
            for page_name, page_data in pages.items():
                full_page_name = f"{flow_name}.{page_name}"
                page_details[full_page_name] = {
                    'display_name': page_data.get('displayName', page_name),
                    'form_parameters': page_data.get('form', {}).get('parameters', []),
                    'entry_fulfillment': page_data.get('entryFulfillment', {}),
                    'transition_routes': page_data.get('transitionRoutes', []),
                    'event_handlers': page_data.get('eventHandlers', [])
                }
        
        return page_details
    
    def _clean_puml_content(self, puml_content: str) -> str:
        """
        Clean and validate PUML content from LLM.
        
        Args:
            puml_content: Raw PUML content from LLM
            
        Returns:
            Cleaned PUML content
        """
        # Remove markdown code blocks if present
        if puml_content.startswith('```'):
            lines = puml_content.split('\n')
            start_idx = None
            end_idx = None
            
            for i, line in enumerate(lines):
                if line.strip().startswith('```') and start_idx is None:
                    start_idx = i + 1
                elif line.strip().startswith('```') and start_idx is not None:
                    end_idx = i
                    break
            
            if start_idx is not None and end_idx is not None:
                puml_content = '\n'.join(lines[start_idx:end_idx])
        
        # Ensure proper start and end tags
        if not puml_content.strip().startswith('@startuml'):
            puml_content = '@startuml DialogFlow Flow Analysis\n' + puml_content
        
        if not puml_content.strip().endswith('@enduml'):
            puml_content = puml_content + '\n@enduml'
        
        return puml_content
    
    def _create_fallback_diagram(self, intents: Dict[str, Any], flows: Dict[str, Any], 
                                entity_types: Dict[str, Any], agent: Dict[str, Any]) -> str:
        """
        Create a basic fallback diagram if LLM generation fails.
        
        Args:
            intents: Intent data
            flows: Flow data
            entity_types: Entity type data
            agent: Agent configuration
            
        Returns:
            Basic PlantUML diagram
        """
        return f"""@startuml DialogFlow Flow Analysis
!theme plain
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam defaultFontSize 10

title DialogFlow Flow Analysis - {agent.get('displayName', 'Unknown Agent')}

' Basic components
rectangle "Intents ({len(intents)})" as intents
rectangle "Flows ({len(flows)})" as flows
rectangle "Entity Types ({len(entity_types)})" as entities

' Basic connections
intents --> flows : "triggers"
flows --> entities : "uses"

note right of intents
  Intent count: {len(intents)}
  Main intents: {', '.join(list(intents.keys())[:5])}
end note

note right of flows
  Flow count: {len(flows)}
  Main flows: {', '.join(list(flows.keys())[:5])}
end note

@enduml"""
    
    def _load_puml_prompt(self) -> str:
        """Load the PUML generation prompt."""
        return """
# PlantUML Diagram Generation for DialogFlow Flows

You are an expert in creating PlantUML diagrams for conversational AI flows. Your task is to analyze the provided DialogFlow data and create a comprehensive, well-structured PlantUML diagram that visualizes the flow architecture.

## Requirements

### 1. Diagram Structure
- Use proper PlantUML syntax
- Include all major components: Intents, Flows, Pages, Entity Types
- Show clear relationships and connections between components
- Use appropriate colors and styling for different component types

### 2. Component Organization
- **Intents**: Group related intents together
- **Flows**: Show the main flow structure with pages
- **Pages**: Include all pages with their relationships
- **Entity Types**: Show entity definitions and relationships
- **System Events**: Include error handlers and system events

### 3. Visual Design
- Use meaningful colors for different component types
- Include proper spacing and layout
- Add notes for important information
- Make the diagram easy to read and understand

### 4. Connection Types
- **Intent Triggers**: Show which intents trigger which pages
- **Page Transitions**: Show page-to-page navigation
- **Event Handlers**: Show system event handling
- **Form Completions**: Show form parameter relationships

## PlantUML Guidelines

### Styling
```plantuml
skinparam rectangle {
    BackgroundColor<<Intent>> #E3F2FD
    BorderColor<<Intent>> #1565C0
    FontColor<<Intent>> #0D47A1
}

skinparam rectangle {
    BackgroundColor<<Page>> #FFF3E0
    BorderColor<<Page>> #E65100
    FontColor<<Page>> #BF360C
}

skinparam rectangle {
    BackgroundColor<<Confirmation>> #F3E5F5
    BorderColor<<Confirmation>> #7B1FA2
    FontColor<<Confirmation>> #4A148C
}

skinparam rectangle {
    BackgroundColor<<System>> #FFEBEE
    BorderColor<<System>> #C62828
    FontColor<<System>> #B71C1C
}
```

### Component Types
- Use `<<Intent>>` for user intents
- Use `<<Page>>` for flow pages
- Use `<<Confirmation>>` for confirmation pages
- Use `<<System>>` for system events and handlers
- Use `<<Entity>>` for entity types

### Connection Labels
- Use descriptive labels for connections
- Include intent names for intent-based transitions
- Include conditions for conditional transitions
- Use "handles" for event handlers
- Use "targets" for direct page targets

## Analysis Instructions

1. **Analyze the flow structure** and identify the main components
2. **Group related components** logically
3. **Identify all connections** between components
4. **Determine appropriate styling** for each component type
5. **Add meaningful notes** for important information
6. **Ensure the diagram is complete** and shows all major relationships

## Output Format

Generate a complete PlantUML diagram that includes:
- Proper header with title and styling
- All major components organized logically
- Clear connections with descriptive labels
- Appropriate notes and documentation
- Proper footer

The diagram should be immediately usable in any PlantUML renderer and should provide a clear visual representation of the DialogFlow architecture.

Please analyze the provided DialogFlow data and create a comprehensive PlantUML diagram following these guidelines.
""" 