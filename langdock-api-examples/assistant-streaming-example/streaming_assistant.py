import json
import os
import sys

import requests

API_URL = "https://api.langdock.com/openai/eu/v1/chat/completions"

api_key = os.getenv("LANGDOCK_API_KEY")
if not api_key:
    print("Set LANGDOCK_API_KEY before running this script.", file=sys.stderr)
    sys.exit(1)

payload = {
    "model": "gpt-5",
    "stream": True,
    "messages": [
        {"role": "system", "content": "You are concise and friendly."},
        {"role": "user", "content": "Give me three fun facts about octopuses."},
    ],
}

with requests.post(API_URL, headers={
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}, json=payload, stream=True) as response:
    response.raise_for_status()
    print("Assistant:", end=" ", flush=True)
    for line in response.iter_lines(decode_unicode=True):
        if not line or not line.startswith("data: "):
            continue
        data = line.removeprefix("data: ").strip()
        if data == "[DONE]":
            break
        chunk = json.loads(data)
        token = chunk.get("choices", [{}])[0].get("delta", {}).get("content")
        if token:
            print(token, end="", flush=True)
    print()

