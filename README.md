# CV Optimizer

AI-powered CV optimization using CrewAI Flow. This application uses AI agents to iteratively improve your CV to match specific job descriptions.

## Features

- **Iterative Optimization**: AI reviewer and writer agents work together to improve your CV
- **Multiple Input Formats**: Support for text, markdown, and PDF files
- **Web Scraping**: Extract job descriptions directly from URLs
- **Multi-LLM Support**: Works with OpenAI, Anthropic, and Ollama (local models)
- **Multi-Language Translation**: Translate your optimized CV to any language (German, French, Spanish, etc.)
- **Flexible Configuration**: Configure via files, environment variables, or CLI arguments
- **Detailed Feedback**: Get comprehensive feedback history for all iterations
- **Production Ready**: Clean, professional markdown output

## Installation

### Prerequisites

- Python 3.10 or higher (< 3.14)
- pip or uv package manager

### Install Dependencies

```bash
# Using pip
pip install -e .

# Or using uv (recommended)
uv pip install -e .
```

## Quick Start

### 1. Set Up API Keys

Create a `.env` file in the project root:

```bash
# For OpenAI (default)
OPENAI_API_KEY=your_openai_api_key_here

# For Anthropic
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# For Ollama (optional, defaults to localhost)
OLLAMA_BASE_URL=http://localhost:11434
```

### 2. Run the Optimizer

Basic usage:

```bash
cv-optimizer --job-description job.txt --cv my_cv.md
```

With additional options:

```bash
cv-optimizer \
  --job-description https://example.com/job-posting \
  --cv my_cv.pdf \
  --additional-docs portfolio.pdf \
  --additional-docs certifications.md \
  --llm-provider openai \
  --max-iterations 5 \
  --output-dir ./results
```

## Usage

### Command Line Options

#### Required Arguments

- `--job-description`, `-j`: Job description source (file path or URL)
- `--cv`, `-c`: Path to your CV file

#### Optional Arguments

- `--additional-docs`, `-a`: Additional supporting documents (can be used multiple times)
- `--llm-provider`, `-p`: LLM provider (openai, anthropic, ollama)
- `--llm-model`, `-m`: Specific model name
- `--max-iterations`, `-i`: Maximum number of iterations (default: 3)
- `--config`: Path to custom config file
- `--output-dir`, `-o`: Output directory for results
- `--translate-to`, `-t`: Target language code for translation (e.g., 'de', 'fr', 'es')
- `--translation-llm-provider`: LLM provider for translation (if different from main)
- `--translation-llm-model`: LLM model for translation (if different from main)

### Supported File Formats

#### Input Files
- **Text**: `.txt`
- **Markdown**: `.md`, `.markdown`
- **PDF**: `.pdf`

#### Job Description Sources
- Local files (text, markdown, PDF)
- URLs (web scraping)

### Configuration

Configuration follows a hierarchy (lowest to highest precedence):

1. Default values
2. Config file (`src/cv_writer/config/cv_optimizer.yaml`)
3. Environment variables
4. CLI arguments

#### Config File Example

Create a custom config file:

```yaml
llm:
  provider: openai
  model: gpt-4o
  temperature: 0.7

optimizer:
  max_iterations: 3
  save_intermediate_versions: false

output:
  directory: ./output
  cv_filename_pattern: "cv_optimized_{timestamp}.md"
  feedback_filename_pattern: "cv_review_history_{timestamp}.md"

translation:
  enabled: false
  target_language: null
  llm_provider: null  # Uses main LLM if not specified
  llm_model: null     # Uses main LLM if not specified
```

Use it:

```bash
cv-optimizer --config my_config.yaml --job-description job.txt --cv cv.md
```

#### Environment Variables

Override configuration with environment variables:

```bash
export LLM_PROVIDER=anthropic
export LLM_MODEL=claude-3-5-sonnet-20241022
export MAX_ITERATIONS=5
export OUTPUT_DIRECTORY=./my_output

cv-optimizer --job-description job.txt --cv cv.md
```

