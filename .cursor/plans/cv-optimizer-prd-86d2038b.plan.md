<!-- 86d2038b-2af1-4d6d-96e0-aee96af3c255 8c6c970c-0b9b-4474-900e-5800987ef782 -->
# Product Requirements Document: CV Optimizer Application

## 1. Executive Summary

The CV Optimizer is an AI-powered application that automatically optimizes CVs to match specific job descriptions. Built using CrewAI Flow, it employs a reviewer-writer agent loop to iteratively refine CVs until they meet quality standards or reach a maximum iteration limit.

## 2. Goals & Objectives

### Primary Goals

- Automate CV optimization to match job descriptions
- Provide actionable, critical feedback on CV content
- Generate production-ready CVs in markdown format
- Support multiple input formats and LLM providers

### Success Metrics

- CV approval rate within 3 iterations
- Quality of reviewer feedback (actionable insights)
- User satisfaction with final CV output
- System extensibility for future web/service interfaces

## 3. User Stories

**As a job seeker, I want to:**

- Upload my CV and a job description to get an optimized CV
- Choose different AI providers based on my preferences/budget
- Receive detailed feedback on what needs improvement
- Get a production-ready CV without manual editing

**As a system administrator, I want to:**

- Configure the application via config files and environment variables
- Override settings via CLI for specific runs
- Control iteration limits to manage costs
- Review the feedback history for quality assurance

## 4. Functional Requirements

### 4.1 Input Processing

**Job Description Input**

- Support two input methods:
  - File path (text, markdown, PDF)
  - URL (web scraping)
- Validate file existence and format
- Extract text content from PDFs
- Handle web scraping errors gracefully

**CV and Supporting Documents Input**

- Accept CV in text, markdown, or PDF format
- Support multiple additional documents (text, markdown, PDF)
- Parse and structure content for agent processing
- Maintain document context and organization

### 4.2 Agent System

**Reviewer Agent**

- Analyze CV against job description requirements
- Generate critical, actionable feedback
- Identify gaps, weaknesses, and improvement areas
- Make binary decision: APPROVE or REVISE
- Provide structured improvement instructions

**Writer Agent**

- Receive reviewer feedback and current CV version
- Generate improved CV in markdown format
- Address all reviewer concerns
- Maintain professional CV structure and formatting
- Incorporate candidate's expertise from supporting documents

### 4.3 Flow Architecture

**CVOptimizationFlow (CrewAI Flow)**

- State management for CV versions, feedback, and iteration count
- Router logic based on reviewer decisions
- Loop control with configurable max iterations
- Graceful exit on approval or max iterations reached

**Flow States:**

```python
- job_description: str
- cv_draft: str
- supporting_docs: List[str]
- current_cv: str
- reviewer_feedback: List[Dict]
- iteration_count: int
- max_iterations: int
- status: str (REVIEWING, REVISING, APPROVED, MAX_ITERATIONS_REACHED)
```

### 4.4 Output Generation

**Final CV Output**

- Clean markdown file with no explanations or metadata
- Professional formatting
- Filename pattern: `cv_optimized_[timestamp].md`

**Reviewer Feedback History**

- Separate markdown file with chronological feedback
- Include iteration number, decision, and detailed comments
- Filename pattern: `cv_review_history_[timestamp].md`

### 4.5 Configuration Management

**Configuration Hierarchy (lowest to highest precedence):**

1. Default values in code
2. Config file (`config/cv_optimizer.yaml`)
3. Environment variables
4. CLI arguments

**Configurable Parameters:**

- `llm_provider`: openai | anthropic | ollama
- `llm_model`: model name (provider-specific)
- `max_iterations`: default 3
- `ollama_base_url`: for local models
- `temperature`: for LLM creativity control
- `output_directory`: where to save results

**Example config file:**

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
```

### 4.6 CLI Interface

**Command Structure:**

```bash
cv-optimizer --job-description <file|url|text> \
             --cv <file> \
             [--additional-docs <file1> <file2> ...] \
             [--llm-provider <openai|anthropic|ollama>] \
             [--llm-model <model-name>] \
             [--max-iterations <number>] \
             [--config <config-file>] \
             [--output-dir <directory>]
