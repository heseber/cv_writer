"""Writer crew for CV optimization."""

from pathlib import Path
from typing import Any, Dict

import yaml
from crewai import Agent, Crew, Task


class WriterCrew:
    """Crew for writing and improving CVs."""

    def __init__(self, llm: Any):
        """
        Initialize writer crew.

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

    def writer_agent(self) -> Agent:
        """Create writer agent."""
        config = self.agents_config["cv_writer"]
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            verbose=config.get("verbose", True),
            allow_delegation=config.get("allow_delegation", False),
            llm=self.llm,
        )

    def write_task(
        self,
        agent: Agent,
        job_description: str,
        current_cv: str,
        supporting_docs: str,
        latest_feedback: str,
    ) -> Task:
        """
        Create write task.

        Args:
            agent: Writer agent
            job_description: Job description text
            current_cv: Current CV version
            supporting_docs: Supporting documents
            latest_feedback: Latest reviewer feedback

        Returns:
            Write task
        """
        config = self.tasks_config["write_cv"]
        return Task(
            description=config["description"].format(
                job_description=job_description,
                current_cv=current_cv,
                supporting_docs=supporting_docs,
                latest_feedback=latest_feedback,
            ),
            expected_output=config["expected_output"],
            agent=agent,
        )

    def crew(
        self,
        job_description: str,
        current_cv: str,
        supporting_docs: str = "",
        latest_feedback: str = "",
    ) -> Crew:
        """
        Create and return the writer crew.

        Args:
            job_description: Job description text
            current_cv: Current CV version
            supporting_docs: Supporting documents
            latest_feedback: Latest reviewer feedback

        Returns:
            Configured crew
        """
        agent = self.writer_agent()
        task = self.write_task(
            agent,
            job_description,
            current_cv,
            supporting_docs,
            latest_feedback,
        )

        return Crew(
            agents=[agent],
            tasks=[task],
            verbose=True,
        )

