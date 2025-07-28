"""
Конкретные реализации crew для системы маркетинговых постов.
"""

from .standard_crew import StandardCrew
from .gaming_crew import GamingCrew

__all__ = [
    'StandardCrew',
    'GamingCrew'
] 