```

**Required Arguments:**

- `--job-description` or `-j`: Job description source
- `--cv` or `-c`: CV file path

**Optional Arguments:**

- `--additional-docs` or `-a`: Supporting documents
- `--llm-provider` or `-p`: AI provider selection
- `--llm-model` or `-m`: Specific model
- `--max-iterations` or `-i`: Iteration limit
- `--config`: Config file path
- `--output-dir` or `-o`: Output directory

## 5. Technical Requirements

### 5.1 Technology Stack

**Core Framework:**

- CrewAI Flow (v1.3.0+)
- Python 3.10-3.13

**Document Processing:**

- PyPDF2 or pypdf for PDF extraction
- BeautifulSoup4 + requests for web scraping
- markdown library for markdown handling

**LLM Integration:**

- OpenAI SDK (for OpenAI)
- Anthropic SDK (for Claude)
- Ollama client (for local models)
- LiteLLM (optional: unified interface)

**Configuration:**

- PyYAML for config file parsing
- python-dotenv for environment variables
- argparse or click for CLI

**Testing:**

- pytest for unit/integration tests
- pytest-mock for mocking LLM calls

### 5.2 Architecture Components

**File Structure:**

```
src/cv_writer/
├── __init__.py
├── main.py                          # Entry point and CLI
├── flows/
│   └── cv_optimization_flow.py      # Main Flow class
├── crews/
│   ├── reviewer_crew/
│   │   ├── __init__.py
│   │   ├── reviewer_crew.py
│   │   └── config/
│   │       ├── agents.yaml
│   │       └── tasks.yaml
│   └── writer_crew/
│       ├── __init__.py
│       ├── writer_crew.py
│       └── config/
│           ├── agents.yaml
│           └── tasks.yaml
├── tools/
│   ├── __init__.py
│   ├── pdf_reader.py               # PDF extraction
│   ├── web_scraper.py              # URL content extraction
│   └── document_parser.py          # General document handling
├── config/
│   ├── __init__.py
│   ├── config_loader.py            # Configuration management
│   └── cv_optimizer.yaml           # Default config
├── models/
│   ├── __init__.py
│   └── state_models.py             # Pydantic state models
└── utils/
    ├── __init__.py
    ├── file_handler.py             # File I/O operations
    └── llm_factory.py              # LLM provider instantiation
```

### 5.3 Data Flow

**Step-by-Step Process:**

1. **Initialization**

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Parse CLI arguments
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Load configuration (file → env → CLI)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Initialize LLM provider
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Read and parse input documents

2. **Flow Start**

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Create CVOptimizationFlow instance
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Initialize state with inputs
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Set iteration counter to 0

3. **Review Phase** (ReviewerCrew)

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Analyze CV against job description
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Generate structured feedback
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Make APPROVE/REVISE decision
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Update state with feedback

4. **Routing Decision**

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - If APPROVED: → Save outputs and exit
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - If REVISE and iterations < max: → Writing phase
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - If REVISE and iterations >= max: → Save current version and exit

5. **Writing Phase** (WriterCrew)

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Receive current CV and feedback
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Generate improved CV version
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Update state with new CV
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Increment iteration counter
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - → Return to Review phase

6. **Output Generation**

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Save final CV (clean markdown)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Save feedback history (structured markdown)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                - Display summary to user

### 5.4 State Management

**CVOptimizerState (Pydantic BaseModel):**

```python
class CVOptimizerState(BaseModel):
    # Inputs
    job_description: str
    cv_draft: str
    supporting_docs: List[str] = []
    
    # Processing
    current_cv: str
    iteration_count: int = 0
    max_iterations: int = 3
    
    # Feedback tracking
    feedback_history: List[ReviewFeedback] = []
    
    # Status
    status: str = "INITIALIZED"
    final_decision: Optional[str] = None
    
class ReviewFeedback(BaseModel):
    iteration: int
    decision: str  # APPROVE | REVISE
    comments: str
    improvements_needed: List[str]
    timestamp: datetime
