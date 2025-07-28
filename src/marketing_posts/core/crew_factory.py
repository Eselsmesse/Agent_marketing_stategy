"""
Фабрика crew для создания различных типов конфигураций crew.
Реализует паттерн Factory для создания crew.
"""

from typing import Dict, Type
from .base_crew import BaseCrew, CrewConfig
from .config_manager import ConfigManager


class CrewFactory:
    """
    Фабрика для создания различных типов конфигураций crew.
    
    Реализует паттерн Factory для создания соответствующих экземпляров crew
    на основе типа конфигурации.
    """
    
    def __init__(self, config_manager: ConfigManager):
        """
        Инициализирует фабрику crew.
        
        Args:
            config_manager: Экземпляр менеджера конфигураций
        """
        self.config_manager = config_manager
        self._crew_registry: Dict[str, Type[BaseCrew]] = {}
    
    def register_crew_type(
        self, 
        crew_type: str, 
        crew_class: Type[BaseCrew]
    ) -> None:
        """
        Регистрирует новый тип crew.
        
        Args:
            crew_type: Идентификатор типа для crew
            crew_class: Класс crew для регистрации
        """
        self._crew_registry[crew_type] = crew_class
    
    def create_crew(
        self, 
        crew_type: str, 
        config: CrewConfig
    ) -> BaseCrew:
        """
        Создает экземпляр crew указанного типа.
        
        Args:
            crew_type: Тип crew для создания
            config: Конфигурация для crew
            
        Returns:
            Настроенный экземпляр crew
            
        Raises:
            ValueError: Если тип crew не зарегистрирован
        """
        if crew_type not in self._crew_registry:
            available_types = list(self._crew_registry.keys())
            raise ValueError(
                f"Неизвестный тип crew: {crew_type}. "
                f"Доступные типы: {available_types}"
            )
        
        crew_class = self._crew_registry[crew_type]
        return crew_class(config)
    
    def get_available_crew_types(self) -> list[str]:
        """Возвращает список доступных типов crew."""
        return list(self._crew_registry.keys())
    
    def validate_crew_config(
        self, 
        crew_type: str, 
        config: CrewConfig
    ) -> bool:
        """
        Валидирует конфигурацию для конкретного типа crew.
        
        Args:
            crew_type: Тип crew для валидации
            config: Конфигурация для валидации
            
        Returns:
            True, если конфигурация валидна
        """
        if crew_type not in self._crew_registry:
            return False
        
        crew_class = self._crew_registry[crew_type]
        
        # Базовая валидация - проверяем, можно ли создать crew
        try:
            crew_class(config)
            return True
        except Exception:
            return False


class CrewBuilder:
    """
    Реализация паттерна Builder для создания конфигураций crew.
    
    Предоставляет fluent интерфейс для построения конфигураций crew.
    """
    
    def __init__(self):
        """Инициализирует builder crew."""
        self._config = CrewConfig()
    
    def with_llm_provider(self, provider: str) -> 'CrewBuilder':
        """Устанавливает провайдера LLM."""
        self._config.llm_provider = provider
        return self
    
    def with_llm_model(self, model: str) -> 'CrewBuilder':
        """Устанавливает модель LLM."""
        self._config.llm_model = model
        return self
    
    def with_agents_config(self, config_path: str) -> 'CrewBuilder':
        """Устанавливает путь к конфигурации агентов."""
        self._config.agents_config = config_path
        return self
    
    def with_tasks_config(self, config_path: str) -> 'CrewBuilder':
        """Устанавливает путь к конфигурации задач."""
        self._config.tasks_config = config_path
        return self
    
    def with_verbose(self, verbose: bool) -> 'CrewBuilder':
        """Устанавливает режим verbose."""
        self._config.verbose = verbose
        return self
    
    def with_memory(self, memory: bool) -> 'CrewBuilder':
        """Устанавливает режим памяти."""
        self._config.memory = memory
        return self
    
    def build(self) -> CrewConfig:
        """Строит и возвращает конфигурацию crew."""
        return self._config
    
    @classmethod
    def create_standard_config(cls) -> 'CrewBuilder':
        """Создает builder со стандартной конфигурацией."""
        return cls().with_llm_provider("deepseek")
    
    @classmethod
    def create_gaming_config(cls) -> 'CrewBuilder':
        """Создает builder с игровой конфигурацией."""
        return (cls()
                .with_llm_provider("deepseek")
                .with_agents_config("config/agents_gaming.yaml")
                .with_tasks_config("config/tasks_gaming.yaml")) 