# 🌐 Альтернативы платным сервисам веб-скрапинга

## 📋 Текущее состояние

В текущей реализации используется **Serper API** для веб-поиска. Это платный сервис, который предоставляет:
- Поиск через Google
- Структурированные результаты
- Простота интеграции

## 🔄 Бесплатные альтернативы

### 1. **DuckDuckGo API** (Рекомендуется)

```python
import requests

def search_duckduckgo(query: str, max_results: int = 5) -> str:
    """
    Бесплатный поиск через DuckDuckGo API.
    """
    url = "https://api.duckduckgo.com/"
    params = {
        'q': query,
        'format': 'json',
        'no_html': '1',
        'skip_disambig': '1'
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    results = []
    for result in data.get('Results', [])[:max_results]:
        results.append(f"Заголовок: {result.get('Title', '')}")
        results.append(f"Ссылка: {result.get('FirstURL', '')}")
        results.append(f"Описание: {result.get('Text', '')}")
        results.append("-----------------")
    
    return '\n'.join(results)
```

**Преимущества:**
- ✅ Полностью бесплатный
- ✅ Не требует API ключа
- ✅ Хорошая приватность
- ✅ Стабильная работа

**Недостатки:**
- ❌ Ограниченное количество результатов
- ❌ Меньше детализации по сравнению с Google

### 2. **Selenium + BeautifulSoup** (Для скрапинга)

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def scrape_with_selenium(url: str) -> str:
    """
    Скрапинг веб-страниц с помощью Selenium.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Без GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        time.sleep(2)  # Ждем загрузки
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Извлекаем текст
        text_content = soup.get_text()
        
        return text_content[:2000]  # Первые 2000 символов
        
    finally:
        driver.quit()
```

**Преимущества:**
- ✅ Полный контроль над процессом
- ✅ Может обрабатывать JavaScript
- ✅ Бесплатный

**Недостатки:**
- ❌ Требует установки Chrome/ChromeDriver
- ❌ Медленнее API
- ❌ Может быть заблокирован сайтами

### 3. **Requests + BeautifulSoup** (Простой скрапинг)

```python
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def simple_scrape(url: str) -> str:
    """
    Простой скрапинг статических страниц.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Удаляем скрипты и стили
    for script in soup(["script", "style"]):
        script.decompose()
    
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    
    return text[:2000]
```

### 4. **Scrapy** (Продвинутый скрапинг)

```python
import scrapy
from scrapy.crawler import CrawlerProcess

class WebSpider(scrapy.Spider):
    name = 'web_spider'
    
    def __init__(self, start_urls=None, *args, **kwargs):
        super(WebSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls or []
    
    def parse(self, response):
        yield {
            'url': response.url,
            'title': response.css('title::text').get(),
            'content': response.css('body::text').get()
        }

def scrape_with_scrapy(urls: list) -> list:
    """
    Скрапинг с помощью Scrapy.
    """
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    process.crawl(WebSpider, start_urls=urls)
    process.start()
    
    return process.crawler.stats.get_stats()
```

## 🛠️ Интеграция в проект

### Обновление web_tools.py

```python
# Добавить в web_tools.py
class FreeWebSearchTools:
    """Бесплатные инструменты веб-поиска."""
    
    @tool("Бесплатный поиск")
    def free_search(self, query: str) -> str:
        """Поиск через DuckDuckGo."""
        return search_duckduckgo(query)
    
    @tool("Простой скрапинг")
    def simple_scrape(self, url: str) -> str:
        """Скрапинг статических страниц."""
        return simple_scrape(url)
```

### Обновление агентов

```python
# В crew файлах добавить бесплатные инструменты
from marketing_posts.core.web_tools import FreeWebSearchTools

free_tools = FreeWebSearchTools()

# Добавить к агентам
tools=[
    free_tools.free_search,
    free_tools.simple_scrape
]
```

## 📊 Сравнение методов

| Метод | Стоимость | Скорость | Качество | Сложность |
|-------|-----------|----------|----------|-----------|
| Serper API | 💰 Платный | ⚡ Быстрый | 🟢 Высокое | 🟢 Простая |
| DuckDuckGo | 🆓 Бесплатный | 🟡 Средняя | 🟡 Среднее | 🟢 Простая |
| Selenium | 🆓 Бесплатный | 🔴 Медленный | 🟢 Высокое | 🔴 Сложная |
| Requests+BS | 🆓 Бесплатный | 🟡 Средняя | 🟡 Среднее | 🟡 Средняя |
| Scrapy | 🆓 Бесплатный | ⚡ Быстрый | 🟢 Высокое | 🔴 Сложная |

## 🚀 Рекомендации

### Для разработки и тестирования:
1. **DuckDuckGo API** - лучший выбор
2. **Requests + BeautifulSoup** - для простого скрапинга

### Для продакшена:
1. **Serper API** - если бюджет позволяет
2. **DuckDuckGo + Selenium** - комбинированный подход

### Для масштабирования:
1. **Scrapy** - для больших объемов
2. **Прокси-ротация** - для обхода блокировок

## 🔧 Настройка бесплатных альтернатив

### 1. Установка зависимостей

```bash
# Для Selenium
pip install selenium webdriver-manager

# Для BeautifulSoup
pip install beautifulsoup4 lxml

# Для Scrapy
pip install scrapy
```

### 2. Настройка ChromeDriver

```python
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

# Автоматическая установка драйвера
driver = webdriver.Chrome(ChromeDriverManager().install())
```

### 3. Ротация User-Agent

```python
import random

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
]

headers = {'User-Agent': random.choice(user_agents)}
```

## ⚠️ Правовые аспекты

### Важные моменты:
1. **Respect robots.txt** - всегда проверяйте
2. **Rate limiting** - не перегружайте серверы
3. **Terms of Service** - соблюдайте условия использования
4. **GDPR/CCPA** - учитывайте законы о данных

### Рекомендации:
- Используйте задержки между запросами
- Ограничивайте количество запросов
- Логируйте все действия
- Получайте разрешение при необходимости

## 📈 Мониторинг и метрики

### Отслеживаемые метрики:
- Количество успешных запросов
- Время ответа
- Количество ошибок
- Использование ресурсов

### Алерты:
- Превышение лимитов
- Высокий процент ошибок
- Медленные ответы
- Блокировки IP

## 🔮 Будущие улучшения

### Планируемые функции:
1. **Кэширование результатов**
2. **Параллельная обработка**
3. **Умная ротация прокси**
4. **Машинное обучение для парсинга**
5. **Интеграция с базами данных**

### Архитектурные улучшения:
1. **Микросервисная архитектура**
2. **Очереди задач**
3. **Распределенное выполнение**
4. **API Gateway**
5. **Мониторинг в реальном времени** 