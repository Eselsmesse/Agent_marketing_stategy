"""
Инструменты для веб-скрапинга и поиска информации.
Использует Serper API для поиска и анализа веб-контента.
"""

import json
import os
from typing import List, Dict, Any, Optional
import requests
from langchain.tools import tool
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()


class WebSearchTools:
    """
    Инструменты для веб-поиска и анализа контента.
    
    Предоставляет функциональность для:
    - Поиска информации в интернете
    - Анализа конкурентов
    - Исследования рынка
    - Сбора данных о продуктах
    """
    
    def __init__(self):
        """Инициализирует инструменты веб-поиска."""
        self.serper_api_key = os.getenv('SERPER_API_KEY')
        if not self.serper_api_key:
            raise ValueError(
                "SERPER_API_KEY не найден в переменных окружения"
            )
    
    @tool("Поиск информации в интернете")
    def search_internet(self, query: str) -> str:
        """
        Поиск информации в интернете по заданному запросу.
        
        Args:
            query: Поисковый запрос
            
        Returns:
            Результаты поиска в структурированном виде
        """
        return self._perform_search(query, num_results=5)
    
    @tool("Поиск конкурентов")
    def search_competitors(self, industry: str, region: str = "Россия") -> str:
        """
        Поиск конкурентов в заданной отрасли и регионе.
        
        Args:
            industry: Отрасль для поиска
            region: Регион поиска (по умолчанию: Россия)
            
        Returns:
            Список конкурентов с описанием
        """
        query = f"конкуренты {industry} {region} 2025"
        return self._perform_search(query, num_results=8)
    
    @tool("Анализ рынка")
    def analyze_market(self, market: str, region: str = "Россия") -> str:
        """
        Анализ рынка по заданной отрасли.
        
        Args:
            market: Рынок для анализа
            region: Регион анализа
            
        Returns:
            Анализ рынка с ключевыми метриками
        """
        query = f"анализ рынка {market} {region} 2024 статистика"
        return self._perform_search(query, num_results=6)
    
    @tool("Исследование продукта")
    def research_product(self, product: str) -> str:
        """
        Исследование продукта и его характеристик.
        
        Args:
            product: Название продукта
            
        Returns:
            Информация о продукте
        """
        query = f"{product} обзор характеристики отзывы"
        return self._perform_search(query, num_results=5)
    
    @tool("Поиск трендов")
    def search_trends(self, topic: str, platform: str = "общие") -> str:
        """
        Поиск трендов по заданной теме.
        
        Args:
            topic: Тема для поиска трендов
            platform: Платформа (общие, telegram, discord)
            
        Returns:
            Актуальные тренды по теме
        """
        if platform == "telegram":
            query = f"тренды {topic} telegram каналы"
        elif platform == "discord":
            query = f"тренды {topic} discord серверы"
        else:
            query = f"тренды {topic} 2024"
        
        return self._perform_search(query, num_results=5)
    
    @tool("Анализ аудитории")
    def analyze_audience(self, target_audience: str) -> str:
        """
        Анализ целевой аудитории.
        
        Args:
            target_audience: Описание целевой аудитории
            
        Returns:
            Анализ аудитории с демографическими данными
        """
        query = f"анализ аудитории {target_audience} демография"
        return self._perform_search(query, num_results=6)
    
    @tool("Поиск маркетинговых стратегий")
    def search_marketing_strategies(
        self, 
        industry: str, 
        platform: str = "общие"
    ) -> str:
        """
        Поиск маркетинговых стратегий для отрасли.
        
        Args:
            industry: Отрасль
            platform: Платформа (общие, telegram, discord)
            
        Returns:
            Эффективные маркетинговые стратегии
        """
        if platform == "telegram":
            query = f"маркетинг {industry} telegram стратегии"
        elif platform == "discord":
            query = f"маркетинг {industry} discord стратегии"
        else:
            query = f"маркетинговые стратегии {industry} 2024"
        
        return self._perform_search(query, num_results=5)
    
    @tool("Исследование игровой индустрии")
    def research_gaming_industry(self, game_type: str) -> str:
        """
        Исследование игровой индустрии.
        
        Args:
            game_type: Тип игры (puzzle, survival, mobile)
            
        Returns:
            Анализ игровой индустрии
        """
        query = f"игровая индустрия {game_type} игры анализ рынка"
        return self._perform_search(query, num_results=6)
    
    @tool("Поиск правовой информации")
    def search_legal_info(self, topic: str) -> str:
        """
        Поиск правовой информации по теме.
        
        Args:
            topic: Тема для правового анализа
            
        Returns:
            Правовая информация и риски
        """
        query = f"правовые аспекты {topic} законодательство риски"
        return self._perform_search(query, num_results=5)
    
    def _perform_search(
        self, 
        query: str, 
        num_results: int = 5
    ) -> str:
        """
        Выполняет поиск через Serper API.
        
        Args:
            query: Поисковый запрос
            num_results: Количество результатов
            
        Returns:
            Структурированные результаты поиска
        """
        try:
            url = "https://google.serper.dev/search"
            payload = json.dumps({"q": query, "num": num_results})
            headers = {
                'X-API-KEY': self.serper_api_key,
                'content-type': 'application/json'
            }
            
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            
            data = response.json()
            organic_results = data.get('organic', [])
            
            if not organic_results:
                return f"По запросу '{query}' ничего не найдено."
            
            results = []
            for i, result in enumerate(organic_results[:num_results], 1):
                try:
                    result_text = '\n'.join([
                        f"Результат {i}:",
                        f"Заголовок: {result.get('title', 'Нет заголовка')}",
                        f"Ссылка: {result.get('link', 'Нет ссылки')}",
                        f"Описание: {result.get('snippet', 'Нет описания')}",
                        "-----------------"
                    ])
                    results.append(result_text)
                except KeyError:
                    continue
            
            content = '\n'.join(results)
            return f"Результаты поиска по запросу '{query}':\n\n{content}"
            
        except requests.exceptions.RequestException as e:
            return f"Ошибка при выполнении поиска: {str(e)}"
        except Exception as e:
            return f"Неожиданная ошибка: {str(e)}"


class WebAnalysisTools:
    """
    Инструменты для анализа веб-контента.
    
    Предоставляет функциональность для:
    - Анализа веб-страниц
    - Извлечения ключевой информации
    - Структурирования данных
    """
    
    @tool("Анализ веб-страницы")
    def analyze_webpage(self, url: str) -> str:
        """
        Анализ содержимого веб-страницы.
        
        Args:
            url: URL страницы для анализа
            
        Returns:
            Структурированный анализ страницы
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Простой анализ HTML (можно расширить)
            content = response.text[:2000]  # Первые 2000 символов
            
            return f"""
Анализ страницы: {url}

Основная информация:
- Статус: {response.status_code}
- Размер контента: {len(response.text)} символов
- Кодировка: {response.encoding}

Начало контента:
{content}...

Для полного анализа рекомендуется использовать специализированные инструменты.
"""
            
        except requests.exceptions.RequestException as e:
            return f"Ошибка при анализе страницы {url}: {str(e)}"
        except Exception as e:
            return f"Неожиданная ошибка при анализе: {str(e)}"


# Создаем экземпляры инструментов
web_search_tools = WebSearchTools()
web_analysis_tools = WebAnalysisTools()

# Экспортируем инструменты для использования в агентах
__all__ = [
    'WebSearchTools',
    'WebAnalysisTools',
    'web_search_tools',
    'web_analysis_tools'
] 