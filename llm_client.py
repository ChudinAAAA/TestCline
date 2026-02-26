#!/usr/bin/env python3
"""
CLI-клиент для отправки запросов в LLM через LiteLLM Proxy.
"""

import os
import sys
from openai import OpenAI


def get_client():
    """Создание клиента OpenAI с настройками из переменных окружения."""
    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get(
        "OPENAI_BASE_URL",
        "https://llmlite.ailab-copilot-prod.corp.tander.ru"
    )
    
    if not api_key:
        print("Ошибка: не найден API-ключ. Установите переменную окружения OPENAI_API_KEY")
        sys.exit(1)
    
    return OpenAI(
        api_key=api_key,
        base_url=base_url
    )


def send_message(client, messages):
    """Отправка запроса в LLM и получение ответа."""
    try:
        response = client.chat.completions.create(
            model="MagnitCopilot",
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка при обращении к API: {str(e)}"


def main():
    """Основная функция CLI-интерфейса."""
    print("=" * 50)
    print("CLI-клиент для LLM")
    print("=" * 50)
    print("Введите ваше сообщение (или 'exit' для выхода)")
    print("-" * 50)
    
    client = get_client()
    messages = []
    
    while True:
        try:
            user_input = input("\nВы: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ("exit", "quit", "выход"):
                print("До свидания!")
                break
            
            # Добавляем сообщение пользователя в историю
            messages.append({"role": "user", "content": user_input})
            
            # Отправляем запрос и получаем ответ
            print("\nLLM: ", end="", flush=True)
            response = send_message(client, messages)
            print(response)
            
            # Добавляем ответ в историю для контекста
            messages.append({"role": "assistant", "content": response})
            
        except KeyboardInterrupt:
            print("\n\nДо свидания!")
            break
        except EOFError:
            break


if __name__ == "__main__":
    main()
