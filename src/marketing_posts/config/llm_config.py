import os
import requests
from typing import Optional, List, Any
from langchain_core.language_models import BaseLanguageModel
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.prompts import BasePromptTemplate
from pydantic import Field
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()


class DeepSeekLLM(BaseLanguageModel):
    """Кастомная реализация DeepSeek LLM"""
    
    model: str = Field(default="deepseek-reasoner")
    temperature: float = Field(default=1.0)
    api_key: Optional[str] = Field(default=None)
    base_url: str = Field(default="https://api.deepseek.com/v1")
    
    def __init__(self, **kwargs):
        # Получаем API ключ из переменных окружения если не передан или None
        if 'api_key' not in kwargs or kwargs.get('api_key') is None:
            kwargs['api_key'] = os.getenv("DEEPSEEK_API_KEY")
        
        if not kwargs.get('api_key'):
            raise ValueError(
                "DEEPSEEK_API_KEY не найден в переменных окружения"
            )
        
        # Убираем None значения, чтобы Pydantic использовал значения по умолчанию
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        
        super().__init__(**kwargs)
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Выполнить запрос к DeepSeek API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": kwargs.get("max_tokens", 1000)
        }
        
        if stop:
            data["stop"] = stop
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка запроса к DeepSeek API: {e}")
        except KeyError as e:
            raise Exception(f"Неожиданный формат ответа от DeepSeek API: {e}")
    
    def _llm_type(self) -> str:
        """Тип LLM"""
        return "deepseek"
    
    def invoke(
        self, 
        input: str, 
        config: Optional[Any] = None, 
        **kwargs: Any
    ) -> str:
        """Синхронный вызов LLM"""
        return self._call(input, **kwargs)
    
    def predict(self, text: str, **kwargs: Any) -> str:
        """Предсказание для текста"""
        return self._call(text, **kwargs)
    
    def predict_messages(self, messages: List[Any], **kwargs: Any) -> str:
        """Предсказание для сообщений"""
        if messages and hasattr(messages[0], 'content'):
            text = messages[0].content
        else:
            text = str(messages)
        return self._call(text, **kwargs)
    
    def generate_prompt(
        self, 
        prompt: BasePromptTemplate, 
        **kwargs: Any
    ) -> str:
        """Генерация из промпта"""
        return self._call(str(prompt), **kwargs)
    
    async def ainvoke(
        self, 
        input: str, 
        config: Optional[Any] = None, 
        **kwargs: Any
    ) -> str:
        """Асинхронный вызов LLM"""
        return self.invoke(input, config, **kwargs)
    
    async def apredict(self, text: str, **kwargs: Any) -> str:
        """Асинхронное предсказание для текста"""
        return self.predict(text, **kwargs)
    
    async def apredict_messages(
        self, 
        messages: List[Any], 
        **kwargs: Any
    ) -> str:
        """Асинхронное предсказание для сообщений"""
        return self.predict_messages(messages, **kwargs)
    
    async def agenerate_prompt(
        self, 
        prompt: BasePromptTemplate, 
        **kwargs: Any
    ) -> str:
        """Асинхронная генерация из промпта"""
        return self.generate_prompt(prompt, **kwargs)


class LLMConfig:
    """Конфигурация для DeepSeek LLM провайдера"""
    
    @staticmethod
    def get_deepseek_llm(
        model: str = "deepseek-reasoner",
        temperature: float = 1.0,
        api_key: Optional[str] = None
    ) -> BaseLanguageModel:
        """Получить DeepSeek LLM"""
        return DeepSeekLLM(
            model=model,
            temperature=temperature,
            api_key=api_key
        )
    
    @staticmethod
    def get_default_llm(
        provider: str = "deepseek", 
        **kwargs
    ) -> BaseLanguageModel:
        """Получить LLM по умолчанию (только DeepSeek)"""
        if provider.lower() == "deepseek":
            return LLMConfig.get_deepseek_llm(**kwargs)
        else:
            raise ValueError(
                f"Неподдерживаемый провайдер: {provider}. "
                "Поддерживается только DeepSeek."
            )


# Доступные модели (только DeepSeek)
AVAILABLE_MODELS = {
    "deepseek": {
        "deepseek-chat": "DeepSeek Chat (DeepSeek)",
        "deepseek-reasoner": "DeepSeek Reasoner (DeepSeek)"
    }
} 