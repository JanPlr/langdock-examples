# Langdock Assistant Streaming Example

This folder contains a minimal Python script that connects to the Langdock Assistants API and prints the streamed answer token by token in the terminal.

## Setup

1. (Optional but recommended) Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Export your API key:
   ```bash
   export LANGDOCK_API_KEY=sk-your-key
   ```

## Run the demo

```bash
python streaming_assistant.py
```

You should immediately see the assistant response appear in place as tokens arrive from the API.





