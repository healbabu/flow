"""
Gemini Client Module
Handles interactions with Google's Gemini API.
"""

import os
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

DOTENV_AVAILABLE = True

class GeminiClient:
    """
    Client for interacting with Google's Gemini API.
    """
    
    def __init__(self, api_key: Optional[str] = None, staging_dir: Optional[str] = None, env_file: Optional[str] = None):
        """
        Initialize the Gemini client.
        
        Args:
            api_key: Gemini API key
            staging_dir: Directory to save staging files for review
            env_file: Path to .env file (default: looks for .env in current directory)
        """
        self.logger = logging.getLogger(__name__)
        
        # Load environment variables from .env file if available
        self._load_env_file(env_file)
        
        # Get API key from parameter, environment variable, or .env file
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.staging_dir = Path(staging_dir) if staging_dir else None
        
        if not self.api_key:
            raise ValueError(
                "Gemini API key is required. Set GEMINI_API_KEY environment variable, "
                "pass api_key parameter, or add it to your .env file."
            )
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        
        # Create staging directory if specified
        if self.staging_dir:
            self.staging_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_env_file(self, env_file: Optional[str] = None) -> None:
        """
        Load environment variables from .env file.
        
        Args:
            env_file: Path to .env file (default: looks for .env in current directory)
        """
        if not DOTENV_AVAILABLE:
            self.logger.warning(
                "python-dotenv not available. Install it with 'pip install python-dotenv' "
                "to enable .env file support."
            )
            return
        
        try:
            # Determine .env file path
            if env_file:
                env_path = Path(env_file)
            else:
                # Look for .env file in current directory and parent directories
                env_path = self._find_env_file()
            
            if env_path and env_path.exists():
                load_dotenv(env_path)
                self.logger.info(f"Loaded environment variables from: {env_path}")
            else:
                self.logger.info("No .env file found, using system environment variables")
                
        except Exception as e:
            self.logger.error(f"Error loading .env file: {e}")
    
    def _find_env_file(self) -> Optional[Path]:
        """
        Find .env file in current directory or parent directories.
        
        Returns:
            Path to .env file if found, None otherwise
        """
        current_dir = Path.cwd()
        
        # Check current directory and up to 3 parent directories
        for i in range(4):
            check_dir = current_dir
            for _ in range(i):
                check_dir = check_dir.parent
            
            env_file = check_dir / ".env"
            if env_file.exists():
                return env_file
        
        return None
    
    def analyze_text(self, prompt: str, context: str, request_id: str = "default") -> str:
        """
        Analyze text using Gemini.
        
        Args:
            prompt: Analysis prompt
            context: Context data to analyze
            request_id: Unique identifier for this request (used in staging files)
            
        Returns:
            Analysis result
        """
        try:
            # Combine prompt and context
            full_prompt = f"{prompt}\n\nContext Data:\n{context}"
            
            # Save to staging file if staging directory is set
            if self.staging_dir:
                self._save_staging_file(request_id, prompt, context, full_prompt)
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            
            if response.text:
                # Save response to staging file
                if self.staging_dir:
                    self._save_response_file(request_id, response.text)
                return response.text
            else:
                raise Exception("No response generated from Gemini")
                
        except Exception as e:
            self.logger.error(f"Error calling Gemini API: {e}")
            raise
    
    def _save_staging_file(self, request_id: str, prompt: str, context: str, full_prompt: str) -> None:
        """
        Save prompt, context, and full prompt to staging file for review.
        
        Args:
            request_id: Unique identifier for this request
            prompt: Original prompt
            context: Context data
            full_prompt: Combined prompt and context
        """
        try:
            staging_file = self.staging_dir / f"staging_{request_id}.txt"
            
            with open(staging_file, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("DIALOGFLOW FLOW ANALYZER - STAGING FILE\n")
                f.write("=" * 80 + "\n\n")
                
                f.write("REQUEST ID: " + request_id + "\n")
                f.write("TIMESTAMP: " + str(Path().stat().st_mtime) + "\n\n")
                
                f.write("-" * 40 + "\n")
                f.write("ORIGINAL PROMPT\n")
                f.write("-" * 40 + "\n")
                f.write(prompt)
                f.write("\n\n")
                
                f.write("-" * 40 + "\n")
                f.write("CONTEXT DATA\n")
                f.write("-" * 40 + "\n")
                f.write(context)
                f.write("\n\n")
                
                f.write("-" * 40 + "\n")
                f.write("FULL PROMPT (SENT TO GEMINI)\n")
                f.write("-" * 40 + "\n")
                f.write(full_prompt)
                f.write("\n\n")
                
                f.write("=" * 80 + "\n")
                f.write("END OF STAGING FILE\n")
                f.write("=" * 80 + "\n")
            
            self.logger.info(f"Staging file saved: {staging_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving staging file: {e}")
    
    def _save_response_file(self, request_id: str, response: str) -> None:
        """
        Save Gemini response to file.
        
        Args:
            request_id: Unique identifier for this request
            response: Response from Gemini
        """
        try:
            response_file = self.staging_dir / f"response_{request_id}.txt"
            
            with open(response_file, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("GEMINI RESPONSE\n")
                f.write("=" * 80 + "\n\n")
                
                f.write("REQUEST ID: " + request_id + "\n")
                f.write("TIMESTAMP: " + str(Path().stat().st_mtime) + "\n\n")
                
                f.write("-" * 40 + "\n")
                f.write("RESPONSE CONTENT\n")
                f.write("-" * 40 + "\n")
                f.write(response)
                f.write("\n\n")
                
                f.write("=" * 80 + "\n")
                f.write("END OF RESPONSE\n")
                f.write("=" * 80 + "\n")
            
            self.logger.info(f"Response file saved: {response_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving response file: {e}")
    
    def analyze_consolidated_data(self, prompt: str, consolidated_data: str, request_id: str = "consolidated_analysis") -> str:
        """
        Analyze consolidated DialogFlow data without chunking to preserve context.
        
        Args:
            prompt: Analysis prompt
            consolidated_data: Complete consolidated DialogFlow data
            request_id: Unique identifier for this request
            
        Returns:
            Analysis result
        """
        try:
            # Combine prompt and consolidated data
            full_prompt = f"{prompt}\n\nConsolidated DialogFlow Data:\n{consolidated_data}"
            
            # Save to staging file if staging directory is set
            if self.staging_dir:
                self._save_consolidated_staging_file(request_id, prompt, consolidated_data, full_prompt)
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            
            if response.text:
                # Save response to staging file
                if self.staging_dir:
                    self._save_response_file(request_id, response.text)
                return response.text
            else:
                raise Exception("No response generated from Gemini")
                
        except Exception as e:
            self.logger.error(f"Error calling Gemini API with consolidated data: {e}")
            raise
    
    def _save_consolidated_staging_file(self, request_id: str, prompt: str, consolidated_data: str, full_prompt: str) -> None:
        """
        Save consolidated data prompt and context to staging file for review.
        
        Args:
            request_id: Unique identifier for this request
            prompt: Original prompt
            consolidated_data: Complete consolidated data
            full_prompt: Combined prompt and consolidated data
        """
        try:
            staging_file = self.staging_dir / f"consolidated_staging_{request_id}.txt"
            
            with open(staging_file, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("CONSOLIDATED DIALOGFLOW ANALYSIS - STAGING FILE\n")
                f.write("=" * 80 + "\n\n")
                
                f.write("REQUEST ID: " + request_id + "\n")
                f.write("TIMESTAMP: " + str(Path().stat().st_mtime) + "\n")
                f.write("DATA SIZE: " + str(len(consolidated_data)) + " characters\n\n")
                
                f.write("-" * 40 + "\n")
                f.write("ORIGINAL PROMPT\n")
                f.write("-" * 40 + "\n")
                f.write(prompt)
                f.write("\n\n")
                
                f.write("-" * 40 + "\n")
                f.write("CONSOLIDATED DATA PREVIEW (First 1000 chars)\n")
                f.write("-" * 40 + "\n")
                f.write(consolidated_data[:1000] + "..." if len(consolidated_data) > 1000 else consolidated_data)
                f.write("\n\n")
                
                f.write("-" * 40 + "\n")
                f.write("FULL PROMPT PREVIEW (First 1500 chars)\n")
                f.write("-" * 40 + "\n")
                f.write(full_prompt[:1500] + "..." if len(full_prompt) > 1500 else full_prompt)
                f.write("\n\n")
                
                f.write("=" * 80 + "\n")
                f.write("END OF CONSOLIDATED STAGING FILE\n")
                f.write("=" * 80 + "\n")
            
            self.logger.info(f"Consolidated staging file saved: {staging_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving consolidated staging file: {e}") 