#### Translation Environment Variables

```bash
# Enable translation with environment variables
export TRANSLATE_TO=de
export TRANSLATION_LLM_PROVIDER=ollama
export TRANSLATION_LLM_MODEL=llama3.1

cv-optimizer --job-description job.txt --cv cv.md
```

## How It Works

### The Optimization Flow

1. **Initialization**
   - Parse job description and CV
   - Load supporting documents
   - Initialize LLM and configuration

2. **Review Phase**
   - Reviewer agent analyzes CV against job requirements
   - Provides detailed, actionable feedback
   - Makes APPROVE or REVISE decision

3. **Routing Decision**
   - If APPROVED: Save outputs and complete
   - If REVISE and iterations < max: Continue to writing
   - If max iterations reached: Save current version

4. **Writing Phase**
   - Writer agent creates improved CV version
   - Addresses all reviewer feedback
   - Incorporates information from supporting documents
   - Returns to review phase

5. **Output Generation**
   - Save final optimized CV (clean markdown)
   - Save feedback history with all iterations

### Agent Roles

#### Reviewer Agent
- Experienced HR professional persona
- Critically assesses CV alignment with job requirements
- Provides structured, actionable feedback
- Makes binary APPROVE/REVISE decisions

#### Writer Agent
- Professional CV writer persona
- Creates compelling career narratives
- Follows reviewer feedback meticulously
- Optimizes for ATS and human readers

#### Translator Agent
- Professional translator specializing in career documents
- Translates CVs while preserving formatting and impact
- Adapts terminology for target language markets
- Maintains exact markdown structure

## Output

The application generates the following files:

1. **Optimized CV** (`cv_optimized_[timestamp].md`)
   - Clean markdown format
   - No explanations or metadata
   - Production-ready document

2. **Translated CV** (`[basename]_[language].md`) - *Optional*
   - Appears only when `--translate-to` is specified
   - Uses the same basename as English version with language code appended
   - Language code suffix (e.g., `cv_optimized_20251113_123456_de.md`)
   - Preserves exact formatting of original

3. **Feedback History** (`cv_review_history_[timestamp].md`)
   - Chronological feedback from all iterations
   - Reviewer decisions and comments
   - Improvement suggestions
   - Timestamps for each iteration

## Examples

### Example 1: Basic Usage with OpenAI

```bash
export OPENAI_API_KEY=your_key_here

cv-optimizer \
  --job-description job_posting.txt \
  --cv my_cv.md
```

### Example 2: Using Anthropic with Additional Documents

```bash
export ANTHROPIC_API_KEY=your_key_here

cv-optimizer \
  --job-description https://example.com/job \
  --cv cv.pdf \
  --additional-docs portfolio.md \
  --additional-docs certifications.pdf \
  --llm-provider anthropic \
  --max-iterations 5
```

### Example 3: Using Local Ollama Model

```bash
# Start Ollama server first
# ollama serve

cv-optimizer \
  --job-description job.txt \
  --cv cv.md \
  --llm-provider ollama \
  --llm-model llama3.1 \
  --max-iterations 3
```

### Example 4: Translation to German

```bash
export OPENAI_API_KEY=your_key_here

cv-optimizer \
  --job-description job.txt \
  --cv cv.md \
  --translate-to de
```

### Example 5: Translation with Different LLM

```bash
# Use Claude for translation while using GPT-4 for optimization
cv-optimizer \
  --job-description job.txt \
  --cv cv.md \
  --llm-provider openai \
  --translate-to de \
  --translation-llm-provider anthropic \
  --translation-llm-model claude-3-5-sonnet-20241022

# Use local Ollama model for translation to save costs
cv-optimizer \
  --job-description job.txt \
  --cv cv.md \
  --translate-to fr \
  --translation-llm-provider ollama \
  --translation-llm-model llama3.1
```

### Example 6: Custom Configuration

