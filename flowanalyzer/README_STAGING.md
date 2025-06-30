# DialogFlow Flow Analyzer - Staging Functionality

## Overview

The DialogFlow Flow Analyzer now includes a staging system that saves all context data, prompts, and LLM responses to files for review before and after sending to Gemini. This allows you to:

- **Review context**: See exactly what data is being sent to the LLM
- **Debug prompts**: Examine the prompts used for analysis
- **Track responses**: Review Gemini's responses
- **Optimize performance**: Identify opportunities to improve context or prompts
- **Audit conversations**: Keep a record of all LLM interactions

## Environment Configuration

### .env File Support

The analyzer supports loading configuration from `.env` files for easier API key management:

1. **Install python-dotenv** (if not already installed):
   ```bash
   pip install python-dotenv
   ```

2. **Create a .env file** by copying the template:
   ```bash
   cp env_example.txt .env
   ```

3. **Configure your API key** in the `.env` file:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

4. **The analyzer will automatically**:
   - Look for `.env` files in the current directory and parent directories
   - Load environment variables from the first `.env` file found
   - Use the API key from the `.env` file

### API Key Priority Order

The analyzer looks for the API key in this order:
1. **Command line parameter**: `--api-key`
2. **Environment variable**: `GEMINI_API_KEY`
3. **.env file**: `GEMINI_API_KEY=your_key`

### .env File Locations

The analyzer searches for `.env` files in:
- Current working directory
- Parent directory (up to 3 levels up)
- Custom path specified with `--env-file`

## How It Works

### Staging Directory Structure

When you run the analyzer, a `staging` directory is created in your output folder with the following structure:

```
output/
├── staging/
│   ├── loaded_data_summary.txt          # Summary of loaded DialogFlow data
│   ├── staging_[request_id].txt         # Context and prompts before LLM call
│   ├── response_[request_id].txt        # Gemini response after LLM call
│   ├── chunk_info_[request_id].txt      # Information about chunked data processing
│   └── ...
├── diagrams/
├── reports/
└── logs/
```

### File Types

#### 1. `loaded_data_summary.txt`
- Overview of all loaded DialogFlow data
- Agent configuration
- Intent summaries
- Flow summaries
- Entity type summaries

#### 2. `staging_[request_id].txt`
- **Original Prompt**: The analysis prompt sent to Gemini
- **Context Data**: The DialogFlow data being analyzed
- **Full Prompt**: The complete prompt + context sent to Gemini
- **Request ID**: Unique identifier for tracking
- **Timestamp**: When the request was made

#### 3. `response_[request_id].txt`
- **Gemini Response**: The complete response from the LLM
- **Request ID**: Links to the corresponding staging file
- **Timestamp**: When the response was received

#### 4. `chunk_info_[request_id].txt`
- **Chunking Information**: Details about how large data was split
- **Chunk Count**: Number of chunks created
- **Chunk Previews**: First 500 characters of each chunk

## Request IDs

Each LLM interaction gets a unique request ID for tracking:

- `puml_diagram_generation`: PlantUML diagram creation
- `flow_analysis`: Main flow analysis
- `flow_analysis_chunk_1`, `flow_analysis_chunk_2`, etc.: Chunked analysis
- `flow_analysis_combined`: Combined chunk results
- `test_intent_analysis`: Test requests

## Usage Examples

### 1. Run Full Analysis with Staging and .env

```bash
# Using .env file (recommended)
python analyzer.py Flow --output my_analysis

# Using environment variable
export GEMINI_API_KEY="your-api-key"
python analyzer.py Flow --output my_analysis

# Using command line parameter
python analyzer.py Flow --output my_analysis --api-key "your-api-key"

# Using custom .env file
python analyzer.py Flow --output my_analysis --env-file "/path/to/custom.env"
```

This will create staging files for:
- Data loading summary
- PUML diagram generation
- Flow analysis (potentially chunked)

### 2. Test Staging and .env Functionality

```bash
python test_staging.py
```

This creates a simple test to demonstrate both the staging system and .env file functionality.

### 3. Review Staging Files

After running the analyzer, check the staging directory:

