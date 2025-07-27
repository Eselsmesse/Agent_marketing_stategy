from dotenv import load_dotenv
from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import yaml
import os

# Uncomment the following line to use an example of a custom tool
# from marketing_posts.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pydantic import BaseModel, Field
from marketing_posts.config.llm_config import LLMConfig

load_dotenv()


def load_yaml_config(file_path):
    """Загружает YAML конфигурацию из файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"⚠️ Файл конфигурации не найден: {file_path}")
        return {}
    except yaml.YAMLError as e:
        print(f"❌ Ошибка парсинга YAML в {file_path}: {e}")
        return {}
    except Exception as e:
        print(f"❌ Неожиданная ошибка при загрузке {file_path}: {e}")
        return {}


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
    """MarketingPosts crew - стандартная конфигурация"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self, llm_provider: str = "deepseek", llm_model: str = None, use_gaming_config: bool = False):
        """
        Инициализация crew с DeepSeek LLM провайдером
        
        Args:
            llm_provider: Провайдер LLM (только "deepseek")
            llm_model: Конкретная модель для использования
            use_gaming_config: Использовать ли игровую конфигурацию
        """
        self.llm_provider = llm_provider
        self.llm_model = llm_model
        self.use_gaming_config = use_gaming_config
        
        # Если нужна игровая конфигурация, создаем экземпляр игрового класса
        if use_gaming_config:
            print("🎮 Переключаемся на игровую конфигурацию")
            # Создаем экземпляр игрового класса и копируем его атрибуты
            gaming_crew = GamingMarketingPostsCrew(llm_provider, llm_model)
            self.__dict__.update(gaming_crew.__dict__)
            return
        
        print("🏢 Используются стандартные агенты и задачи")
        
        # Проверяем существование файлов (полные пути для проверки)
        full_agents_path = f'src/marketing_posts/{self.agents_config}'
        full_tasks_path = f'src/marketing_posts/{self.tasks_config}'
        
        if not os.path.exists(full_agents_path):
            print(f"⚠️ Файл агентов не найден: {full_agents_path}")
        if not os.path.exists(full_tasks_path):
            print(f"⚠️ Файл задач не найден: {full_tasks_path}")
        
        # Загружаем для отладки
        agents_data = load_yaml_config(full_agents_path)
        tasks_data = load_yaml_config(full_tasks_path)
        print(f"📋 Загружено агентов: {len(agents_data)}")
        print(f"📋 Загружено задач: {len(tasks_data)}")
        
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
        )


@CrewBase
class GamingMarketingPostsCrew():
    """MarketingPosts crew - игровая конфигурация"""
    agents_config = 'config/agents_gaming.yaml'
    tasks_config = 'config/tasks_gaming.yaml'

    def __init__(self, llm_provider: str = "deepseek", llm_model: str = None):
        """
        Инициализация игрового crew с DeepSeek LLM провайдером
        
        Args:
            llm_provider: Провайдер LLM (только "deepseek")
            llm_model: Конкретная модель для использования
        """
        self.llm_provider = llm_provider
        self.llm_model = llm_model
        
        print("🎮 Используются игровые агенты и задачи")
        
        # Проверяем существование файлов (полные пути для проверки)
        full_agents_path = f'src/marketing_posts/{self.agents_config}'
        full_tasks_path = f'src/marketing_posts/{self.tasks_config}'
        
        if not os.path.exists(full_agents_path):
            print(f"⚠️ Файл агентов не найден: {full_agents_path}")
        if not os.path.exists(full_tasks_path):
            print(f"⚠️ Файл задач не найден: {full_tasks_path}")
        
        # Загружаем для отладки
        agents_data = load_yaml_config(full_agents_path)
        tasks_data = load_yaml_config(full_tasks_path)
        print(f"📋 Загружено агентов: {len(agents_data)}")
        print(f"📋 Загружено задач: {len(tasks_data)}")
        
        self.llm = LLMConfig.get_default_llm(
            provider=llm_provider,
            model=llm_model
        )

    @agent
    def gaming_market_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['gaming_market_analyst'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True,
            memory=False,
            llm=self.llm,
        )

    @agent
    def gaming_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['gaming_strategist'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True,
            memory=False,
            llm=self.llm,
        )

    @agent
    def content_creator_gaming(self) -> Agent:
        return Agent(
            config=self.agents_config['content_creator_gaming'],
            verbose=True,
            memory=False,
            llm=self.llm,
        )

    @agent
    def community_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['community_manager'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True,
            memory=False,
            llm=self.llm,
        )

    @agent
    def legal_compliance_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['legal_compliance_specialist'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True,
            memory=False,
            llm=self.llm,
        )

    @agent
    def technical_marketing_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['technical_marketing_specialist'],
            verbose=True,
            memory=False,
            llm=self.llm,
        )

    @task
    def gaming_market_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['gaming_market_research_task'],
            agent=self.gaming_market_analyst()
        )

    @task
    def gaming_audience_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['gaming_audience_analysis_task'],
            agent=self.gaming_strategist()
        )

    @task
    def gaming_marketing_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['gaming_marketing_strategy_task'],
            agent=self.gaming_strategist()
        )

    @task
    def gaming_content_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['gaming_content_creation_task'],
            agent=self.content_creator_gaming()
        )

    @task
    def gaming_technical_positioning_task(self) -> Task:
        return Task(
            config=self.tasks_config['gaming_technical_positioning_task'],
            agent=self.content_creator_gaming(),
            context=[
                self.gaming_marketing_strategy_task(), 
                self.gaming_content_creation_task()
            ]
        )

    @task
    def gaming_legal_risk_assessment_task(self) -> Task:
        return Task(
            config=self.tasks_config['gaming_legal_risk_assessment_task'],
            agent=self.legal_compliance_specialist()
        )

    @task
    def gaming_community_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['gaming_community_strategy_task'],
            agent=self.community_manager()
        )

    @task
    def gaming_campaign_execution_task(self) -> Task:
        return Task(
            config=self.tasks_config['gaming_campaign_execution_task'],
            agent=self.technical_marketing_specialist(),
            context=[
                self.gaming_marketing_strategy_task(),
                self.gaming_legal_risk_assessment_task(),
                self.gaming_community_strategy_task()
            ]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Gaming MarketingPosts crew"""
        return Crew(
            agents=self.agents,  # Automatically created by @agent decorator
            tasks=self.tasks,  # Automatically created by @task decorator
            process=Process.sequential,
            verbose=True,
        )