```

### 5.5 Error Handling

**Critical Errors (Exit with error message):**

- Invalid file paths
- Unsupported file formats
- LLM API failures (after retries)
- Invalid configuration

**Recoverable Errors (Log warning and continue):**

- PDF extraction issues (use raw text)
- Web scraping failures (prompt user for alternative)
- Missing optional supporting documents

**Validation:**

- File existence checks before processing
- Format validation for inputs
- Configuration schema validation
- LLM response structure validation

### 5.6 LLM Provider Support

**Provider Configuration:**

OpenAI:

- Environment variable: `OPENAI_API_KEY`
- Default model: `gpt-4o`

Anthropic:

- Environment variable: `ANTHROPIC_API_KEY`
- Default model: `claude-3-5-sonnet-20241022`

Ollama:

- Environment variable: `OLLAMA_BASE_URL` (default: http://localhost:11434)
- Default model: `llama3.1`
- No API key required

**LLM Factory Pattern:**

```python
def create_llm(provider: str, model: str, **kwargs):
    if provider == "openai":
        return ChatOpenAI(model=model, **kwargs)
    elif provider == "anthropic":
        return ChatAnthropic(model=model, **kwargs)
    elif provider == "ollama":
        return ChatOllama(model=model, **kwargs)
```

## 6. Agent Configurations

### 6.1 Reviewer Agent

**agents.yaml:**

```yaml
cv_reviewer:
  role: CV Optimization Reviewer
  goal: Critically assess CV alignment with job requirements and provide actionable improvement guidance
  backstory: |
    You are an experienced HR professional and recruitment specialist with 15 years of experience
    reviewing CVs for technical and professional roles. You have a keen eye for detail and understand
    what hiring managers look for in candidates. You provide honest, constructive feedback that helps
    candidates present their best selves.
  allow_delegation: false
  verbose: true
```

**tasks.yaml:**

```yaml
review_cv:
  description: |
    Review the candidate's CV against the job description and provide detailed feedback.
    
    Job Description:
    {job_description}
    
    Current CV Version:
    {current_cv}
    
    Supporting Documents:
    {supporting_docs}
    
    Iteration: {iteration_count} of {max_iterations}
    
    Analyze:
 1. Alignment with job requirements
 2. Relevant skills and experience presentation
 3. Gaps or missing information
 4. Formatting and clarity
 5. Keywords and ATS optimization
    
    Provide:
 - Specific improvement suggestions
 - Priority areas to address
 - Examples of better phrasing when applicable
    
    Make a final decision: APPROVE or REVISE
  expected_output: |
    A structured review with:
 - Decision: APPROVE or REVISE
 - Overall assessment (2-3 sentences)
 - Detailed feedback organized by category
 - Specific action items for improvement
 - Prioritized list of changes needed
```

### 6.2 Writer Agent

**agents.yaml:**

```yaml
cv_writer:
  role: Professional CV Writer
  goal: Create compelling, optimized CVs that highlight candidate strengths and match job requirements
  backstory: |
    You are a professional CV writer with expertise in crafting compelling career narratives.
    You excel at presenting candidate experience and skills in ways that resonate with hiring
    managers and pass ATS systems. You follow reviewer feedback meticulously and create
    polished, professional documents.
  allow_delegation: false
  verbose: true
```

**tasks.yaml:**

```yaml
write_cv:
  description: |
    Create an improved version of the CV based on reviewer feedback.
    
    Job Description:
    {job_description}
    
    Current CV Version:
    {current_cv}
    
    Supporting Documents:
    {supporting_docs}
    
    Reviewer Feedback:
    {latest_feedback}
    
    Requirements:
 - Address ALL points from reviewer feedback
 - Maintain professional CV formatting in markdown
 - Incorporate relevant information from supporting documents
 - Optimize for keywords from job description
 - Ensure clarity and conciseness
 - Use action verbs and quantifiable achievements
    
    Output ONLY the CV content in clean markdown format.
    Do NOT include explanations, metadata, or commentary.
  expected_output: |
    A complete, optimized CV in markdown format with:
 - Professional structure (Contact, Summary, Experience, Skills, Education)
 - Clear, concise language
 - Relevant keywords from job description
 - Quantified achievements where possible
 - No surrounding text or explanations
