"""
Основной модуль для запуска системы маркетинговых постов.
Использует новую архитектуру с модульной структурой.
"""

import argparse
from typing import Dict, Any, Optional

from marketing_posts.core.base_crew import CrewConfig
from marketing_posts.core.config_manager import ConfigManager
from marketing_posts.core.result_saver import ResultSaver
from marketing_posts.core.crew_factory import CrewFactory, CrewBuilder
from marketing_posts.crews.standard_crew import StandardCrew
from marketing_posts.crews.gaming_crew import GamingCrew


class MarketingPostsRunner:
    """
    Основной класс для запуска системы маркетинговых постов.
    
    Использует новую архитектуру с разделением ответственности
    и применением паттернов проектирования.
    """
    
    def __init__(self):
        """Инициализирует runner системы."""
        self.config_manager = ConfigManager()
        self.result_saver = ResultSaver()
        self.crew_factory = CrewFactory(self.config_manager)
        self._register_crew_types()
    
    def _register_crew_types(self) -> None:
        """Регистрирует доступные типы crew в фабрике."""
        self.crew_factory.register_crew_type('standard', StandardCrew)
        self.crew_factory.register_crew_type('gaming', GamingCrew)
    
    def load_gaming_config(self) -> Dict[str, Any]:
        """
        Загружает игровую конфигурацию.
        
        Returns:
            Словарь с игровой конфигурацией
        """
        try:
            return self.config_manager.get_gaming_config()
        except Exception as e:
            print(f"⚠️ Ошибка загрузки игровой конфигурации: {e}")
            return {}
    
    def create_crew_config(
        self, 
        crew_type: str, 
        llm_provider: str = "deepseek",
        llm_model: Optional[str] = None,
        verbose: bool = True
    ) -> CrewConfig:
        """
        Создает конфигурацию crew.
        
        Args:
            crew_type: Тип crew (standard/gaming)
            llm_provider: Провайдер LLM
            llm_model: Модель LLM
            verbose: Режим подробного вывода
            
        Returns:
            Конфигурация crew
        """
        if crew_type == 'gaming':
            return (CrewBuilder.create_gaming_config()
                    .with_llm_provider(llm_provider)
                    .with_llm_model(llm_model)
                    .with_verbose(verbose)
                    .build())
        else:
            return (CrewBuilder.create_standard_config()
                    .with_llm_provider(llm_provider)
                    .with_llm_model(llm_model)
                    .with_verbose(verbose)
                    .build())
    
    def run_crew(
        self, 
        crew_type: str, 
        inputs: Dict[str, Any],
        llm_provider: str = "deepseek",
        llm_model: Optional[str] = None,
        verbose: bool = True
    ) -> Any:
        """
        Запускает crew с заданными параметрами.
        
        Args:
            crew_type: Тип crew для запуска
            inputs: Входные данные
            llm_provider: Провайдер LLM
            llm_model: Модель LLM
            verbose: Режим подробного вывода
            
        Returns:
            Результаты выполнения crew
        """
        try:
            # Создаем конфигурацию
            config = self.create_crew_config(
                crew_type, llm_provider, llm_model, verbose
            )
            
            # Создаем crew через фабрику
            crew = self.crew_factory.create_crew(crew_type, config)
            
            # Выполняем crew
            results = crew.execute(inputs)
            
            return results
            
        except Exception as e:
            print(f"❌ Ошибка выполнения crew: {e}")
            raise
    
    def save_results(
        self, 
        results: Any, 
        crew_type: str,
        config_info: Dict[str, Any]
    ) -> None:
        """
        Сохраняет результаты выполнения.
        
        Args:
            results: Результаты выполнения
            crew_type: Тип crew
            config_info: Информация о конфигурации
        """
        try:
            # Создаем директорию результатов
            results_dir = self.result_saver.create_results_directory()
            
            # Сохраняем результаты
            save_result = self.result_saver.save_marketing_results(
                results, results_dir
            )
            
            if save_result.success:
                print(f"✅ Результаты сохранены: {save_result.file_path}")
                
                # Сохраняем информацию о конфигурации
                config_save = self.result_saver.save_config_info(
                    config_info, results_dir
                )
                
                if config_save.success:
                    print("✅ Информация о конфигурации сохранена")
                else:
                    error_msg = config_save.error_message
                    print(f"⚠️ Ошибка сохранения конфигурации: {error_msg}")
            else:
                error_msg = save_result.error_message
                print(f"❌ Ошибка сохранения результатов: {error_msg}")
                
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
    
    def run(
        self, 
        crew_type: str = "standard",
        use_gaming_config: bool = False,
        llm_provider: str = "deepseek",
        llm_model: Optional[str] = None,
        verbose: bool = True
    ) -> None:
        """
        Основной метод запуска системы.
        
        Args:
            crew_type: Тип crew для запуска
            use_gaming_config: Использовать игровую конфигурацию
            llm_provider: Провайдер LLM
            llm_model: Модель LLM
            verbose: Режим подробного вывода
        """
        try:
            print("🚀 Запуск системы маркетинговых постов")
            print(f"📋 Тип crew: {crew_type}")
            print(f"🤖 Провайдер LLM: {llm_provider}")
            
            # Определяем тип crew
            actual_crew_type = 'gaming' if use_gaming_config else crew_type
            
            # Подготавливаем входные данные
            inputs = {}
            if use_gaming_config:
                gaming_config = self.load_gaming_config()
                if gaming_config:
                    inputs = gaming_config.get('project_info', {})
                    print("🎮 Загружена игровая конфигурация")
                else:
                    print("⚠️ Игровая конфигурация не загружена, "
                          "используются стандартные данные")
            
            # Запускаем crew
            results = self.run_crew(
                actual_crew_type, inputs, llm_provider, llm_model, verbose
            )
            
            # Получаем информацию о конфигурации
            config = self.create_crew_config(
                actual_crew_type, llm_provider, llm_model, verbose
            )
            config_info = {
                'crew_type': actual_crew_type,
                'llm_provider': config.llm_provider,
                'llm_model': config.llm_model,
                'agents_config': config.agents_config,
                'tasks_config': config.tasks_config,
                'use_gaming_config': use_gaming_config
            }
            
            # Сохраняем результаты
            self.save_results(results, actual_crew_type, config_info)
            
            print("✅ Выполнение завершено успешно")
            
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")
            
            # Сохраняем отчет об ошибке
            try:
                config_type = 'Игровая' if use_gaming_config else 'Стандартная'
                error_save = self.result_saver.save_error_report(
                    str(e), 
                    config_type=config_type
                )
                if error_save.success:
                    print(f"📄 Отчет об ошибке сохранен: "
                          f"{error_save.file_path}")
            except Exception as save_error:
                print(f"❌ Ошибка сохранения отчета: {save_error}")


def main():
    """Точка входа в приложение."""
    parser = argparse.ArgumentParser(
        description="Система маркетинговых постов CrewAI"
    )
    
    parser.add_argument(
        '--crew-type',
        choices=['standard', 'gaming'],
        default='standard',
        help='Тип crew для запуска (default: standard)'
    )
    
    parser.add_argument(
        '--use-gaming-config',
        action='store_true',
        help='Использовать игровую конфигурацию'
    )
    
    parser.add_argument(
        '--llm-provider',
        default='deepseek',
        help='Провайдер LLM (default: deepseek)'
    )
    
    parser.add_argument(
        '--llm-model',
        help='Модель LLM (опционально)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        default=True,
        help='Подробный вывод (default: True)'
    )
    
    args = parser.parse_args()
    
    # Создаем и запускаем runner
    runner = MarketingPostsRunner()
    runner.run(
        crew_type=args.crew_type,
        use_gaming_config=args.use_gaming_config,
        llm_provider=args.llm_provider,
        llm_model=args.llm_model,
        verbose=args.verbose
    )


if __name__ == "__main__":
    main() 