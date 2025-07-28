"""
Сохранение результатов для системы маркетинговых постов.
Обрабатывает сохранение результатов в файлы с правильной кодировкой.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass


@dataclass
class SaveResult:
    """Результат операции сохранения."""
    success: bool
    file_path: str
    error_message: Optional[str] = None


class ResultFormatter:
    """Обрабатывает форматирование результатов для разных типов вывода."""
    
    @staticmethod
    def format_task_result(task_result: Any) -> str:
        """Форматирует результат одной задачи для вывода."""
        if hasattr(task_result, 'raw') and task_result.raw:
            return str(task_result.raw)
        elif hasattr(task_result, 'result'):
            return str(task_result.result)
        elif hasattr(task_result, 'output'):
            return str(task_result.output)
        else:
            return str(task_result)
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Очищает и форматирует текст для вывода."""
        if not isinstance(text, str):
            return str(text)
        
        # Удаляем escape-последовательности
        text = text.replace('\\n', '\n')
        text = text.replace('\\"', '"')
        text = text.replace("\\'", "'")
        
        # Обрабатываем результаты-кортежи
        if text.startswith("('raw', '") and text.endswith("')"):
            start_idx = text.find("('raw', '") + 9
            end_idx = text.rfind("')")
            if start_idx > 8 and end_idx > start_idx:
                text = text[start_idx:end_idx]
                # Безопасное декодирование Unicode
                try:
                    text = text.encode('latin-1').decode('unicode_escape')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    pass
        
        return text


class ResultSaver:
    """
    Обрабатывает сохранение результатов выполнения crew в файлы.
    
    Предоставляет методы для сохранения результатов в разных форматах
    с правильной кодировкой и обработкой ошибок.
    """
    
    def __init__(self, base_dir: str = "results"):
        """
        Инициализирует сохранитель результатов.
        
        Args:
            base_dir: Базовая директория для сохранения результатов
        """
        self.base_dir = Path(base_dir)
        self.formatter = ResultFormatter()
    
    def create_results_directory(self) -> str:
        """
        Создает директорию результатов с временной меткой.
        
        Returns:
            Путь к созданной директории
        """
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        results_dir = self.base_dir / f"results_{timestamp}"
        
        # Создаем базовую директорию, если она не существует
        if not self.base_dir.exists():
            self.base_dir.mkdir(parents=True)
        
        # Создаем директорию с временной меткой
        if not results_dir.exists():
            results_dir.mkdir(parents=True)
        
        return str(results_dir)
    
    def save_marketing_results(
        self, 
        results: Any, 
        results_dir: Optional[str] = None
    ) -> SaveResult:
        """
        Сохраняет результаты маркетинговой стратегии в markdown файл.
        
        Args:
            results: Результаты выполнения crew
            results_dir: Директория для сохранения результатов
            
        Returns:
            SaveResult с статусом операции
        """
        try:
            if results_dir is None:
                results_dir = self.create_results_directory()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"marketing_strategy_results_{timestamp}.md"
            file_path = Path(results_dir) / filename
            
            with open(file_path, 'w', encoding='utf-8') as f:
                self._write_results_header(f)
                self._write_results_content(f, results)
            
            return SaveResult(
                success=True,
                file_path=str(file_path)
            )
            
        except Exception as e:
            return SaveResult(
                success=False,
                file_path=str(file_path) if 'file_path' in locals() else "",
                error_message=str(e)
            )
    
    def save_config_info(
        self, 
        config_info: Dict[str, Any], 
        results_dir: str
    ) -> SaveResult:
        """
        Сохраняет информацию о конфигурации в markdown файл.
        
        Args:
            config_info: Информация о конфигурации для сохранения
            results_dir: Директория для сохранения файла
            
        Returns:
            SaveResult с статусом операции
        """
        try:
            file_path = Path(results_dir) / "config_info.md"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("# Информация о конфигурации\n\n")
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"**Дата запуска:** {current_time}\n\n")
                
                for key, value in config_info.items():
                    f.write(f"**{key}:** {value}\n")
            
            return SaveResult(
                success=True,
                file_path=str(file_path)
            )
            
        except Exception as e:
            return SaveResult(
                success=False,
                file_path=str(file_path) if 'file_path' in locals() else "",
                error_message=str(e)
            )
    
    def save_error_report(
        self, 
        error_msg: str, 
        results_dir: Optional[str] = None,
        config_type: str = "Стандартная"
    ) -> SaveResult:
        """
        Сохраняет отчет об ошибке в markdown файл.
        
        Args:
            error_msg: Сообщение об ошибке для сохранения
            results_dir: Директория для сохранения файла
            config_type: Тип конфигурации, которая не сработала
            
        Returns:
            SaveResult с статусом операции
        """
        try:
            if results_dir is None:
                results_dir = self.create_results_directory()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"error_report_{timestamp}.md"
            file_path = Path(results_dir) / filename
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("# Отчет об ошибке выполнения\n\n")
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"**Дата:** {current_time}\n")
                f.write(f"**Ошибка:** {error_msg}\n")
                f.write(f"**Конфигурация:** {config_type}\n\n")
                f.write("## Рекомендации:\n")
                f.write("1. Проверьте логи выше\n")
                f.write("2. Попробуйте запустить снова\n")
                f.write("3. Обратитесь к разработчику\n")
            
            return SaveResult(
                success=True,
                file_path=str(file_path)
            )
            
        except Exception as e:
            return SaveResult(
                success=False,
                file_path=str(file_path) if 'file_path' in locals() else "",
                error_message=str(e)
            )
    
    def _write_results_header(self, file_handle) -> None:
        """Записывает заголовочную секцию файла результатов."""
        file_handle.write("# Результаты маркетинговой стратегии CrewAI\n\n")
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file_handle.write(f"**Дата создания:** {current_time}\n\n")
        file_handle.write("## Результаты выполнения задач\n\n")
    
    def _write_results_content(self, file_handle, results: Any) -> None:
        """Записывает основное содержимое файла результатов."""
        if hasattr(results, '__iter__') and not isinstance(results, str):
            for i, task_result in enumerate(results, 1):
                self._write_task_result(file_handle, i, task_result)
        else:
            file_handle.write("### Общий результат\n\n")
            formatted_result = self.formatter.clean_text(str(results))
            file_handle.write(f"{formatted_result}\n\n")
    
    def _write_task_result(
        self, 
        file_handle, 
        task_num: int, 
        task_result: Any
    ) -> None:
        """Записывает результат одной задачи в файл."""
        file_handle.write(f"### Задача {task_num}\n\n")
        
        # Получаем имя агента
        agent_name = "Неизвестно"
        if hasattr(task_result, 'agent') and task_result.agent:
            agent_name = getattr(task_result.agent, 'name', 'Неизвестно')
            if isinstance(agent_name, str):
                agent_name = agent_name.strip().replace('\n', ' ')
        
        file_handle.write(f"**Агент:** {agent_name}\n\n")
        
        # Получаем имя задачи
        task_name = "Неизвестно"
        if hasattr(task_result, 'name') and task_result.name:
            task_name = task_result.name
        
        file_handle.write(f"**Задача:** {task_name}\n\n")
        file_handle.write("**Результат:**\n\n")
        
        # Форматируем и записываем результат
        formatted_result = self.formatter.format_task_result(task_result)
        cleaned_result = self.formatter.clean_text(formatted_result)
        file_handle.write(f"{cleaned_result}\n\n")
        file_handle.write("---\n\n") 