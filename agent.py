import openai
from deep_translator import GoogleTranslator
import os

# Вставь свой API-ключ
openai.api_key = os.getenv("API_KEY")

def LLM(prompt: str) -> str:
    """
    Функция принимает русский текст, переводит на английский,
    отправляет в GPT-5-mini, получает ответ, переводит обратно на русский.
    """
    # Перевод с русского на английский
    prompt_en = GoogleTranslator(source='ru', target='en').translate(prompt)

    # Запрос к GPT-5-mini
    response = openai.ChatCompletion.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": (
                "You are a patient and knowledgeable school teacher. "
                "Answer briefly in one sentence. "
                "Verify factual accuracy. If you don't know the answer, say so honestly."
            )},
            {"role": "user", "content": prompt_en}
        ],
        temperature=0.1,   # меньше креативности, больше точности
        max_tokens=200      # ограничение длины ответа
    )

    # Получаем ответ
    ans_en = response['choices'][0]['message']['content']

    # Перевод обратно на русский
    ans_ru = GoogleTranslator(source='en', target='ru').translate(ans_en)

    return ans_ru

