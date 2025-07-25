from dotenv import load_dotenv
from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from marketing_posts.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pydantic import BaseModel, Field
from marketing_posts.config.llm_config import LLMConfig

load_dotenv()


class MarketStrategy(BaseModel):
    """Market strategy model"""
    name: str = Field(..., description="Name of the market strategy")
    tatics: List[str] = Field(
        ..., 
        description="List of tactics to be used in the market strategy"
    )
    channels: List[str] = Field(
        ..., 
        description="List of channels to be used in the market strategy"
    )
    KPIs: List[str] = Field(
        ..., 
        description="List of KPIs to be used in the market strategy"
    )


class CampaignIdea(BaseModel):
    """Campaign idea model"""
    name: str = Field(..., description="Name of the campaign idea")
    description: str = Field(
        ..., 
        description="Description of the campaign idea"
    )
    audience: str = Field(..., description="Audience of the campaign idea")
    channel: str = Field(..., description="Channel of the campaign idea")


class Copy(BaseModel):
    """Copy model"""
    title: str = Field(..., description="Title of the copy")
    body: str = Field(..., description="Body of the copy")


@CrewBase
class MarketingPostsCrew():
    """MarketingPosts crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self, llm_provider: str = "deepseek", llm_model: str = None):
        """
        Инициализация crew с DeepSeek LLM провайдером
        
        Args:
            llm_provider: Провайдер LLM (только "deepseek")
            llm_model: Конкретная модель для использования
        """
        self.llm_provider = llm_provider
        self.llm_model = llm_model
        self.llm = LLMConfig.get_default_llm(
            provider=llm_provider,
            model=llm_model
        )

    @agent
    def lead_market_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_market_analyst'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True,
            memory=False,
            llm=self.llm,
        )

    @agent
    def chief_marketing_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['chief_marketing_strategist'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True,
            memory=False,
            llm=self.llm,
        )

    @agent
    def creative_content_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['creative_content_creator'],
            verbose=True,
            memory=False,
            llm=self.llm,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            agent=self.lead_market_analyst()
        )

    @task
    def project_understanding_task(self) -> Task:
        return Task(
            config=self.tasks_config['project_understanding_task'],
            agent=self.chief_marketing_strategist()
        )

    @task
    def marketing_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['marketing_strategy_task'],
            agent=self.chief_marketing_strategist()
        )

    @task
    def campaign_idea_task(self) -> Task:
        return Task(
            config=self.tasks_config['campaign_idea_task'],
            agent=self.creative_content_creator()
        )

    @task
    def copy_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['copy_creation_task'],
            agent=self.creative_content_creator(),
            context=[
                self.marketing_strategy_task(), 
                self.campaign_idea_task()
            ]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MarketingPosts crew"""
        return Crew(
            agents=self.agents,  # Automatically created by @agent decorator
            tasks=self.tasks,  # Automatically created by @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead 
            # https://docs.crewai.com/how-to/Hierarchical/
        )
