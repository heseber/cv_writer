"""Reviewer crew for CV optimization."""

from pathlib import Path
from typing import Any, Dict

import yaml
from crewai import Agent, Crew, Task


class ReviewerCrew:
    """Crew for reviewing CVs and providing feedback."""

    def __init__(self, llm: Any):
        """
        Initialize reviewer crew.

        Args:
            llm: Language model instance
        """
        self.llm = llm
        self.config_dir = Path(__file__).parent / "config"
        self.agents_config = self._load_config("agents.yaml")
        self.tasks_config = self._load_config("tasks.yaml")

    def _load_config(self, filename: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        config_path = self.config_dir / filename
        with open(config_path, "r") as f:
            return yaml.safe_load(f)

    def reviewer_agent(self) -> Agent:
        """Create reviewer agent."""
        config = self.agents_config["cv_reviewer"]
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            verbose=config.get("verbose", True),
            allow_delegation=config.get("allow_delegation", False),
            llm=self.llm,
        )

    def review_task(
        self,
        agent: Agent,
        job_description: str,
        current_cv: str,
        supporting_docs: str,
        iteration_count: int,
        max_iterations: int,
    ) -> Task:
        """
        Create review task.

        Args:
            agent: Reviewer agent
            job_description: Job description text
            current_cv: Current CV version
            supporting_docs: Supporting documents
            iteration_count: Current iteration number
            max_iterations: Maximum iterations

        Returns:
            Review task
        """
        config = self.tasks_config["review_cv"]
        return Task(
            description=config["description"].format(
                job_description=job_description,
                current_cv=current_cv,
                supporting_docs=supporting_docs,
                iteration_count=iteration_count,
                max_iterations=max_iterations,
            ),
            expected_output=config["expected_output"],
            agent=agent,
        )

    def crew(
        self,
        job_description: str,
        current_cv: str,
        supporting_docs: str = "",
        iteration_count: int = 1,
        max_iterations: int = 3,
    ) -> Crew:
        """
        Create and return the reviewer crew.

        Args:
            job_description: Job description text
            current_cv: Current CV version
            supporting_docs: Supporting documents
            iteration_count: Current iteration number
            max_iterations: Maximum iterations

        Returns:
            Configured crew
        """
        agent = self.reviewer_agent()
        task = self.review_task(
            agent,
            job_description,
            current_cv,
            supporting_docs,
            iteration_count,
            max_iterations,
        )

        return Crew(
            agents=[agent],
            tasks=[task],
            verbose=True,
        )

