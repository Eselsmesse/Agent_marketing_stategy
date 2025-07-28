"""
Стандартная реализация crew для обычного маркетинга.
"""

from typing import List
from crewai import Agent, Task
from marketing_posts.core.base_crew import BaseCrew
from marketing_posts.core.config_manager import ConfigManager


class StandardCrew(BaseCrew):
    """
    Стандартная реализация crew для обычного маркетинга.
    
    Использует стандартные агенты и задачи для создания
    маркетинговых стратегий общего назначения.
    """
    
    def _validate_config(self) -> None:
        """Валидирует конфигурацию стандартного crew."""
        if not self.config.agents_config or not self.config.tasks_config:
            raise ValueError(
                "Необходимо указать пути к конфигурациям агентов и задач"
            )
    
    def _initialize_crew(self) -> None:
        """Инициализирует компоненты стандартного crew."""
        self.config_manager = ConfigManager()
        print("🏢 Используются стандартные агенты и задачи")
    
    def lead_market_analyst(self) -> Agent:
        """Ведущий аналитик рынка."""
        agents_config = self.config_manager.get_agents_config()
        analyst_config = agents_config.get('lead_market_analyst', {})
        
        return Agent(
            role=analyst_config.get('role', 'Ведущий аналитик рынка'),
            goal=analyst_config.get(
                'goal', 'Проведение глубокого анализа рынка'
            ),
            backstory=analyst_config.get(
                'backstory', 'Опытный аналитик с 10+ лет опыта'
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def chief_marketing_strategist(self) -> Agent:
        """Главный маркетинговый стратег."""
        agents_config = self.config_manager.get_agents_config()
        strategist_config = agents_config.get('chief_marketing_strategist', {})
        
        return Agent(
            role=strategist_config.get(
                'role', 'Главный маркетинговый стратег'
            ),
            goal=strategist_config.get(
                'goal', 'Разработка эффективных маркетинговых стратегий'
            ),
            backstory=strategist_config.get(
                'backstory', 'Стратег с опытом в крупных компаниях'
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def creative_content_creator(self) -> Agent:
        """Креативный создатель контента."""
        agents_config = self.config_manager.get_agents_config()
        creator_config = agents_config.get('creative_content_creator', {})
        
        return Agent(
            role=creator_config.get(
                'role', 'Креативный создатель контента'
            ),
            goal=creator_config.get(
                'goal', 'Создание привлекательного контента'
            ),
            backstory=creator_config.get(
                'backstory', 'Креативщик с богатым опытом'
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def research_task(self) -> Task:
        """Задача исследования рынка."""
        tasks_config = self.config_manager.get_tasks_config()
        research_config = tasks_config.get('research_task', {})
        
        return Task(
            description=research_config.get(
                'description', 'Проведите анализ рынка'
            ),
            agent=self.lead_market_analyst(),
            expected_output=research_config.get(
                'expected_output', 'Детальный анализ рынка'
            ),
            output_format='raw'
        )
    
    def project_understanding_task(self) -> Task:
        """Задача понимания проекта."""
        tasks_config = self.config_manager.get_tasks_config()
        understanding_config = tasks_config.get(
            'project_understanding_task', {}
        )
        
        return Task(
            description=understanding_config.get(
                'description', 'Изучите проект'
            ),
            agent=self.lead_market_analyst(),
            expected_output=understanding_config.get(
                'expected_output', 'Понимание проекта'
            ),
            output_format='raw'
        )
    
    def marketing_strategy_task(self) -> Task:
        """Задача разработки маркетинговой стратегии."""
        tasks_config = self.config_manager.get_tasks_config()
        strategy_config = tasks_config.get('marketing_strategy_task', {})
        
        return Task(
            description=strategy_config.get(
                'description', 'Разработайте маркетинговую стратегию'
            ),
            agent=self.chief_marketing_strategist(),
            expected_output=strategy_config.get(
                'expected_output', 'Маркетинговая стратегия'
            ),
            output_format='raw'
        )
    
    def campaign_idea_task(self) -> Task:
        """Задача создания идей кампаний."""
        tasks_config = self.config_manager.get_tasks_config()
        campaign_config = tasks_config.get('campaign_idea_task', {})
        
        return Task(
            description=campaign_config.get(
                'description', 'Создайте идеи кампаний'
            ),
            agent=self.chief_marketing_strategist(),
            expected_output=campaign_config.get(
                'expected_output', 'Идеи кампаний'
            ),
            output_format='raw'
        )
    
    def copy_creation_task(self) -> Task:
        """Задача создания копирайтинга."""
        tasks_config = self.config_manager.get_tasks_config()
        copy_config = tasks_config.get('copy_creation_task', {})
        
        return Task(
            description=copy_config.get('description', 'Создайте копирайтинг'),
            agent=self.creative_content_creator(),
            expected_output=copy_config.get('expected_output', 'Копирайтинг'),
            output_format='raw'
        )
    
    def get_agents(self) -> List[Agent]:
        """Возвращает список агентов для стандартного crew."""
        return [
            self.lead_market_analyst(),
            self.chief_marketing_strategist(),
            self.creative_content_creator()
        ]
    
    def get_tasks(self) -> List[Task]:
        """Возвращает список задач для стандартного crew."""
        return [
            self.research_task(),
            self.project_understanding_task(),
            self.marketing_strategy_task(),
            self.campaign_idea_task(),
            self.copy_creation_task()
        ] 