# DialogFlow Flow Analyzer

A Python tool to analyze DialogFlow flows using Gemini LLM with a **consolidated data approach** that preserves complete context without chunking.

## 🆕 New Consolidated Approach

The analyzer now uses a **consolidated file approach** that combines all DialogFlow data into a single file with clear separators, eliminating the need for chunking and preserving complete context for better analysis quality.

### Key Benefits:
- ✅ **No Chunking** - Complete context preserved
- ✅ **Better Analysis** - Full relationships between components
- ✅ **Simpler Processing** - Single file, single LLM call
- ✅ **Full Transparency** - Complete audit trail
- ✅ **Easier Debugging** - All data in one place

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

## Test the New Approach
```bash
python test_consolidated.py
```

## Output Files

- **`output/consolidated_dialogflow_data.txt`** - Complete consolidated data
- **`output/reports/flow_analysis_report.md`** - Analysis report  
- **`output/staging/`** - Debug files (context, prompts, responses)
- **`output/logs/`** - Application logs

## How the Consolidated Approach Works

### 1. Data Consolidation
```
Flow/
├── agent.json
├── intents/
│   ├── intent1/
│   └── intent2/
├── flows/
│   ├── flow1/
│   └── flow2/
└── entityTypes/
    ├── entity1/
    └── entity2/
```

**Becomes:**
```
consolidated_dialogflow_data.txt
├── <agent.json Begins>
├── <intents Begins>
│   ├── <intent: intent1 Begins>
│   └── <intent: intent2 Begins>
├── <flows Begins>
│   ├── <flow: flow1 Begins>
│   └── <flow: flow2 Begins>
└── <entityTypes Begins>
    ├── <entityType: entity1 Begins>
    └── <entityType: entity2 Begins>
```

### 2. Single LLM Call
- **Complete data** sent to Gemini in one request
- **No chunking** - preserves all relationships
- **Full context** for better analysis
- **Single response** with comprehensive insights

### 3. Staging Transparency
- **Complete audit trail** of what was sent
- **Full prompt and response** logging
- **File size and processing** information
- **Easy debugging** and review

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

### Large file handling
The consolidated approach handles large DialogFlow exports without chunking. If you encounter API limits, the system will provide clear error messages.

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

## Comparison: Old vs New Approach

| Feature | Old (Chunking) | New (Consolidated) |
|---------|----------------|-------------------|
| **Data Processing** | Split into chunks | Single consolidated file |
| **Context Preservation** | Limited per chunk | Complete context |
| **LLM Calls** | Multiple (chunks + combine) | Single call |
| **Analysis Quality** | Fragmented insights | Comprehensive analysis |
| **Debugging** | Complex chunk tracking | Simple file review |
| **Transparency** | Multiple staging files | Clear audit trail |
| **Performance** | Slower (multiple calls) | Faster (single call) |
| **Reliability** | Risk of chunk loss | Complete data guarantee |

## Architecture

```
DialogFlow Export
       ↓
File Loader (Consolidates)
       ↓
Consolidated File
       ↓
Gemini LLM (Single Call)
       ↓
Analysis Results
```

The new approach ensures **complete context preservation** and **better analysis quality** while maintaining **full transparency** through comprehensive staging and logging. 