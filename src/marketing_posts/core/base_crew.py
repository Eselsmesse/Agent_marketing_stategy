"""
Абстрактный базовый класс для всех конфигураций crew.
Определяет интерфейс, который должны реализовывать все crew конфигурации.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from crewai import Agent, Task, Crew, Process
from marketing_posts.config.llm_config import LLMConfig


@dataclass
class CrewConfig:
    """Конфигурация для инициализации crew."""
    llm_provider: str = "deepseek"
    llm_model: Optional[str] = None
    agents_config: str = "config/agents.yaml"
    tasks_config: str = "config/tasks.yaml"
    verbose: bool = True
    memory: bool = False


class BaseCrew:
    """
    Базовый класс для всех реализаций crew.
    
    Этот класс определяет общий интерфейс и функциональность, которые должны
    реализовывать все конфигурации crew. Предоставляет паттерн Template Method
    для инициализации и выполнения crew.
    """
    
    def __init__(self, config: CrewConfig):
        """
        Инициализирует crew с заданной конфигурацией.
        
        Args:
            config: Объект конфигурации crew
        """
        self.config = config
        self.llm = LLMConfig.get_default_llm(
            provider=config.llm_provider,
            model=config.llm_model
        )
        self._validate_config()
        self._initialize_crew()
    
    def _validate_config(self) -> None:
        """Валидирует конфигурацию crew."""
        # Базовая реализация - переопределяется в наследниках
        pass
    
    def _initialize_crew(self) -> None:
        """Инициализирует компоненты, специфичные для crew."""
        # Базовая реализация - переопределяется в наследниках
        pass
    
    def get_agents(self) -> List[Agent]:
        """Возвращает список агентов для этого crew."""
        # Должно быть переопределено в наследниках
        raise NotImplementedError("Метод get_agents должен быть реализован")
    
    def get_tasks(self) -> List[Task]:
        """Возвращает список задач для этого crew."""
        # Должно быть переопределено в наследниках
        raise NotImplementedError("Метод get_tasks должен быть реализован")
    
    def create_crew(self) -> Crew:
        """
        Создает и возвращает экземпляр crew.
        
        Returns:
            Настроенный экземпляр crew
        """
        return Crew(
            agents=self.get_agents(),
            tasks=self.get_tasks(),
            process=Process.sequential,
            verbose=self.config.verbose
        )
    
    def execute(self, inputs: Dict[str, Any]) -> Any:
        """
        Выполняет crew с заданными входными данными.
        
        Args:
            inputs: Входные данные для выполнения crew
            
        Returns:
            Результаты выполнения
        """
        crew_instance = self.create_crew()
        return crew_instance.kickoff(inputs=inputs)
    
    def get_config_info(self) -> Dict[str, Any]:
        """
        Возвращает информацию о конфигурации этого crew.
        
        Returns:
            Словарь с деталями конфигурации
        """
        return {
            'llm_provider': self.config.llm_provider,
            'llm_model': self.config.llm_model,
            'agents_config': self.config.agents_config,
            'tasks_config': self.config.tasks_config,
            'crew_type': self.__class__.__name__
        } 