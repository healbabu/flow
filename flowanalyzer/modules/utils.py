"""
Utility functions for the DialogFlow analyzer.
"""

import os
import logging
from pathlib import Path
from typing import Optional

def setup_logging(log_dir: Optional[Path] = None) -> None:
    """
    Setup logging configuration.
    
    Args:
        log_dir: Directory for log files
    """
    # Create log directory if specified
    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "flow_analyzer.log"
    else:
        log_file = None
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file) if log_file else logging.NullHandler()
        ]
    )

def create_output_directories(output_path: Path) -> None:
    """
    Create output directories.
    
    Args:
        output_path: Base output path
    """
    directories = [
        output_path / "diagrams",
        output_path / "reports",
        output_path / "logs"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def validate_flow_path(flow_path: Path) -> bool:
    """
    Validate that the flow path contains DialogFlow export files.
    
    Args:
        flow_path: Path to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_dirs = ["intents", "flows"]
    required_files = ["agent.json"]
    
    # Check required directories
    for dir_name in required_dirs:
        if not (flow_path / dir_name).exists():
            return False
    
    # Check required files
    for file_name in required_files:
        if not (flow_path / file_name).exists():
            return False
    
    return True

def get_file_size_mb(file_path: Path) -> float:
    """
    Get file size in megabytes.
    
    Args:
        file_path: Path to file
        
    Returns:
        File size in MB
    """
    return file_path.stat().st_size / (1024 * 1024) 