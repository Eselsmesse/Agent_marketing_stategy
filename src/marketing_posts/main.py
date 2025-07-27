#!/usr/bin/env python
import sys
import os
import argparse
import yaml
from datetime import datetime
from dotenv import load_dotenv
from marketing_posts.crew import MarketingPostsCrew

load_dotenv()


def create_results_directory():
    """Создает датированную папку для результатов внутри results/"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    results_dir = f"results/results_{timestamp}"
    
    # Создаем основную папку results если её нет
    if not os.path.exists("results"):
        os.makedirs("results")
        print(f"📁 Создана основная папка: results/")
    
    # Создаем датированную папку если её нет
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        print(f"📁 Создана папка для результатов: {results_dir}")
    
    return results_dir


def save_additional_info(results_dir, gaming_config=None, use_gaming_config=False):
    """Сохраняет дополнительную информацию в папку результатов"""
    if results_dir is None:
        return
    
    # Сохраняем информацию о конфигурации
    config_info = f"""
# Информация о конфигурации

**Дата запуска:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Тип конфигурации:** {'Игровая' if use_gaming_config else 'Стандартная'}

## Параметры запуска:
- LLM провайдер: DeepSeek
- Конфигурация: {'Игровая (Puzzle & Survival Bot)' if use_gaming_config else 'Стандартная (CrewAI)'}

"""
    
    if gaming_config and use_gaming_config:
        project_info = gaming_config.get('project_info', {})
        config_info += f"""
## Игровая конфигурация:
- **Продукт:** {project_info.get('product_name', 'N/A')}
- **Игра:** {project_info.get('game_name', 'N/A')}
- **Целевые регионы:** {', '.join(project_info.get('target_regions', []))}
- **Языки:** {', '.join(project_info.get('target_languages', []))}
- **Основные каналы:** {', '.join(project_info.get('primary_channels', []))}

## Ключевые особенности:
{chr(10).join([f"- {feature}" for feature in gaming_config.get('key_features', [])])}

## Правовые аспекты:
{chr(10).join([f"- {consideration}" for consideration in gaming_config.get('legal_considerations', [])])}

## Рыночные возможности:
{chr(10).join([f"- {opportunity}" for opportunity in gaming_config.get('market_opportunities', [])])}

## Вызовы:
{chr(10).join([f"- {challenge}" for challenge in gaming_config.get('challenges', [])])}

## Метрики успеха:
{chr(10).join([f"- {metric}" for metric in gaming_config.get('success_metrics', [])])}
"""
    
    config_path = os.path.join(results_dir, "config_info.md")
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_info)
    
    print(f"📋 Информация о конфигурации сохранена в: {config_path}")


def save_results_to_md(results, results_dir=None, filename=None):
    """
    Сохраняет результаты работы crew в .md файл в датированной папке
    
    Args:
        results: Результаты выполнения crew
        results_dir: Папка для сохранения (если None, создается автоматически)
        filename: Имя файла (если None, генерируется автоматически)
    """
    # Создаем папку для результатов если не передана
    if results_dir is None:
        results_dir = create_results_directory()
    
    # Генерируем имя файла если не передано
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"marketing_strategy_results_{timestamp}.md"
    
    # Полный путь к файлу
    file_path = os.path.join(results_dir, filename)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("# Результаты маркетинговой стратегии CrewAI\n\n")
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"**Дата создания:** {current_time}\n\n")
        
        f.write("## Результаты выполнения задач\n\n")
        
        # Проверяем тип результатов
        if hasattr(results, '__iter__') and not isinstance(results, str):
            # Если results - это список или итерируемый объект
            for i, task_result in enumerate(results, 1):
                f.write(f"### Задача {i}\n\n")
                
                # Получаем имя агента
                agent_name = "Неизвестно"
                if hasattr(task_result, 'agent') and task_result.agent:
                    agent_name = getattr(task_result.agent, 'name', 'Неизвестно')
                    # Убираем лишние символы из имени агента
                    if isinstance(agent_name, str):
                        agent_name = agent_name.strip().replace('\n', ' ')
                
                f.write(f"**Агент:** {agent_name}\n\n")
                
                # Получаем имя задачи
                task_name = "Неизвестно"
                if hasattr(task_result, 'name') and task_result.name:
                    task_name = task_result.name
                
                f.write(f"**Задача:** {task_name}\n\n")
                f.write("**Результат:**\n\n")
                
                # Получаем результат в читаемом формате
                result_text = ""
                if hasattr(task_result, 'raw') and task_result.raw:
                    # Используем raw результат если доступен
                    result_text = str(task_result.raw)
                elif hasattr(task_result, 'result'):
                    result_text = str(task_result.result)
                elif hasattr(task_result, 'output'):
                    result_text = str(task_result.output)
                else:
                    result_text = str(task_result)
                
                # Очищаем результат от лишних символов и форматируем
                if isinstance(result_text, str):
                    # Убираем лишние экранирования и символы
                    result_text = result_text.replace('\\n', '\n')
                    result_text = result_text.replace('\\"', '"')
                    result_text = result_text.replace("\\'", "'")
                    
                    # Если результат содержит tuple, извлекаем нужную часть
                    if result_text.startswith("('raw', '") and result_text.endswith("')"):
                        # Извлекаем содержимое из tuple
                        start_idx = result_text.find("('raw', '") + 9
                        end_idx = result_text.rfind("')")
                        if start_idx > 8 and end_idx > start_idx:
                            result_text = result_text[start_idx:end_idx]
                            # Простое декодирование без сложной логики
                            try:
                                result_text = result_text.encode('latin-1').decode('unicode_escape')
                            except:
                                # Если не получается, оставляем как есть
                                pass
                
                f.write(f"{result_text}\n\n")
                f.write("---\n\n")
        else:
            # Если results - это строка или другой тип
            f.write("### Общий результат\n\n")
            result_text = str(results)
            
            # Очищаем результат от лишних символов
            if isinstance(result_text, str):
                result_text = result_text.replace('\\n', '\n')
                result_text = result_text.replace('\\"', '"')
                result_text = result_text.replace("\\'", "'")
            
            f.write(f"{result_text}\n\n")
    
    print(f"📄 Результаты сохранены в файл: {file_path}")
    return file_path


def save_error_report(error_msg, results_dir=None, use_gaming_config=False):
    """Сохраняет отчет об ошибке в датированную папку"""
    if results_dir is None:
        results_dir = create_results_directory()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    error_filename = f"error_report_{timestamp}.md"
    error_path = os.path.join(results_dir, error_filename)
    
    error_report = f"""
