"""
Игровая реализация crew для маркетинга игровых проектов.
"""

from typing import List
from crewai import Agent, Task
from marketing_posts.core.base_crew import BaseCrew
from marketing_posts.core.config_manager import ConfigManager


class GamingCrew(BaseCrew):
    """
    Игровая реализация crew для маркетинга игровых проектов.
    
    Использует специализированных агентов и задачи для создания
    маркетинговых стратегий для игровой индустрии.
    """
    
    def _validate_config(self) -> None:
        """Валидирует конфигурацию игрового crew."""
        if not self.config.agents_config or not self.config.tasks_config:
            raise ValueError(
                "Необходимо указать пути к конфигурациям агентов и задач"
            )
    
    def _initialize_crew(self) -> None:
        """Инициализирует компоненты игрового crew."""
        self.config_manager = ConfigManager()
        print("🎮 Используются игровые агенты и задачи")
    
    def gaming_market_analyst(self) -> Agent:
        """Игровой аналитик рынка."""
        agents_config = self.config_manager.get_agents_config(
            "agents_gaming.yaml"
        )
        analyst_config = agents_config.get('gaming_market_analyst', {})
        
        return Agent(
            role=analyst_config.get('role', 'Игровой аналитик рынка'),
            goal=analyst_config.get('goal', 'Анализ игрового рынка'),
            backstory=analyst_config.get(
                'backstory', 'Эксперт по игровой индустрии'
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def gaming_strategist(self) -> Agent:
        """Игровой стратег."""
        agents_config = self.config_manager.get_agents_config(
            "agents_gaming.yaml"
        )
        strategist_config = agents_config.get('gaming_strategist', {})
        
        return Agent(
            role=strategist_config.get('role', 'Игровой стратег'),
            goal=strategist_config.get('goal', 'Разработка игровых стратегий'),
            backstory=strategist_config.get(
                'backstory', 'Стратег игровой индустрии'
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def content_creator_gaming(self) -> Agent:
        """Создатель игрового контента."""
        agents_config = self.config_manager.get_agents_config(
            "agents_gaming.yaml"
        )
        creator_config = agents_config.get('content_creator_gaming', {})
        
        return Agent(
            role=creator_config.get('role', 'Создатель игрового контента'),
            goal=creator_config.get('goal', 'Создание игрового контента'),
            backstory=creator_config.get(
                'backstory', 'Креативщик игровой индустрии'
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def community_manager(self) -> Agent:
        """Менеджер сообщества."""
        agents_config = self.config_manager.get_agents_config(
            "agents_gaming.yaml"
        )
        manager_config = agents_config.get('community_manager', {})
        
        return Agent(
            role=manager_config.get('role', 'Менеджер сообщества'),
            goal=manager_config.get(
                'goal', 'Управление игровым сообществом'
            ),
            backstory=manager_config.get(
                'backstory', 'Эксперт по сообществам'
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def legal_compliance_specialist(self) -> Agent:
        """Специалист по правовому соответствию."""
        agents_config = self.config_manager.get_agents_config(
            "agents_gaming.yaml"
        )
        legal_config = agents_config.get('legal_compliance_specialist', {})
        
        return Agent(
            role=legal_config.get('role', 'Юридический специалист'),
            goal=legal_config.get('goal', 'Правовое соответствие'),
            backstory=legal_config.get('backstory', 'Юрист игровой индустрии'),
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def technical_marketing_specialist(self) -> Agent:
        """Технический маркетинговый специалист."""
        agents_config = self.config_manager.get_agents_config(
            "agents_gaming.yaml"
        )
        tech_config = agents_config.get('technical_marketing_specialist', {})
        
        return Agent(
            role=tech_config.get('role', 'Технический маркетолог'),
            goal=tech_config.get('goal', 'Технический маркетинг'),
            backstory=tech_config.get('backstory', 'Технолог маркетинга'),
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def gaming_market_research_task(self) -> Task:
        """Задача исследования игрового рынка."""
        tasks_config = self.config_manager.get_tasks_config(
            "tasks_gaming.yaml"
        )
        research_config = tasks_config.get('gaming_market_research_task', {})
        
        return Task(
            description=research_config.get(
                'description', 'Исследуйте игровой рынок'
            ),
            agent=self.gaming_market_analyst(),
            expected_output=research_config.get(
                'expected_output', 'Анализ игрового рынка'
            ),
            output_format='raw'
        )
    
    def gaming_audience_analysis_task(self) -> Task:
        """Задача анализа игровой аудитории."""
        tasks_config = self.config_manager.get_tasks_config(
            "tasks_gaming.yaml"
        )
        audience_config = tasks_config.get('gaming_audience_analysis_task', {})
        
        return Task(
            description=audience_config.get(
                'description', 'Проанализируйте аудиторию'
            ),
            agent=self.gaming_market_analyst(),
            expected_output=audience_config.get(
                'expected_output', 'Анализ аудитории'
            ),
            output_format='raw'
        )
    
    def gaming_legal_risk_assessment_task(self) -> Task:
        """Задача оценки правовых рисков."""
        tasks_config = self.config_manager.get_tasks_config(
            "tasks_gaming.yaml"
        )
        legal_config = tasks_config.get(
            'gaming_legal_risk_assessment_task', {}
        )
        
        return Task(
            description=legal_config.get(
                'description', 'Оцените правовые риски'
            ),
            agent=self.legal_compliance_specialist(),
            expected_output=legal_config.get(
                'expected_output', 'Оценка рисков'
            ),
            output_format='raw'
        )
    
    def gaming_community_strategy_task(self) -> Task:
        """Задача стратегии сообщества."""
        tasks_config = self.config_manager.get_tasks_config(
            "tasks_gaming.yaml"
        )
        community_config = tasks_config.get(
            'gaming_community_strategy_task', {}
        )
        
        return Task(
            description=community_config.get(
                'description', 'Разработайте стратегию сообщества'
            ),
            agent=self.community_manager(),
            expected_output=community_config.get(
                'expected_output', 'Стратегия сообщества'
            ),
            output_format='raw'
        )
    
    def gaming_marketing_strategy_task(self) -> Task:
        """Задача игровой маркетинговой стратегии."""
        tasks_config = self.config_manager.get_tasks_config(
            "tasks_gaming.yaml"
        )
        strategy_config = tasks_config.get(
            'gaming_marketing_strategy_task', {}
        )
        
        return Task(
            description=strategy_config.get(
                'description', 'Разработайте игровую стратегию'
            ),
            agent=self.gaming_strategist(),
            expected_output=strategy_config.get(
                'expected_output', 'Игровая стратегия'
            ),
            output_format='raw'
        )
    
    def gaming_content_creation_task(self) -> Task:
        """Задача создания игрового контента."""
        tasks_config = self.config_manager.get_tasks_config(
            "tasks_gaming.yaml"
        )
        content_config = tasks_config.get('gaming_content_creation_task', {})
        
        return Task(
            description=content_config.get(
                'description', 'Создайте игровой контент'
            ),
            agent=self.content_creator_gaming(),
            expected_output=content_config.get(
                'expected_output', 'Игровой контент'
            ),
            output_format='raw'
        )
    
    def gaming_technical_positioning_task(self) -> Task:
        """Задача технического позиционирования."""
        tasks_config = self.config_manager.get_tasks_config(
            "tasks_gaming.yaml"
        )
        tech_config = tasks_config.get('gaming_technical_positioning_task', {})
        
        return Task(
            description=tech_config.get(
                'description', 'Позиционируйте технически'
            ),
            agent=self.technical_marketing_specialist(),
            expected_output=tech_config.get(
                'expected_output', 'Техническое позиционирование'
            ),
            output_format='raw'
        )
    
    def gaming_campaign_execution_task(self) -> Task:
        """Задача выполнения игровой кампании."""
        tasks_config = self.config_manager.get_tasks_config(
            "tasks_gaming.yaml"
        )
        campaign_config = tasks_config.get(
            'gaming_campaign_execution_task', {}
        )
        
        return Task(
            description=campaign_config.get(
                'description', 'Выполните игровую кампанию'
            ),
            agent=self.gaming_strategist(),
            expected_output=campaign_config.get(
                'expected_output', 'Исполнение кампании'
            ),
            output_format='raw'
        )
    
    def get_agents(self) -> List[Agent]:
        """Возвращает список агентов для игрового crew."""
        return [
            self.gaming_market_analyst(),
            self.gaming_strategist(),
            self.content_creator_gaming(),
            self.community_manager(),
            self.legal_compliance_specialist(),
            self.technical_marketing_specialist()
        ]
    
    def get_tasks(self) -> List[Task]:
        """Возвращает список задач для игрового crew."""
        return [
            self.gaming_market_research_task(),
            self.gaming_audience_analysis_task(),
            self.gaming_legal_risk_assessment_task(),
            self.gaming_community_strategy_task(),
            self.gaming_marketing_strategy_task(),
            self.gaming_content_creation_task(),
            self.gaming_technical_positioning_task(),
            self.gaming_campaign_execution_task()
        ] 