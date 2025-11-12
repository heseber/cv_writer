"""CV Optimization Flow using CrewAI Flow."""

import re
from datetime import datetime
from typing import Any

from crewai.flow import Flow, listen, router, start
from pydantic import BaseModel

from cv_writer.crews.reviewer_crew import ReviewerCrew
from cv_writer.crews.writer_crew import WriterCrew
from cv_writer.models.state_models import CVOptimizerState, ReviewFeedback


class CVOptimizationFlow(Flow[CVOptimizerState]):
    """Flow for iterative CV optimization."""

    def __init__(self, llm: Any):
        """
        Initialize CV Optimization Flow.

        Args:
            llm: Language model instance
        """
        super().__init__()
        self.llm = llm
        self.reviewer_crew = ReviewerCrew(llm)
        self.writer_crew = WriterCrew(llm)

    @start()
    def initialize_flow(self):
        """Initialize the flow and prepare the first CV version."""
        print(f"\n{'='*80}")
        print("CV OPTIMIZATION FLOW - STARTING")
        print(f"{'='*80}\n")
        print(f"Job Description length: {len(self.state.job_description)} characters")
        print(f"CV Draft length: {len(self.state.cv_draft)} characters")
        print(f"Supporting Documents: {len(self.state.supporting_docs)}")
        print(f"Max Iterations: {self.state.max_iterations}\n")

        # Initialize current_cv with the draft
        self.state.current_cv = self.state.cv_draft
        self.state.status = "REVIEWING"

    @listen(initialize_flow)
    def review_cv(self):
        """Review the current CV version."""
        print(f"\n{'='*80}")
        print(f"ITERATION {self.state.iteration_count + 1} - REVIEW PHASE")
        print(f"{'='*80}\n")

        # Prepare supporting docs text
        supporting_docs_text = "\n\n".join(
            f"Document {i+1}:\n{doc}"
            for i, doc in enumerate(self.state.supporting_docs)
        ) if self.state.supporting_docs else "No additional documents provided."

        # Run reviewer crew
        crew = self.reviewer_crew.crew(
            job_description=self.state.job_description,
            current_cv=self.state.current_cv,
            supporting_docs=supporting_docs_text,
            iteration_count=self.state.iteration_count + 1,
            max_iterations=self.state.max_iterations,
        )

        result = crew.kickoff()
        feedback_text = result.raw if hasattr(result, 'raw') else str(result)

        # Extract decision from feedback
        decision = self._extract_decision(feedback_text)

        # Create feedback object
        feedback = ReviewFeedback(
            iteration=self.state.iteration_count + 1,
            decision=decision,
            comments=feedback_text,
            improvements_needed=self._extract_improvements(feedback_text),
            timestamp=datetime.now(),
        )

        # Add to history
        self.state.feedback_history.append(feedback)

        print(f"\nReviewer Decision: {decision}")
        print(f"Feedback length: {len(feedback_text)} characters\n")

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
        if decision == "APPROVE":
            print(f"\n{'='*80}")
            print("CV APPROVED - Flow Complete")
            print(f"{'='*80}\n")
            self.state.status = "APPROVED"
            return self.complete_flow

        # Check if max iterations reached
        if self.state.iteration_count + 1 >= self.state.max_iterations:
            print(f"\n{'='*80}")
            print("MAX ITERATIONS REACHED - Flow Complete")
            print(f"{'='*80}\n")
            self.state.status = "MAX_ITERATIONS_REACHED"
            return self.complete_flow

        # Continue to revision
        print(f"\nContinuing to revision phase...")
        self.state.status = "REVISING"
        return self.revise_cv

    @listen(route_decision)
    def revise_cv(self):
        """Revise the CV based on reviewer feedback."""
        print(f"\n{'='*80}")
        print(f"ITERATION {self.state.iteration_count + 1} - WRITING PHASE")
        print(f"{'='*80}\n")

        # Get latest feedback
        latest_feedback = self.state.feedback_history[-1].comments

        # Prepare supporting docs text
        supporting_docs_text = "\n\n".join(
            f"Document {i+1}:\n{doc}"
            for i, doc in enumerate(self.state.supporting_docs)
        ) if self.state.supporting_docs else "No additional documents provided."

        # Run writer crew
        crew = self.writer_crew.crew(
            job_description=self.state.job_description,
            current_cv=self.state.current_cv,
            supporting_docs=supporting_docs_text,
            latest_feedback=latest_feedback,
        )

        result = crew.kickoff()
        revised_cv = result.raw if hasattr(result, 'raw') else str(result)

        # Clean up the CV (remove any markdown code blocks if present)
        revised_cv = self._clean_cv_output(revised_cv)

        # Update state
        self.state.current_cv = revised_cv
        self.state.iteration_count += 1

        print(f"\nRevised CV length: {len(revised_cv)} characters")
        print(f"Completed iteration {self.state.iteration_count}\n")

        # Loop back to review
        self.state.status = "REVIEWING"
        return self.review_cv()

    @listen(route_decision)
    def complete_flow(self):
        """Complete the flow."""
        print(f"\n{'='*80}")
        print("CV OPTIMIZATION COMPLETE")
        print(f"{'='*80}\n")
        print(f"Final Status: {self.state.status}")
        print(f"Total Iterations: {self.state.iteration_count}")
        print(f"Total Feedback Entries: {len(self.state.feedback_history)}\n")

    @staticmethod
    def _extract_decision(feedback: str) -> str:
        """
        Extract decision from feedback text.

        Args:
            feedback: Feedback text

        Returns:
            Decision (APPROVE or REVISE)
        """
        # Look for "DECISION: APPROVE" or "DECISION: REVISE"
        match = re.search(r"DECISION:\s*(APPROVE|REVISE)", feedback, re.IGNORECASE)
        if match:
            return match.group(1).upper()

        # Fallback: look for APPROVE or REVISE in the first few lines
        lines = feedback.split("\n")[:5]
        for line in lines:
            if "APPROVE" in line.upper() and "REVISE" not in line.upper():
                return "APPROVE"
            if "REVISE" in line.upper() and "APPROVE" not in line.upper():
                return "REVISE"

        # Default to REVISE if unclear
        return "REVISE"

    @staticmethod
    def _extract_improvements(feedback: str) -> list:
        """
        Extract improvement points from feedback.

        Args:
            feedback: Feedback text

        Returns:
            List of improvement points
        """
        improvements = []
        lines = feedback.split("\n")

        for line in lines:
            # Look for bullet points or numbered items
            if re.match(r"^\s*[-*•]\s+", line) or re.match(r"^\s*\d+\.\s+", line):
                # Clean and add
                clean_line = re.sub(r"^\s*[-*•\d.]+\s+", "", line).strip()
                if clean_line and len(clean_line) > 10:
                    improvements.append(clean_line)

        return improvements[:10]  # Limit to top 10

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
            flags=re.IGNORECASE | re.MULTILINE
        )

        return cv_text.strip()

