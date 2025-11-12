# Changelog

All notable changes to the CV Optimizer project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-12

### Added
- Initial release of CV Optimizer
- CrewAI Flow-based architecture for iterative CV optimization
- Reviewer agent for critical CV assessment
- Writer agent for CV improvement
- Support for multiple input formats (text, markdown, PDF)
- Web scraping for job descriptions from URLs
- Multi-LLM support (OpenAI, Anthropic, Ollama)
- Hierarchical configuration system (defaults, config file, env vars, CLI)
- CLI interface with comprehensive options
- Automatic output generation (optimized CV + feedback history)
- Document parsing tools for various formats
- LLM factory pattern for provider flexibility
- Comprehensive test suite
- Full documentation and examples
- Example job description and CV files

### Features
- Iterative optimization with configurable max iterations
- Detailed feedback history tracking
- Clean markdown output without metadata
- Support for additional supporting documents
- Progress indicators and status reporting
- Error handling and validation
- Configuration via YAML files and environment variables

### Technical Details
- Python 3.10-3.13 support
- Pydantic-based state management
- Type hints throughout codebase
- Modular architecture for extensibility
- Integration with langchain for LLM abstraction
- Click-based CLI framework
- Pytest-based testing infrastructure

### Documentation
- Comprehensive README with usage examples
- Configuration reference
- Troubleshooting guide
- Example files for quick start
- Inline code documentation
- Test coverage documentation

[0.1.0]: https://github.com/yourusername/cv_writer/releases/tag/v0.1.0

