"""
Менеджер конфигураций для загрузки и валидации YAML файлов.
Предоставляет централизованное управление конфигурациями с валидацией.
"""

import yaml
from typing import Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class ConfigValidationError(Exception):
    """Исключение, возникающее при ошибке валидации конфигурации."""
    message: str
    config_file: str
    field: Optional[str] = None


class ConfigValidator(ABC):
    """Абстрактный базовый класс для валидаторов конфигураций."""
    
    @abstractmethod
    def validate(self, config: Dict[str, Any]) -> None:
        """Валидирует данные конфигурации."""
        pass


class AgentsConfigValidator(ConfigValidator):
    """Валидатор для конфигурации агентов."""
    
    def validate(self, config: Dict[str, Any]) -> None:
        """Валидирует структуру конфигурации агентов."""
        if not isinstance(config, dict):
            raise ConfigValidationError(
                "Конфигурация агентов должна быть словарем",
                "agents.yaml"
            )
        
        required_fields = ['role', 'goal', 'backstory']
        
        for agent_name, agent_config in config.items():
            if not isinstance(agent_config, dict):
                raise ConfigValidationError(
                    f"Конфигурация агента '{agent_name}' должна быть словарем",
                    "agents.yaml",
                    agent_name
                )
            
            for field in required_fields:
                if field not in agent_config:
                    raise ConfigValidationError(
                        f"Агент '{agent_name}' отсутствует обязательное поле: "
                        f"{field}",
                        "agents.yaml",
                        f"{agent_name}.{field}"
                    )


class TasksConfigValidator(ConfigValidator):
    """Валидатор для конфигурации задач."""
    
    def validate(self, config: Dict[str, Any]) -> None:
        """Валидирует структуру конфигурации задач."""
        if not isinstance(config, dict):
            raise ConfigValidationError(
                "Конфигурация задач должна быть словарем",
                "tasks.yaml"
            )
        
        required_fields = ['description', 'expected_output']
        
        for task_name, task_config in config.items():
            if not isinstance(task_config, dict):
                raise ConfigValidationError(
                    f"Конфигурация задачи '{task_name}' должна быть словарем",
                    "tasks.yaml",
                    task_name
                )
            
            for field in required_fields:
                if field not in task_config:
                    raise ConfigValidationError(
                        f"Задача '{task_name}' отсутствует обязательное поле: "
                        f"{field}",
                        "tasks.yaml",
                        f"{task_name}.{field}"
                    )


class ConfigManager:
    """
    Централизованный менеджер конфигураций для системы маркетинговых постов.
    
    Обрабатывает загрузку, валидацию и кэширование файлов конфигурации.
    Предоставляет чистый интерфейс для доступа к данным конфигурации.
    """
    
    def __init__(self, base_path: str = "src/marketing_posts/config"):
        """
        Инициализирует менеджер конфигураций.
        
        Args:
            base_path: Базовый путь для файлов конфигурации
        """
        self.base_path = Path(base_path)
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._validators = {
            'agents': AgentsConfigValidator(),
            'tasks': TasksConfigValidator()
        }
    
    def load_config(
        self, 
        config_type: str, 
        config_name: str
    ) -> Dict[str, Any]:
        """
        Загружает и валидирует файл конфигурации.
        
        Args:
            config_type: Тип конфигурации (agents, tasks, gaming_inputs)
            config_name: Имя файла конфигурации
            
        Returns:
            Загруженная и валидированная конфигурация
            
        Raises:
            ConfigValidationError: Если валидация конфигурации не прошла
            FileNotFoundError: Если файл конфигурации не найден
        """
        cache_key = f"{config_type}_{config_name}"
        
        # Возвращаем кэшированную конфигурацию, если доступна
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        config_path = self.base_path / config_name
        
        if not config_path.exists():
            raise FileNotFoundError(
                f"Файл конфигурации не найден: {config_path}"
            )
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # Валидируем конфигурацию, если есть валидатор
            if config_type in self._validators:
                self._validators[config_type].validate(config)
            
            # Кэшируем конфигурацию
            self._cache[cache_key] = config
            
            return config
            
        except yaml.YAMLError as e:
            raise ConfigValidationError(
                f"Неверный YAML в {config_name}: {e}",
                config_name
            )
        except Exception as e:
            raise ConfigValidationError(
                f"Ошибка загрузки {config_name}: {e}",
                config_name
            )
    
    def get_agents_config(
        self, 
        config_name: str = "agents.yaml"
    ) -> Dict[str, Any]:
        """Загружает конфигурацию агентов."""
        return self.load_config('agents', config_name)
    
    def get_tasks_config(
        self, 
        config_name: str = "tasks.yaml"
    ) -> Dict[str, Any]:
        """Загружает конфигурацию задач."""
        return self.load_config('tasks', config_name)
    
    def get_gaming_config(
        self, 
        config_name: str = "gaming_inputs.yaml"
    ) -> Dict[str, Any]:
        """Загружает игровую конфигурацию."""
        return self.load_config('gaming_inputs', config_name)
    
    def clear_cache(self) -> None:
        """Очищает кэш конфигураций."""
        self._cache.clear()
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Возвращает информацию о кэшированных конфигурациях."""
        return {
            'cached_configs': list(self._cache.keys()),
            'cache_size': len(self._cache)
        } 