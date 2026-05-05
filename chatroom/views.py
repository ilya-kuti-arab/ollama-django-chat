from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from json import dumps
from requests import post
import json

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

def index(request):
    return render(request, "index.html")

@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    # API endpoint for chat requests
    try:
        data = json.loads(request.body)
        model = data.get("qwen2.5-coder:7b", "qwen2.5-coder:7b")
        prompt = data.get("prompt", '')
        
        if not prompt:
            return JsonResponse({"error": "Prompt is required"}, status=400)
        
        # Call Ollama model
        response_text = call_ollama_model(model, prompt)
        
        if response_text == "error":
            return JsonResponse({"error": "Failed to get response from Ollama"}, status=500)
        
        return JsonResponse({
            "response": response_text,
            "model": model,
            "success": True
        })
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def models_api(request):
    # Get list of available models
    try:
        url = "http://localhost:11434/api/tags"
        response = post(url, headers={"content_type": "application/json"})
        
        if response.status_code == 200:
            models_data = response.json()
            models = [model["name"] for model in models_data.get("models", [])]
            return JsonResponse({"models": models, "success": True})
        else:
            return JsonResponse({"error": "Failed to fetch models", "success": False}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e), "success": False}, status=500)