```bash
cv-optimizer \
  --config my_config.yaml \
  --job-description job.md \
  --cv cv.md \
  --output-dir ./custom_output \
  --max-iterations 4
```

## Development

### Project Structure

```
cv_writer/
├── src/cv_writer/
│   ├── __init__.py
│   ├── main.py                      # CLI entry point
│   ├── config/
│   │   ├── config_loader.py         # Configuration management
│   │   └── cv_optimizer.yaml        # Default config
│   ├── crews/
│   │   ├── reviewer_crew/           # Reviewer agent & tasks
│   │   ├── translator_crew/         # Translator agent & tasks
│   │   └── writer_crew/             # Writer agent & tasks
│   ├── flows/
│   │   └── cv_optimization_flow.py  # Main optimization flow
│   ├── models/
│   │   └── state_models.py          # Pydantic state models
│   ├── tools/
│   │   ├── document_parser.py       # Document processing
│   │   ├── pdf_reader.py            # PDF extraction
│   │   └── web_scraper.py           # Web scraping
│   └── utils/
│       ├── file_handler.py          # File I/O operations
│       └── llm_factory.py           # LLM instantiation
├── tests/                           # Unit tests
├── pyproject.toml                   # Project dependencies
└── README.md                        # This file
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-mock

# Run tests
pytest tests/

# Run with coverage
pytest --cov=cv_writer tests/
```

### Visualizing the Flow

Generate a flow diagram:

```bash
python -m cv_writer.main plot
```

## Configuration Reference

### LLM Providers

#### OpenAI
- **Provider**: `openai`
- **Default Model**: `gpt-4o`
- **Environment Variable**: `OPENAI_API_KEY`
- **Other Models**: `gpt-4`, `gpt-3.5-turbo`, etc.

#### Anthropic
- **Provider**: `anthropic`
- **Default Model**: `claude-3-5-sonnet-20241022`
- **Environment Variable**: `ANTHROPIC_API_KEY`
- **Other Models**: `claude-3-opus-20240229`, etc.

#### Ollama
- **Provider**: `ollama`
- **Default Model**: `llama3.1`
- **Environment Variable**: `OLLAMA_BASE_URL` (optional)
- **Other Models**: `llama2`, `mistral`, `codellama`, etc.
- **Note**: Requires Ollama server running locally

### Parameters

- **max_iterations**: Number of review-revise cycles (default: 3)
- **temperature**: LLM creativity (0.0-1.0, default: 0.7)
- **output_directory**: Where to save results (default: ./output)

## Troubleshooting

### Common Issues

#### "OPENAI_API_KEY environment variable not set"
- Ensure you've created a `.env` file with your API key
- Or export the variable: `export OPENAI_API_KEY=your_key`

#### "Failed to extract text from PDF"
- Ensure pypdf is installed: `pip install pypdf`
- Some PDFs may have image-based text (not supported)
- Try converting to text or markdown first

#### "Failed to fetch URL"
- Check your internet connection
- Some websites block scraping
- Try saving the job description to a file instead

#### "Max iterations reached"
- Increase iterations: `--max-iterations 5`
- Review feedback history to understand issues
- Consider manually incorporating feedback

## Future Enhancements

- Web-based user interface
- Multiple output formats (DOCX)
- Cover letter generation
- A/B testing of CV versions
- Industry-specific templates
- Integration with job boards
- Batch translation to multiple languages simultaneously

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please ensure:
- Code follows existing style
- Tests are included
- Documentation is updated
- Type hints are used

## Support

For issues, questions, or contributions:
1. Check existing documentation
2. Review troubleshooting section
3. Open an issue with detailed information

## Credits

Built with:
- [CrewAI](https://www.crewai.com/) - Multi-agent framework
- [LangChain](https://www.langchain.com/) - LLM integrations
- [Click](https://click.palletsprojects.com/) - CLI framework
- [Pydantic](https://docs.pydantic.dev/) - Data validation

---

**Version**: 0.2.0  
**Status**: Production Ready  
**Python**: 3.10-3.13
