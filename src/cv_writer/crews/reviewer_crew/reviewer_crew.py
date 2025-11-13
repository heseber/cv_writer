"""Reviewer crew for CV optimization."""

from typing import Any

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class ReviewerCrew:
    """Crew for reviewing CVs and providing feedback."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, llm: Any):
        """
        Initialize reviewer crew.

        Args:
            llm: Language model instance
        """
        self.llm = llm

    @agent
    def cv_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config["cv_reviewer"],
            llm=self.llm,
        )

    @task
    def review_cv(self) -> Task:
        return Task(
            config=self.tasks_config["review_cv"],
            agent=self.cv_reviewer(),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Reviewer Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=False,
        )