# Отчет об ошибке выполнения

**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Ошибка:** {error_msg}

## Что произошло:
Система выполнила часть задач, но произошла ошибка при обработке результатов.

## Рекомендации:
1. Проверьте логи выше - там могут быть полезные результаты
2. Попробуйте запустить снова
3. Обратитесь к разработчику для исправления ошибки

## Техническая информация:
- Конфигурация: {'Игровая' if use_gaming_config else 'Стандартная'}
- Папка результатов: {results_dir}
"""
    
    with open(error_path, 'w', encoding='utf-8') as f:
        f.write(error_report)
    
    print(f"⚠️ Отчет об ошибке сохранен в: {error_path}")
    return error_path


def load_gaming_config():
    """Загружает конфигурацию игрового проекта"""
    try:
        config_path = 'src/marketing_posts/config/gaming_inputs.yaml'
        print(f"📂 Загружаю конфигурацию из: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        print(f"✅ Конфигурация загружена успешно")
        print(f"📋 Доступные ключи: {list(config.keys())}")
        
        if 'project_info' in config:
            project_info = config['project_info']
            print(f"🎮 Информация о проекте: {project_info.get('product_name', 'N/A')}")
        
        return config
        
    except FileNotFoundError:
        print("⚠️ Файл gaming_inputs.yaml не найден. Используются стандартные данные.")
        return None
    except yaml.YAMLError as e:
        print(f"❌ Ошибка парсинга YAML: {e}")
        return None
    except Exception as e:
        print(f"❌ Неожиданная ошибка при загрузке конфигурации: {e}")
        return None


def run(
    llm_provider: str = "deepseek", 
    llm_model: str = None, 
    save_output: bool = True,
    use_gaming_config: bool = False
):
    """
    Запуск маркетинговой стратегии с DeepSeek LLM провайдером
    
    Args:
        llm_provider: Провайдер LLM (только "deepseek")
        llm_model: Конкретная модель для использования
        save_output: Сохранять ли результаты в .md файл
        use_gaming_config: Использовать ли игровую конфигурацию
    """
    
    # Создаем папку для результатов заранее
    results_dir = None
    if save_output:
        results_dir = create_results_directory()
    
    # Загружаем игровую конфигурацию если нужно
    gaming_config = None
    if use_gaming_config:
        gaming_config = load_gaming_config()
    
    # Формируем входные данные
    if gaming_config:
        # Используем игровую конфигурацию
        project_info = gaming_config.get('project_info', {})
        inputs = {
            'customer_domain': 'zeonbot.com',
            'project_description': gaming_config.get('product_description', ''),
            'target_regions': project_info.get('target_regions', []),
            'target_languages': project_info.get('target_languages', []),
            'primary_channels': project_info.get('primary_channels', []),
            'key_features': gaming_config.get('key_features', []),
            'legal_considerations': gaming_config.get('legal_considerations', []),
            'market_opportunities': gaming_config.get('market_opportunities', []),
            'challenges': gaming_config.get('challenges', []),
            'success_metrics': gaming_config.get('success_metrics', [])
        }
        print("🎮 Используется игровая конфигурация для Puzzle & Survival Bot")
    else:
        # Стандартная конфигурация CrewAI
        inputs = {
            'customer_domain': 'crewai.com',
            'project_description': """
