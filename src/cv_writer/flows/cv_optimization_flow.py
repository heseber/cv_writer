"""CV Optimization Flow using CrewAI Flow."""

import re
from datetime import datetime
from typing import Any

from crewai.flow import Flow, listen, or_, router, start

from cv_writer.crews.reviewer_crew import ReviewerCrew
from cv_writer.crews.translator_crew import TranslatorCrew
from cv_writer.crews.writer_crew import WriterCrew
from cv_writer.models.state_models import CVOptimizerState, ReviewFeedback


class CVOptimizationFlow(Flow[CVOptimizerState]):
    """Flow for iterative CV optimization."""

    def __init__(self, llm: Any, translation_llm: Any | None = None):
        """
        Initialize CV Optimization Flow.

        Args:
            llm: Language model instance for optimization
            translation_llm: Optional separate LLM for translation (uses main LLM if None)
        """
        super().__init__()
        self.llm = llm
        self.translation_llm = translation_llm or llm

    @start()
    def initialize_flow(self):
        """Initialize the flow and prepare the first CV version."""
        print(f"\n{'=' * 80}")
        print("CV OPTIMIZATION FLOW - STARTING")
        print(f"{'=' * 80}\n")
        print(f"Job Description length: {len(self.state.job_description)} characters")
        print(f"CV Draft length: {len(self.state.cv_draft)} characters")
        print(f"Supporting Documents: {len(self.state.supporting_docs)}")
        print(f"Max Iterations: {self.state.max_iterations}\n")

        # Initialize current_cv with the draft
        self.state.current_cv = self.state.cv_draft
        self.state.status = "REVIEWING"

    @listen("decision_to_revise")
    def revise_cv(self):
        """Revise the CV based on reviewer feedback."""
        print(f"\n{'=' * 80}")
        print(f"ITERATION {self.state.iteration_count} - WRITING PHASE")
        print(f"{'=' * 80}\n")

        # Get latest feedback
        latest_feedback = self.state.feedback_history[-1].comments

        # Prepare supporting docs text
        supporting_docs_text = self._format_supporting_docs()

        # Run writer crew
        result = (
            WriterCrew(self.llm)
            .crew()
            .kickoff(
                inputs={
                    "job_description": self.state.job_description,
                    "current_cv": self.state.current_cv,
                    "supporting_docs": supporting_docs_text,
                    "latest_feedback": latest_feedback,
                }
            )
        )

        revised_cv = result.raw if hasattr(result, "raw") else str(result)

        # Clean up the CV (remove any markdown code blocks if present)
        revised_cv = self._clean_cv_output(revised_cv)

        # Update state
        self.state.current_cv = revised_cv

        print(f"\nRevised CV length: {len(revised_cv)} characters")
        print(f"Completed iteration {self.state.iteration_count}\n")

        # Loop back to review
        self.state.status = "REVIEWING"

    @listen(or_(initialize_flow, revise_cv))
    def review_cv(self):
        """Review the current CV version."""

        # Increment iteration count
        self.state.iteration_count += 1

        print(f"\n{'=' * 80}")
        print(f"ITERATION {self.state.iteration_count} - REVIEW PHASE")
        print(f"{'=' * 80}\n")

        # Prepare supporting docs text
        supporting_docs_text = self._format_supporting_docs()

        # Run reviewer crew
        result = (
            ReviewerCrew(self.llm)
            .crew()
            .kickoff(
                inputs={
                    "job_description": self.state.job_description,
                    "current_cv": self.state.current_cv,
                    "supporting_docs": supporting_docs_text,
                    "iteration_count": self.state.iteration_count,
                    "max_iterations": self.state.max_iterations,
                }
            )
        )

        review_output = result.raw if hasattr(result, "raw") else str(result)

        # Parse the review to check if approved
        review_upper = review_output.upper()
        if "DECISION: APPROVED" in review_upper or "DECISION:APPROVED" in review_upper:
            decision = "APPROVED"
            comments = review_output
            print("✅ Draft APPROVED by reviewer!")
        else:
            decision = "REVISE"
            comments = (
                f"Based on the review, please improve the draft:\n\n{review_output}"
            )
            print("⚠️  Draft needs improvement. Feedback provided for next iteration.")

        # Create feedback object
        feedback = ReviewFeedback(
            iteration=self.state.iteration_count,
            decision=decision,
            comments=comments,
            timestamp=datetime.now(),
        )

        # Add to history
        self.state.feedback_history.append(feedback)

        print(f"\nReviewer Decision: {decision}")
        print(f"Feedback length: {len(review_output)} characters\n")

        # Store decision for routing
        self.state.final_decision = decision

    @router(review_cv)
    def route_decision(self):
        """
        Route based on reviewer decision.

        Returns:
            Next method to execute
        """
        decision = self.state.final_decision

        # Check if approved
        if decision == "APPROVED":
            print(f"\n{'=' * 80}")
            print("CV APPROVED - Flow Complete")
            print(f"{'=' * 80}\n")
            self.state.status = "APPROVED"
            return "decision_to_finalize"

        # Check if max iterations reached
        if self.state.iteration_count >= self.state.max_iterations:
            print(f"\n{'=' * 80}")
            print("MAX ITERATIONS REACHED - Flow Complete")
            print(f"{'=' * 80}\n")
            self.state.status = "MAX_ITERATIONS_REACHED"
            return "decision_to_finalize"

        # Continue to revision
        print("\nContinuing to revision phase...")
        self.state.status = "REVISING"
        return "decision_to_revise"

    @listen("decision_to_finalize")
    def complete_flow(self):
        """Complete the optimization phase."""
        print(f"\n{'=' * 80}")
        print("CV OPTIMIZATION COMPLETE")
        print(f"{'=' * 80}\n")
        print(f"Final Status: {self.state.status}")
        print(f"Total Iterations: {self.state.iteration_count}")
        print(f"Total Feedback Entries: {len(self.state.feedback_history)}\n")

    @router(complete_flow)
    def route_translation(self):
        """
        Route based on translation requirement.

        Returns:
            Next method to execute or None to end flow
        """
        if self.state.translate_to:
            print(f"\nTranslation requested to {self.state.translate_to.upper()}...")
            return "decision_to_translate"
        else:
            print("\nNo translation requested. Flow complete.")
            return "decision_to_end"

    @listen("decision_to_translate")
    def translate_cv(self):
        """Translate the final CV to the target language."""
        print(f"\n{'=' * 80}")
        print(f"TRANSLATION PHASE - Translating to {self.state.translate_to.upper()}")
        print(f"{'=' * 80}\n")

        # Run translator crew with appropriate LLM
        result = (
            TranslatorCrew(self.translation_llm)
            .crew()
            .kickoff(
                inputs={
                    "cv_content": self.state.current_cv,
                    "target_language": self.state.translate_to,
                }
            )
        )

        translated_cv = result.raw if hasattr(result, "raw") else str(result)

        # Clean up the translated CV
        translated_cv = self._clean_cv_output(translated_cv)

        # Update state
        self.state.translated_cv = translated_cv

        print(f"\nTranslated CV length: {len(translated_cv)} characters")
        print(f"Translation to {self.state.translate_to.upper()} complete\n")

    @listen(or_("decision_to_translate", "decision_to_end"))
    def finalize_flow(self):
        """Final cleanup and flow termination."""
        print(f"\n{'=' * 80}")
        print("FLOW FINALIZED")
        print(f"{'=' * 80}\n")

    def _format_supporting_docs(self) -> str:
        """
        Format supporting documents for display.

        Returns:
            Formatted supporting documents text
        """
        if self.state.supporting_docs:
            return "\n\n".join(
                f"Document {i + 1}:\n{doc}"
                for i, doc in enumerate(self.state.supporting_docs)
            )
        return "No additional documents provided."

    @staticmethod
    def _clean_cv_output(cv_text: str) -> str:
        """
        Clean CV output to remove any markdown code blocks or extra formatting.

        Args:
            cv_text: Raw CV text

        Returns:
            Cleaned CV text
        """
        # Remove markdown code blocks
        cv_text = re.sub(r"```markdown\s*", "", cv_text)
        cv_text = re.sub(r"```\s*$", "", cv_text, flags=re.MULTILINE)
        cv_text = re.sub(r"```", "", cv_text)

        # Remove any leading/trailing "Here is" type phrases
        cv_text = re.sub(
            r"^(Here is|Here's|Below is|The following is).*?CV:?\s*",
            "",
            cv_text,
            flags=re.IGNORECASE | re.MULTILINE,
        )

        # Ensure lists are surrounded by blank lines
        lines = cv_text.split("\n")
        result_lines = []
        in_list = False

        for line in lines:
            # Check if this is a list item (line starting with dash)
            is_list_item = line.strip().startswith("-") and len(line.strip()) > 1

            if is_list_item:
                if not in_list:
                    # Starting a new list
                    # Add blank line before if previous line has content
                    if result_lines and result_lines[-1].strip() != "":
                        result_lines.append("")
                    in_list = True
                # Remove trailing whitespace from list items
                result_lines.append(line.rstrip())
            else:
                if in_list:
                    # Just ended a list
                    # Add blank line after if current line has content
                    if line.strip() != "":
                        result_lines.append("")
                    in_list = False
                result_lines.append(line)

        return "\n".join(result_lines).strip()
