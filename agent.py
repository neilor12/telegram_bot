import ollama
from deep_translator import GoogleTranslator

def LLM(prompt):
    #Перевод с русского на английский
    result =  GoogleTranslator(source='ru', target='en').translate(prompt)
    #нейросеть
    stream = ollama.generate(
        model="llama3.2",
        prompt= result,
        system = """"You are a patient and knowledgeable school teacher. 
                Answer briefly in one sentence.
                Verify factual accuracy. If you don't know the answer, say so honestly.""",
        options={
            'temperature': 0.1,
            'num_predict': 500,
            'top_p': 0.9
      },
    )
    ans = stream["response"]
    result = GoogleTranslator(source='en', target='ru').translate(ans)
    return result
