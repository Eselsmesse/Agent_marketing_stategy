# Changelog

## [0.3.1] - 2024-12-19

### Fixed
- Исправлена проблема с зависимостями - убрана несуществующая библиотека `langchain_llms`
- Создана кастомная реализация `DeepSeekLLM` для работы с DeepSeek API
- Обновлены зависимости для использования только доступных библиотек

### Changed
- Заменена зависимость `langchain_llms` на `langchain-community` и `requests`
- Создан класс `DeepSeekLLM` с прямой интеграцией к DeepSeek API
- Обновлен тестовый скрипт для проверки новой реализации

### Dependencies
- Убрана: `langchain_llms>=0.1.0`
- Добавлена: `langchain-community>=0.2.0`
- Добавлена: `requests>=2.31.0`

## [0.3.0] - 2024-12-19

### Changed
- **BREAKING CHANGE**: Убрана поддержка OpenAI и других LLM провайдеров
- DeepSeek теперь является единственным поддерживаемым LLM провайдером
- Обновлена конфигурация по умолчанию для использования DeepSeek
- Упрощены аргументы командной строки (убрана опция --provider)
- Обновлена документация для отражения использования только DeepSeek

### Removed
- Зависимость от `langchain_openai`
- Поддержка OpenAI API ключей
- Опция выбора провайдера LLM

### Dependencies
- Оставлена только зависимость `langchain_llms>=0.1.0` для DeepSeek
- Оставлена зависимость `langchain>=0.2.0`
- Оставлена зависимость `python-dotenv>=1.0.0`

### Usage
Теперь используется только DeepSeek:

```bash
# DeepSeek (по умолчанию)
uv run marketing_posts

# Конкретная модель DeepSeek
uv run marketing_posts --model deepseek-chat

# DeepSeek Coder
uv run marketing_posts --model deepseek-coder

# Обучение
uv run marketing_posts --train 5
```

## [0.2.0] - 2024-12-19

### Added
- Поддержка DeepSeek LLM через библиотеку `langchain_llms`
- Конфигурационный класс `LLMConfig` для управления различными LLM провайдерами
- Аргументы командной строки для выбора LLM провайдера и модели
- Тестовый скрипт `test_llm.py` для проверки работы с различными провайдерами
- Файл `env_example.txt` с примерами переменных окружения

### Changed
- Обновлен `pyproject.toml` с новыми зависимостями
- Модифицирован класс `MarketingPostsCrew` для поддержки выбора LLM
- Обновлен `main.py` с поддержкой аргументов командной строки
- Обновлен `README.md` с документацией по использованию различных LLM

### Dependencies
- Добавлена зависимость `langchain_llms>=0.1.0`
- Добавлена зависимость `langchain>=0.2.0`
- Добавлена зависимость `python-dotenv>=1.0.0`

### Usage
Теперь можно использовать различные LLM провайдеры:

```bash
# OpenAI (по умолчанию)
uv run marketing_posts

# DeepSeek
uv run marketing_posts --provider deepseek

# Конкретная модель
uv run marketing_posts --provider deepseek --model deepseek-chat
``` 