#!/usr/bin/env python3
"""
CLI-клиент для отправки запросов в LLM через LiteLLM Proxy.
"""

import os
import sys
from openai import OpenAI


def get_client():
    """Создание клиента OpenAI с настройками из переменных окружения или через ввод."""
    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = os.environ.get("OPENAI_BASE_URL")
    model = os.environ.get("OPENAI_MODEL")
    
    # Если переменные не установлены, запрашиваем через input в нужном порядке
    if not base_url:
        base_url = input("Введите OPENAI_BASE_URL: ").strip()
    
    if not model:
        model = input("Введите OPENAI_MODEL: ").strip()
    
    if not api_key:
        api_key = input("Введите OPENAI_API_KEY: ").strip()
    
    if not api_key or not base_url or not model:
        print("Ошибка: все три переменные обязательны")
        sys.exit(1)
    
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    
    # Сохраняем модель в объекте клиента
    client.model = model
    return client


def send_message(client, messages):
    """Отправка запроса в LLM и получение ответа."""
    try:
        response = client.chat.completions.create(
            model=client.model,
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
