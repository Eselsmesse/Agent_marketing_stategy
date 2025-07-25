#!/usr/bin/env python
import sys
import argparse
from datetime import datetime
from dotenv import load_dotenv
from marketing_posts.crew import MarketingPostsCrew

load_dotenv()


def save_results_to_md(results, filename=None):
    """
    Сохраняет результаты работы crew в .md файл
    
    Args:
        results: Результаты выполнения crew
        filename: Имя файла (если None, генерируется автоматически)
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"marketing_strategy_results_{timestamp}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
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
                
                f.write(f"**Агент:** {agent_name}\n\n")
                f.write("**Результат:**\n\n")
                
                # Получаем результат
                result_text = ""
                if hasattr(task_result, 'result'):
                    result_text = str(task_result.result)
                elif hasattr(task_result, 'output'):
                    result_text = str(task_result.output)
                else:
                    result_text = str(task_result)
                
                f.write(f"{result_text}\n\n")
                f.write("---\n\n")
        else:
            # Если results - это строка или другой тип
            f.write("### Общий результат\n\n")
            f.write(f"{str(results)}\n\n")
    
    print(f"Результаты сохранены в файл: {filename}")
    return filename


def run(
    llm_provider: str = "deepseek", 
    llm_model: str = None, 
    save_output: bool = True
):
    """
    Запуск маркетинговой стратегии с DeepSeek LLM провайдером
    
    Args:
        llm_provider: Провайдер LLM (только "deepseek")
        llm_model: Конкретная модель для использования
        save_output: Сохранять ли результаты в .md файл
    """
    # Replace with your inputs, it will automatically interpolate any tasks 
    # and agents information
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
    
    print(f"Используется LLM провайдер: {llm_provider}")
    if llm_model:
        print(f"Модель: {llm_model}")
    
    crew_instance = MarketingPostsCrew(
        llm_provider=llm_provider,
        llm_model=llm_model
    )
    
    results = crew_instance.crew().kickoff(inputs=inputs)
    
    if save_output:
        save_results_to_md(results)
    
    return results


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
    
    args = parser.parse_args()
    
    if args.train:
        train(args.provider, args.model)
    else:
        run(args.provider, args.model, save_output=not args.no_save)


if __name__ == "__main__":
    main()
