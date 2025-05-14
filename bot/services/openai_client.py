import aiohttp
import os
from typing import Dict, List, Optional


class OpenAIClient:
    def __init__(self):
        self.api_key = ""
        self.base_url = "https://api.openai.com/v1"
        self.session = None
        self.model = "gpt-3.5-turbo"
        
    async def _create_session(self):
        """Создает aiohttp сессию для запросов к API"""
        self.session = aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
    
    async def close_session(self):
        """Закрывает aiohttp сессию"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def generate_response(self, user_message: str, history: List[Dict[str, str]]) -> str:
        """
        Генерирует ответ на сообщение пользователя с учетом истории
        
        Args:
            user_message: Сообщение от пользователя
            history: История диалога, список словарей {"role": "user/assistant", "content": "текст"}
        
        Returns:
            str: Ответ от ассистента
        """
        if not self.session:
            await self._create_session()
        
        # Добавляем новое сообщение пользователя в историю
        history.append({"role": "user", "content": user_message})
        
        # Сохраняем только последние 10 сообщений для экономии токенов
        if len(history) > 20:  # 10 пар сообщений (вопрос-ответ)
            history = history[-20:]
        
        # Создаем контекст с системным промптом и историей
        messages = [
            {
                "role": "system", 
                "content": "Ты консультант в маркетплейсе. Твоя задача - помогать покупателям находить товары, отвечать на вопросы о доставке и оплате. Будь вежливым, лаконичным и полезным."
            },
            *history
        ]
        
        url = f"{self.base_url}/chat/completions"
        
        try:
            async with self.session.post(
                url,
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 500,
                }
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    return f"Ошибка API: {error_text}"
                
                response_data = await response.json()
                assistant_message = response_data["choices"][0]["message"]["content"]
                
                # Добавляем ответ ассистента в историю
                history.append({"role": "assistant", "content": assistant_message})
                
                return assistant_message
                
        except Exception as e:
            return f"Произошла ошибка: {str(e)}"

# Создаем глобальный экземпляр клиента
openai_client = OpenAIClient()