```bash
ls output/staging/
cat output/staging/staging_flow_analysis.txt
cat output/staging/response_flow_analysis.txt
```

## Benefits

### For Developers
- **Debug LLM interactions**: See exactly what was sent and received
- **Optimize prompts**: Identify opportunities to improve prompt quality
- **Track performance**: Monitor how different prompts perform
- **Reproduce issues**: Use staging files to reproduce and debug problems
- **Secure API key management**: Use .env files to keep API keys out of code

### For Business Users
- **Audit AI decisions**: Review what data influenced the analysis
- **Quality assurance**: Verify the analysis is based on correct data
- **Compliance**: Keep records of AI interactions for compliance purposes
- **Transparency**: Understand how the AI arrived at its conclusions

### For Researchers
- **Data collection**: Gather examples of LLM interactions for research
- **Prompt engineering**: Test and refine prompts systematically
- **Performance analysis**: Compare different approaches and their results

## Configuration

### Environment Variables
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### .env File
```bash
# .env file
GEMINI_API_KEY=your_api_key_here
```

### Command Line Options
```bash
python analyzer.py Flow \
  --output my_analysis \
  --api-key YOUR_API_KEY \
  --env-file /path/to/custom.env \
  --verbose
```

## File Formats

### Staging File Format
```
================================================================================
DIALOGFLOW FLOW ANALYZER - STAGING FILE
================================================================================

REQUEST ID: flow_analysis
TIMESTAMP: 1703123456.789

----------------------------------------
ORIGINAL PROMPT
----------------------------------------
[Analysis prompt content]

----------------------------------------
CONTEXT DATA
----------------------------------------
[DialogFlow data content]

----------------------------------------
FULL PROMPT (SENT TO GEMINI)
----------------------------------------
[Complete prompt + context]

================================================================================
END OF STAGING FILE
================================================================================
```

### Response File Format
```
================================================================================
GEMINI RESPONSE
================================================================================

REQUEST ID: flow_analysis
TIMESTAMP: 1703123456.789

----------------------------------------
RESPONSE CONTENT
----------------------------------------
[Gemini's complete response]

================================================================================
END OF RESPONSE
================================================================================
```

## Best Practices

### 1. API Key Security
- **Never commit API keys** to version control
- **Use .env files** for local development
- **Use environment variables** in production
- **Add .env to .gitignore** to prevent accidental commits

### 2. Review Before Sending
Always check the staging files before making important LLM calls to ensure:
- Correct data is being sent
- Prompts are clear and complete
- No sensitive information is included

### 3. Monitor File Sizes
Large staging files may indicate:
- Too much context data
- Inefficient data formatting
- Need for chunking

### 4. Clean Up Regularly
Staging files can accumulate over time:
- Archive old staging files
- Delete test files
- Keep only relevant files for current analysis

### 5. Use Request IDs
Use meaningful request IDs to:
- Track specific analysis runs
- Link related files together
- Organize staging files logically

## Troubleshooting

### Common Issues

1. **Missing API Key**
   - Error: "Gemini API key is required"
   - Solution: Set `GEMINI_API_KEY` in .env file, environment variable, or command line

2. **python-dotenv not installed**
   - Warning: "python-dotenv not available"
   - Solution: `pip install python-dotenv`

3. **Large Data Chunking**
   - Staging files show chunking information
   - This is normal for large DialogFlow exports
   - Check `chunk_info_*.txt` files for details

4. **File Permission Errors**
   - Ensure write permissions to output directory
   - Check disk space availability

5. **Encoding Issues**
   - Staging files use UTF-8 encoding
   - Ensure your text editor supports UTF-8

### Debug Mode
Run with verbose logging to see detailed information:
```bash
python analyzer.py Flow --verbose
```

## Integration with Existing Workflows

The staging system is designed to be non-intrusive:
- Staging is enabled by default
- No changes to existing code required
- Staging files are created alongside normal output
- Can be disabled by setting `staging_dir=None`

## Future Enhancements

Planned improvements to the staging system:
- Web interface for reviewing staging files
- Automatic prompt optimization suggestions
- Integration with version control systems
- Advanced filtering and search capabilities
- Export to different formats (JSON, CSV, etc.)
- Enhanced .env file validation and error handling 