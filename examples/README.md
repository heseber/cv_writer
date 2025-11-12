# CV Optimizer Examples

This directory contains example files to help you get started with CV Optimizer.

## Files

### example_job_description.txt
A sample job posting for a Senior Software Engineer position. This demonstrates the type of job description you can provide to the optimizer.

### example_cv_draft.md
A basic CV that needs improvement. This serves as an example of input CV that would benefit from optimization.

## Usage

To test the CV optimizer with these examples:

```bash
# Basic optimization
cv-optimizer \
  --job-description examples/example_job_description.txt \
  --cv examples/example_cv_draft.md

# With more iterations
cv-optimizer \
  --job-description examples/example_job_description.txt \
  --cv examples/example_cv_draft.md \
  --max-iterations 5

# With custom output directory
cv-optimizer \
  --job-description examples/example_job_description.txt \
  --cv examples/example_cv_draft.md \
  --output-dir ./my_results
```

## What to Expect

The optimizer will:
1. Analyze the job description requirements
2. Review the CV against those requirements
3. Provide detailed feedback on improvements needed
4. Generate an optimized version addressing the feedback
5. Continue iterating until approved or max iterations reached

## Output

You'll receive:
- `cv_optimized_[timestamp].md` - The final optimized CV
- `cv_review_history_[timestamp].md` - Detailed feedback from each iteration

## Tips

- Provide additional documents (certifications, portfolios) using `--additional-docs`
- Increase iterations for more refinement
- Review the feedback history to understand the changes
- Use the optimized CV as a starting point and add personal touches

