# Quick Start Guide

Get started with CV Optimizer in 5 minutes!

## Step 1: Install

```bash
# Clone or navigate to the project directory
cd cv_writer

# Install dependencies
pip install -e .
```

## Step 2: Set Up API Key

Create a `.env` file in the project root:

```bash
# For OpenAI (easiest to start with)
OPENAI_API_KEY=sk-your-key-here
```

Get your API key from: https://platform.openai.com/api-keys

## Step 3: Prepare Your Files

You need two files:
1. **Job Description** - The job you're applying for
2. **Your CV** - Your current CV in text, markdown, or PDF format

**Tip**: Use the example files to test first!

## Step 4: Run the Optimizer

### Try with Examples First

```bash
cv-optimizer \
  --job-description examples/example_job_description.txt \
  --cv examples/example_cv_draft.md
```

### Use Your Own Files

```bash
cv-optimizer \
  --job-description path/to/job_description.txt \
  --cv path/to/your_cv.pdf
```

### From a Job Posting URL

```bash
cv-optimizer \
  --job-description https://example.com/job-posting \
  --cv your_cv.md
```

## Step 5: Check Results

Find your optimized CV in the `output/` directory:
- `cv_optimized_[timestamp].md` - Your improved CV
- `cv_review_history_[timestamp].md` - Detailed feedback

## Next Steps

### Add Supporting Documents

```bash
cv-optimizer \
  --job-description job.txt \
  --cv cv.md \
  --additional-docs portfolio.pdf \
  --additional-docs certifications.md
```

### Increase Iterations

```bash
cv-optimizer \
  --job-description job.txt \
  --cv cv.md \
  --max-iterations 5
```

### Use Different LLM Provider

```bash
# Anthropic Claude
export ANTHROPIC_API_KEY=your-key
cv-optimizer --job-description job.txt --cv cv.md --llm-provider anthropic

# Local Ollama (free!)
ollama serve  # In another terminal
cv-optimizer --job-description job.txt --cv cv.md --llm-provider ollama
```

## Common Issues

**"OPENAI_API_KEY not set"**
- Check your `.env` file exists
- Make sure the key starts with `sk-`
- Try: `export OPENAI_API_KEY=your-key`

**"Failed to extract text from PDF"**
- Some PDFs don't extract well
- Convert to text or markdown first
- Use an online PDF to text converter

**"Max iterations reached"**
- Normal! Review the feedback
- Increase with `--max-iterations 5`
- The CV is still improved even if not "approved"

## Tips for Best Results

1. **Be Specific**: Use the exact job posting, not a generic description
2. **Add Context**: Include portfolios, certificates as additional docs
3. **Iterate**: Start with 3 iterations, increase if needed
4. **Review Feedback**: Check the feedback history to understand changes
5. **Personalize**: Use the output as a base, add your personal touch

## Get Help

- See full docs: [README.md](README.md)
- Check examples: [examples/](examples/)
- View configuration: [src/cv_writer/config/cv_optimizer.yaml](src/cv_writer/config/cv_optimizer.yaml)

## What's Happening?

1. **Reviewer** analyzes your CV against the job requirements
2. **Writer** improves your CV based on feedback
3. This repeats until CV is approved or max iterations reached
4. You get a polished, job-specific CV!

---

Ready? Run your first optimization now! 🚀

```bash
cv-optimizer \
  --job-description examples/example_job_description.txt \
  --cv examples/example_cv_draft.md
```

