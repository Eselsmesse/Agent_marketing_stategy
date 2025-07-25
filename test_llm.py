#!/usr/bin/env python
"""
Тестовый скрипт для проверки работы с DeepSeek LLM
"""
from dotenv import load_dotenv
from marketing_posts.config.llm_config import LLMConfig, AVAILABLE_MODELS

load_dotenv()


def test_deepseek_llm():
    """Тестирование DeepSeek LLM"""
    print("=== Тестирование DeepSeek LLM ===\n")
    
    # Тест DeepSeek
    print("1. Тестирование подключения к DeepSeek...")
    try:
        llm = LLMConfig.get_deepseek_llm(model="deepseek-chat")
        print("✅ DeepSeek подключен успешно")
        print(f"   Модель: {llm.model}")
        print(f"   API URL: {llm.base_url}")
    except Exception as e:
        print(f"❌ Ошибка DeepSeek: {e}")
        return False
    
    print()
    
    # Показать доступные модели
    print("2. Доступные модели DeepSeek:")
    for provider, models in AVAILABLE_MODELS.items():
        print(f"   {provider.upper()}:")
        for model_id, model_name in models.items():
            print(f"     - {model_id}: {model_name}")
    
    return True


def test_simple_generation():
    """Тестирование простой генерации текста"""
    print("\n=== Тестирование генерации текста ===\n")
    
    test_prompt = "Напиши короткое приветствие на русском языке."
    
    # Тест с DeepSeek
    try:
        print("Отправка запроса к DeepSeek...")
        deepseek_llm = LLMConfig.get_deepseek_llm(model="deepseek-chat")
        response = deepseek_llm.invoke(test_prompt)
        print(f"✅ DeepSeek ответ: {response}")
        return True
    except Exception as e:
        print(f"❌ Ошибка DeepSeek генерации: {e}")
        return False


def test_api_key():
    """Проверка наличия API ключа"""
    import os
    print("=== Проверка API ключа ===\n")
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if api_key:
        print(f"✅ API ключ найден: {api_key[:10]}...")
        return True
    else:
        print("❌ API ключ DEEPSEEK_API_KEY не найден в переменных окружения")
        print("   Создайте файл .env на основе env_example.txt")
        return False


if __name__ == "__main__":
    print("🧪 Тестирование DeepSeek LLM интеграции\n")
    
    # Проверка API ключа
    if not test_api_key():
        exit(1)
    
    # Тест подключения
    if not test_deepseek_llm():
        exit(1)
    
    # Тест генерации
    if not test_simple_generation():
        print("\n⚠️  Генерация не удалась, но подключение работает")
        print("   Проверьте правильность API ключа и доступность сервиса")
    else:
        print("\n🎉 Все тесты прошли успешно!") 