CrewAI, a leading provider of multi-agent systems, aims to revolutionize 
marketing automation for its enterprise clients. This project involves 
developing an innovative marketing strategy to showcase CrewAI's advanced 
AI-driven solutions, emphasizing ease of use, scalability, and integration 
capabilities. The campaign will target tech-savvy decision-makers in medium 
to large enterprises, highlighting success stories and the transformative 
potential of CrewAI's platform.

Customer Domain: AI and Automation Solutions
Project Overview: Creating a comprehensive marketing campaign to boost 
awareness and adoption of CrewAI's services among enterprise clients.
"""
        }
        print("🏢 Используется стандартная конфигурация CrewAI")
    
    print(f"Используется LLM провайдер: {llm_provider}")
    if llm_model:
        print(f"Модель: {llm_model}")
    
    crew_instance = MarketingPostsCrew(
        llm_provider=llm_provider,
        llm_model=llm_model,
        use_gaming_config=use_gaming_config
    )
    
    try:
        results = crew_instance.crew().kickoff(inputs=inputs)
        print("✅ Все задачи выполнены успешно!")
        
        if save_output:
            save_results_to_md(results, results_dir=results_dir)
            save_additional_info(results_dir, gaming_config, use_gaming_config)
        
        return results
        
    except Exception as e:
        print(f"⚠️ Произошла ошибка: {e}")
        print("Попытка сохранить частичные результаты...")
        
        if save_output:
            save_error_report(str(e), results_dir=results_dir, use_gaming_config=use_gaming_config)
        
        return None


def train(llm_provider: str = "deepseek", llm_model: str = None):
    """
    Обучение crew для заданного количества итераций.
    
    Args:
        llm_provider: Провайдер LLM (только "deepseek")
        llm_model: Конкретная модель для использования
    """
    inputs = {
        'customer_domain': 'crewai.com',
        'project_description': """
CrewAI, a leading provider of multi-agent systems, aims to revolutionize 
marketing automation for its enterprise clients. This project involves 
developing an innovative marketing strategy to showcase CrewAI's advanced 
AI-driven solutions, emphasizing ease of use, scalability, and integration 
capabilities. The campaign will target tech-savvy decision-makers in medium 
to large enterprises, highlighting success stories and the transformative 
potential of CrewAI's platform.

Customer Domain: AI and Automation Solutions
Project Overview: Creating a comprehensive marketing campaign to boost 
awareness and adoption of CrewAI's services among enterprise clients.
"""
    }
    try:
        print(f"Обучение с LLM провайдером: {llm_provider}")
        if llm_model:
            print(f"Модель: {llm_model}")
            
        MarketingPostsCrew(
            llm_provider=llm_provider,
            llm_model=llm_model
        ).crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def main():
    """Основная функция с поддержкой аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description="Marketing Posts Crew с DeepSeek LLM"
    )
    parser.add_argument(
        "--provider", 
        choices=["deepseek"],
        default="deepseek",
        help="LLM провайдер (только deepseek)"
    )
    parser.add_argument(
        "--model",
        help="Конкретная модель DeepSeek для использования"
    )
    parser.add_argument(
        "--train",
        type=int,
        help="Количество итераций для обучения"
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Не сохранять результаты в .md файл"
    )
    parser.add_argument(
        "--gaming",
        action="store_true",
        help="Использовать игровую конфигурацию для Puzzle & Survival Bot"
    )
    
    args = parser.parse_args()
    
    if args.train:
        train(args.provider, args.model)
    else:
        run(
            args.provider, 
            args.model, 
            save_output=not args.no_save, 
            use_gaming_config=args.gaming
        )


if __name__ == "__main__":
    main()
