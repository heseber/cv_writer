# Changelog

All notable changes to the CV Optimizer project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2025-11-17

### Changed
- Updated default OpenAI model from `gpt-4o` to `gpt-5`
- Updated all documentation to reflect new default model
- Updated test cases to expect `gpt-5` as default

## [0.2.0] - 2025-11-13

### Added
- Multi-language translation support for optimized CVs
- TranslatorCrew with professional translation agent
- `--translate-to` CLI option for specifying target language
- `--translation-llm-provider` CLI option for separate translation LLM
- `--translation-llm-model` CLI option for separate translation model
- Translation configuration section in config files
- Language-specific filename generation (e.g., `cv_optimized_20251113_123456_de.md`)
- Support for any language via two-letter language codes (de, fr, es, etc.)
- Environment variable support for translation settings (`TRANSLATE_TO`, `TRANSLATION_LLM_PROVIDER`, `TRANSLATION_LLM_MODEL`)
- Translation phase in CVOptimizationFlow after optimization completes
- `save_translated_cv()` method in FileHandler for consistent naming
- Automatic timestamp matching between English and translated versions
- Ability to use different LLM for translation than for optimization

### Changed
- Updated README.md with translation examples and documentation
- Updated QUICKSTART.md with translation usage examples
- Updated IMPLEMENTATION_SUMMARY.md to reflect translation architecture
- Enhanced configuration system with translation settings
- Extended CVOptimizerState model with translation fields
- Updated project structure documentation to include translator_crew
- CVOptimizationFlow now accepts optional translation_llm parameter

### Removed
- PDF generation option for translated CVs (manual conversion preferred)
- `--translation-pdf` CLI option
- `translation.generate_pdf` configuration option

### Technical Details
- TranslatorCrew follows same pattern as ReviewerCrew and WriterCrew
- Translation preserves exact markdown formatting and structure
- Configurable LLM provider/model for translation (defaults to main LLM)
- Translation output cleaned using existing CV cleaning utilities
- Language-aware file naming: translated CV uses same basename as English with language code appended
- Respects custom filename patterns from configuration
- Fallback to main LLM if translation LLM initialization fails

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

[0.2.1]: https://github.com/heseber/cv_writer/releases/tag/v0.2.1
[0.2.0]: https://github.com/heseber/cv_writer/releases/tag/v0.2.0
[0.1.0]: https://github.com/heseber/cv_writer/releases/tag/v0.1.0

