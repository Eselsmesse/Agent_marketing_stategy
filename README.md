# 🚀 Система маркетинговых постов с CrewAI

Современная система для создания маркетинговых стратегий с использованием CrewAI и DeepSeek LLM.

## 📋 Особенности

- ✅ **Модульная архитектура** - легко расширяемая система
- ✅ **Поддержка разных типов crew** - стандартный и игровой маркетинг
- ✅ **Веб-инструменты** - поиск и анализ информации через Serper API
- ✅ **Валидация конфигураций** - надежная обработка ошибок
- ✅ **Автоматическое сохранение результатов** - с временными метками
- ✅ **Полная типизация** - type hints для всех компонентов
- ✅ **Документация на русском** - понятные docstring

## 🏗️ Архитектура

```
src/marketing_posts/
├── core/                    # Основные модули
│   ├── base_crew.py        # Абстрактный базовый класс
│   ├── config_manager.py   # Менеджер конфигураций
│   ├── result_saver.py     # Сохранение результатов
│   ├── crew_factory.py     # Фабрика crew
│   └── web_tools.py        # Веб-инструменты для аналитики
├── crews/                   # Конкретные реализации
│   ├── standard_crew.py    # Стандартный crew
│   └── gaming_crew.py      # Игровой crew
├── config/                  # Конфигурации
│   ├── agents.yaml
│   ├── tasks.yaml
│   ├── agents_gaming.yaml
│   ├── tasks_gaming.yaml
│   └── gaming_inputs.yaml
└── main.py                 # Основной модуль
```

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
# Клонирование репозитория
git clone <repository-url>
cd marketing_strategy

# Установка зависимостей
uv sync
```

### 2. Настройка переменных окружения

Создайте файл `.env`:

```bash
# Обязательные API ключи
DEEPSEEK_API_KEY=your_deepseek_api_key
SERPER_API_KEY=your_serper_api_key
```

**Получение API ключей:**
- **DeepSeek**: https://platform.deepseek.com/
- **Serper**: https://serper.dev/ (для веб-поиска)

### 3. Запуск

#### Стандартный маркетинг:
```bash
python -m src.marketing_posts.main --crew-type standard
```

#### Игровой маркетинг:
```bash
python -m src.marketing_posts.main --crew-type gaming --use-gaming-config
```

#### Программное использование:
```python
from marketing_posts.main import MarketingPostsRunner

runner = MarketingPostsRunner()
runner.run(
    crew_type='gaming',
    use_gaming_config=True,
    llm_provider='deepseek'
)
```

## 📖 Использование

### Параметры командной строки

- `--crew-type`: Тип crew (`standard` или `gaming`)
- `--use-gaming-config`: Использовать игровую конфигурацию
- `--llm-provider`: Провайдер LLM (по умолчанию: `deepseek`)
- `--llm-model`: Модель LLM (опционально)
- `--verbose`: Подробный вывод

### Примеры

```bash
# Стандартный маркетинг
python -m src.marketing_posts.main

# Игровой маркетинг с конфигурацией
python -m src.marketing_posts.main --crew-type gaming --use-gaming-config

# С указанием модели
python -m src.marketing_posts.main --llm-model deepseek-chat

# Без подробного вывода
python -m src.marketing_posts.main --crew-type standard --verbose false
```

## 🔧 Конфигурация

### Конфигурационные файлы

- `agents.yaml` - стандартные агенты
- `tasks.yaml` - стандартные задачи
- `agents_gaming.yaml` - игровые агенты
- `tasks_gaming.yaml` - игровые задачи
- `gaming_inputs.yaml` - игровые входные данные

### Веб-инструменты

Система включает специализированные инструменты для аналитики:

#### Доступные инструменты поиска:
- `search_internet` - общий поиск информации
- `search_competitors` - поиск конкурентов
- `analyze_market` - анализ рынка
- `research_product` - исследование продукта
- `search_trends` - поиск трендов
- `analyze_audience` - анализ аудитории
- `search_marketing_strategies` - поиск маркетинговых стратегий
- `research_gaming_industry` - исследование игровой индустрии
- `search_legal_info` - поиск правовой информации

#### Инструменты анализа:
- `analyze_webpage` - анализ веб-страниц

## 🛠️ Разработка

### Добавление нового типа crew

1. Создайте новый класс в `src/marketing_posts/crews/`
2. Наследуйтесь от `BaseCrew`
3. Реализуйте абстрактные методы
4. Зарегистрируйте в `CrewFactory`

```python
class EcommerceCrew(BaseCrew):
    """Crew для e-commerce маркетинга."""
    
    def _validate_config(self) -> None:
        # Валидация конфигурации
        pass
    
    def _initialize_crew(self) -> None:
        # Инициализация
        pass
    
    def get_agents(self) -> List[Agent]:
        # Возврат агентов
        pass
    
    def get_tasks(self) -> List[Task]:
        # Возврат задач
        pass
```

### Добавление новых агентов

1. Создайте метод агента
2. Добавьте конфигурацию в соответствующий YAML файл
3. Обновите методы `get_agents()`
4. Добавьте необходимые веб-инструменты

### Добавление новых задач

1. Создайте метод задачи
2. Добавьте конфигурацию в соответствующий YAML файл
3. Обновите методы `get_tasks()`

## 🌐 Веб-инструменты

### Интеграция с Serper API

Система использует Serper API для веб-поиска и анализа. Это позволяет агентам:

- Искать актуальную информацию в интернете
- Анализировать конкурентов
- Исследовать рынки и тренды
- Собирать данные о продуктах

### Альтернативы платным сервисам

Для экономии средств можно использовать бесплатные альтернативы:

- **DuckDuckGo API** - бесплатный поиск
- **Selenium + BeautifulSoup** - скрапинг веб-страниц
- **Requests + BeautifulSoup** - простой скрапинг
- **Scrapy** - продвинутый скрапинг

Подробная документация: [docs/web_scraping_alternatives.md](docs/web_scraping_alternatives.md)

## 🚀 Развертывание

### Docker

```dockerfile
FROM python:3.10-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "-m", "src.marketing_posts.main"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  marketing-posts:
    build: .
    environment:
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
      - SERPER_API_KEY=${SERPER_API_KEY}
    volumes:
      - ./results:/app/results
```

## 📝 Документация

- [Архитектура системы](ARCHITECTURE_README.md)
- [Веб-скрапинг альтернативы](docs/web_scraping_alternatives.md)
- [API документация](docs/api.md)
- [Руководство разработчика](docs/developer.md)

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Добавьте тесты
5. Создайте pull request

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 🆘 Поддержка

Если у вас есть вопросы или проблемы:

1. Проверьте [Issues](https://github.com/your-repo/issues)
2. Создайте новое issue с подробным описанием
3. Обратитесь к [документации](docs/)

## 🔮 Планы развития

### Краткосрочные (1-2 месяца)
- [ ] Добавление тестов
- [ ] Интеграция с CI/CD
- [ ] Мониторинг и алерты
- [ ] Бесплатные альтернативы веб-поиска

### Среднесрочные (3-6 месяцев)
- [ ] Поддержка MCP протоколов
- [ ] Асинхронное выполнение
- [ ] Веб-интерфейс
- [ ] Расширенные веб-инструменты

### Долгосрочные (6+ месяцев)
- [ ] Машинное обучение для оптимизации
- [ ] Распределенное выполнение
- [ ] Интеграция с внешними системами
- [ ] Продвинутый веб-скрапинг
