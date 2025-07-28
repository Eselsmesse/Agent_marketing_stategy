"""
Основной модуль для системы маркетинговых постов.
Содержит базовые классы, интерфейсы и общую функциональность.
"""

from .base_crew import BaseCrew
from .crew_factory import CrewFactory
from .config_manager import ConfigManager
from .result_saver import ResultSaver

__all__ = [
    'BaseCrew',
    'CrewFactory', 
    'ConfigManager',
    'ResultSaver'
] 