```

## 7. Non-Functional Requirements

### 7.1 Performance

- Processing time: < 5 minutes for 3-iteration cycle
- Support documents up to 50 pages total
- Concurrent request handling (future web service)

### 7.2 Reliability

- Graceful degradation on LLM API failures
- State persistence for long-running operations
- Retry logic for transient errors

### 7.3 Usability

- Clear CLI help documentation
- Informative progress indicators
- Detailed error messages with remediation steps
- Example usage in README

### 7.4 Maintainability

- Modular architecture for easy extension
- Comprehensive inline documentation
- Type hints throughout codebase
- Configuration-driven behavior

### 7.5 Security

- API keys via environment variables only
- No hardcoded credentials
- Input sanitization for file paths
- Secure file operations

## 8. Future Considerations

### 8.1 Web Interface

- FastAPI or Streamlit web UI
- File upload interface
- Real-time progress updates
- Session management for multiple users

### 8.2 Service Deployment

- REST API endpoints
- Authentication and authorization
- Rate limiting
- Usage tracking and analytics

### 8.3 Enhanced Features

- Multiple CV format outputs (PDF, DOCX)
- A/B testing of CV versions
- Industry-specific templates
- Multi-language support
- Integration with job boards (LinkedIn, Indeed)
- Cover letter generation

### 8.4 Quality Improvements

- Human-in-the-loop feedback option
- ML-based CV scoring
- Benchmarking against successful CVs
- Automated testing with synthetic data

## 9. Acceptance Criteria

### MVP Requirements

1. Successfully processes text, markdown, and PDF inputs
2. Completes reviewer-writer iteration loop
3. Generates clean final CV and feedback history
4. Supports all three LLM providers
5. Configuration via CLI, env vars, and config file
6. Handles errors gracefully with clear messages
7. Respects max iteration limits
8. Produces production-ready markdown CVs

### Quality Standards

- Code coverage > 80%
- Type checking with mypy passes
- Linting with ruff passes
- All functional tests pass
- Documentation complete and accurate

## 10. Implementation Phases

### Phase 1: Core Infrastructure (Week 1)

- Document parsing tools (PDF, web scraping)
- Configuration system
- LLM factory and provider support
- Basic Flow structure

### Phase 2: Agent Development (Week 2)

- Reviewer agent and crew
- Writer agent and crew
- Agent configurations and prompts
- State management models

### Phase 3: Flow Implementation (Week 3)

- Complete CVOptimizationFlow
- Routing logic
- Iteration control
- Output generation

### Phase 4: CLI and Integration (Week 4)

- CLI argument parsing
- End-to-end flow execution
- Error handling
- Testing and validation

### Phase 5: Documentation and Polish (Week 5)

- User documentation
- Code documentation
- Example runs
- Performance optimization

## 11. Dependencies

### Python Packages

```toml
dependencies = [
    "crewai[tools]>=1.3.0",
    "pydantic>=2.0.0",
    "pyyaml>=6.0",
    "python-dotenv>=1.0.0",
    "pypdf>=3.0.0",
    "beautifulsoup4>=4.12.0",
    "requests>=2.31.0",
    "click>=8.1.0",
    "langchain-openai>=0.1.0",
    "langchain-anthropic>=0.1.0",
    "langchain-ollama>=0.1.0",
]
```

## 12. Risks and Mitigations

| Risk | Impact | Mitigation |

|------|--------|------------|

| LLM API costs exceed budget | High | Implement iteration limits, caching, local model option |

| PDF extraction unreliable | Medium | Multiple extraction libraries, fallback to text input |

| Reviewer never approves | High | Hard max iteration limit, quality threshold tuning |

| Poor CV quality output | High | Extensive prompt engineering, human validation phase |

| Web scraping blocked | Low | User-agent rotation, alternative input methods |

## 13. Success Metrics (Post-Launch)

- 80%+ of CVs approved within 3 iterations
- User satisfaction score > 4.5/5
- 50%+ adoption of local LLM option
- Zero critical bugs in first month
- Extension to web interface within 3 months

---

**Document Version:** 1.0

**Last Updated:** November 12, 2025

**Status:** Ready for Implementation

### To-dos

- [ ] Set up core infrastructure including document parsing tools, configuration system, and LLM factory
- [ ] Create Pydantic state models for CVOptimizerState and ReviewFeedback
- [ ] Implement reviewer crew with agent configuration and review task
- [ ] Implement writer crew with agent configuration and writing task
- [ ] Build CVOptimizationFlow with routing logic and iteration control
- [ ] Create CLI interface with argument parsing and configuration hierarchy
- [ ] Implement output generation for final CV and feedback history
- [ ] Write comprehensive tests and perform end-to-end validation
- [ ] Complete user documentation, README, and usage examples