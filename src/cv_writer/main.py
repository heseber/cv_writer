"""Main entry point for CV Optimizer CLI."""

import sys

import click

from cv_writer.config import Config
from cv_writer.flows import CVOptimizationFlow
from cv_writer.tools import DocumentParser
from cv_writer.utils import FileHandler, LLMFactory


@click.command()
@click.option(
    "--job-description",
    "-j",
    required=True,
    help="Job description source (file path or URL)",
)
@click.option(
    "--cv",
    "-c",
    required=True,
    help="CV file path",
)
@click.option(
    "--additional-docs",
    "-a",
    multiple=True,
    help="Additional supporting documents (can be specified multiple times)",
)
@click.option(
    "--llm-provider",
    "-p",
    type=click.Choice(["openai", "anthropic", "ollama"], case_sensitive=False),
    help="LLM provider (openai, anthropic, ollama)",
)
@click.option(
    "--llm-model",
    "-m",
    help="Specific LLM model name",
)
@click.option(
    "--max-iterations",
    "-i",
    type=int,
    help="Maximum number of iterations",
)
@click.option(
    "--config",
    type=click.Path(exists=True),
    help="Path to config file",
)
@click.option(
    "--output-dir",
    "-o",
    help="Output directory for results",
)
def main(
    job_description: str,
    cv: str,
    additional_docs: tuple,
    llm_provider: str | None,
    llm_model: str | None,
    max_iterations: int | None,
    config: str | None,
    output_dir: str | None,
):
    """
    CV Optimizer - Optimize your CV for specific job descriptions.

    This tool uses AI to iteratively improve your CV based on job requirements.
    """
    try:
        # Load configuration
        cfg = Config(config_file=config)

        # Override with CLI arguments
        if llm_provider:
            cfg.set("llm.provider", llm_provider)
        if llm_model:
            cfg.set("llm.model", llm_model)
        if max_iterations:
            cfg.set("optimizer.max_iterations", max_iterations)
        if output_dir:
            cfg.set("output.directory", output_dir)

        # Display configuration
        print("\n" + "=" * 80)
        print("CV OPTIMIZER - Configuration")
        print("=" * 80)
        print(f"LLM Provider: {cfg.llm_provider}")
        print(f"LLM Model: {cfg.llm_model}")
        print(f"Max Iterations: {cfg.max_iterations}")
        print(f"Output Directory: {cfg.output_directory}")
        print("=" * 80 + "\n")

        # Parse job description
        print("Loading job description...")
        try:
            job_desc_text = DocumentParser.parse_source(job_description)
            print(f"✅ Job description loaded ({len(job_desc_text)} characters)\n")
        except Exception as e:
            raise click.ClickException(
                f"Failed to load job description: {str(e)}"
            ) from e

        # Parse CV
        print("Loading CV...")
        try:
            cv_text = DocumentParser.parse_file(cv)
            print(f"✅ CV loaded ({len(cv_text)} characters)\n")
        except Exception as e:
            raise click.ClickException(f"Failed to load CV: {str(e)}") from e

        # Parse additional documents
        supporting_docs = []
        if additional_docs:
            print(f"Loading {len(additional_docs)} additional document(s)...")
            try:
                supporting_docs = DocumentParser.parse_multiple_files(
                    list(additional_docs)
                )
                print("✅ All documents loaded\n")
            except Exception as e:
                raise click.ClickException(
                    f"Failed to load additional documents: {str(e)}"
                ) from e

        # Create LLM instance
        print("Initializing LLM...")
        try:
            llm = LLMFactory.create_llm(
                provider=cfg.llm_provider,
                model=cfg.llm_model,
                temperature=cfg.llm_temperature,
            )
            print("✅ LLM initialized\n")
        except Exception as e:
            raise click.ClickException(f"Failed to initialize LLM: {str(e)}") from e

        # Run optimization flow
        flow = CVOptimizationFlow(llm)

        # Initialize state with inputs
        flow.state.job_description = job_desc_text
        flow.state.cv_draft = cv_text
        flow.state.supporting_docs = supporting_docs
        flow.state.max_iterations = cfg.max_iterations

        # Run the flow
        flow.kickoff()

        # Save outputs
        print("\n" + "=" * 80)
        print("SAVING OUTPUTS")
        print("=" * 80 + "\n")

        # Save final CV
        cv_path = FileHandler.save_cv(
            cv_content=flow.state.current_cv,
            output_dir=cfg.output_directory,
            filename_pattern=cfg.cv_filename_pattern,
        )
        print(f"✅ Final CV saved: {cv_path}")

        # Save feedback history
        feedback_content = FileHandler.format_feedback_history(
            flow.state.feedback_history
        )
        feedback_path = FileHandler.save_feedback_history(
            feedback_content=feedback_content,
            output_dir=cfg.output_directory,
            filename_pattern=cfg.feedback_filename_pattern,
        )
        print(f"✅ Feedback history saved: {feedback_path}")

        # Display summary
        print("\n" + "=" * 80)
        print("OPTIMIZATION SUMMARY")
        print("=" * 80)
        print(f"Status: {flow.state.status}")
        print(f"Iterations Completed: {flow.state.iteration_count}")
        print(f"Final Decision: {flow.state.final_decision or 'N/A'}")
        print(f"Output Directory: {cfg.output_directory}")
        print("=" * 80 + "\n")

        if flow.state.status == "APPROVED":
            print("✅ CV was approved by the reviewer!")
        elif flow.state.status == "MAX_ITERATIONS_REACHED":
            print(
                "⚠️ Maximum iterations reached. Consider running again with more iterations."
            )

        print("\nThank you for using CV Optimizer!\n")

    except click.ClickException:
        raise
    except KeyboardInterrupt:
        print("\n\n⚠️ Optimization interrupted by user.")
        sys.exit(1)
    except Exception as e:
        raise click.ClickException(f"❌ An error occurred: {str(e)}") from e


def plot():
    """Plot the CV Optimization Flow diagram."""
    try:
        # Create a dummy LLM for plotting
        from cv_writer.utils import LLMFactory

        llm = LLMFactory.create_llm("openai", "gpt-4o", temperature=0.7)

        flow = CVOptimizationFlow(llm)
        flow.plot()
    except Exception as e:
        print(f"Error plotting flow: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
