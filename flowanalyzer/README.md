# DialogFlow Flow Analyzer

A Python tool to analyze DialogFlow flows using Gemini LLM, with staging functionality for debugging and auditing.

## Quick Start

### 1. Install Dependencies
```bash
pip install google-generativeai python-dotenv
```

### 2. Set Up API Key
Create a `.env` file in the flowanalyzer directory:
```bash
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
```

### 3. Run the Analyzer
```bash
python analyzer.py Flow --output my_analysis
```

## Usage

### Basic Analysis
```bash
python analyzer.py Flow
```

### Custom Output Directory
```bash
python analyzer.py Flow --output my_custom_output
```

### Verbose Logging
```bash
python analyzer.py Flow --output my_analysis --verbose
```

### Custom API Key
```bash
python analyzer.py Flow --api-key "your_api_key_here"
```

## Test the Setup
```bash
python test_staging.py
```

## Output Files

- **`output/diagrams/dialogflow_flow.puml`** - PlantUML diagram
- **`output/reports/flow_analysis_report.md`** - Analysis report  
- **`output/staging/`** - Debug files (context, prompts, responses)
- **`output/logs/`** - Application logs

## Troubleshooting

### "Gemini API key is required"
Set your API key in `.env` file, environment variable, or command line parameter.

### "No module named 'google.generativeai'"
```bash
pip install google-generativeai
```

### "No module named 'dotenv'"
```bash
pip install python-dotenv
```

### Import errors
Make sure you're running from the `flowanalyzer` directory.

## Command Line Options

```bash
python analyzer.py flow_path [OPTIONS]

Arguments:
  flow_path              Path to DialogFlow export directory

Options:
  --output, -o           Output directory (default: output)
  --api-key              Gemini API key
  --env-file             Path to .env file
  --verbose, -v          Enable verbose logging
  --help                 Show help message
``` 