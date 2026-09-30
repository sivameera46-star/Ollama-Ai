import requests

url = "http://localhost:11434/api/generate"

data = {
    "model": "llama3.2:1b",
    "prompt": "Explain Python in simple terms",
    "stream": False
}

response = requests.post(url, json=data)

result = response.json()

print(result["response"])