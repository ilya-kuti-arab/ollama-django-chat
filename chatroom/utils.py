from json import dumps
from requests import post


def call_ollama_model(model, prompt, stream=False):
    url = "http://localhost:11434/api/generate"
    params = {
        "model": model,
        "prompt": prompt,
        "stream": stream,
    }
    
    data = dumps(params)
    response = post(url, data=data, headers={"content_type": "application/json"})
    
    if response.status_code != 200:
        return "error"
    else:
        return response.json()["response"]
