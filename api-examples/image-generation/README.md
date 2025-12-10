# Image Generation Example

Generate images using the Langdock Assistant API. This example uses an Assistant with image generation capability enabled.

## Setup

### 1. Install dependencies

```bash
cd api-examples/image-generation
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set up your API key

Create a `.env` file in this directory:

```bash
LANGDOCK_API_KEY=your-api-key-here
```

### 3. Configure your Assistant

The script uses an Assistant ID that's pre-configured in the Langdock platform.

To use your own assistant:
1. Create an assistant in [Langdock](https://app.langdock.com)
2. Enable image generation in the assistant settings
3. Share the assistant with your API key
4. Copy the assistant ID from the URL: `https://app.langdock.com/assistants/ASSISTANT_ID/edit`
5. Update the `ASSISTANT_ID` variable in `generate_image.py`

## Usage

Run the script:

```bash
python generate_image.py
```

Generated images are saved to the `generated_images/` folder.

## How It Works

1. The script sends a POST request to `https://api.langdock.com/assistant/v1/chat/completions`
2. The request includes the Assistant ID and your image prompt
3. The Assistant processes the request and uses an image model (like DALL-E 3) in the background
4. The response contains a base64-encoded image
5. The script decodes and saves the image to a file

## Available Image Models

Langdock supports these image generation models:
- **DALL-E 3** (OpenAI)
- **GPT Image 1** (OpenAI)
- **Flux1.1 Pro Ultra** (Black Forest Labs)
- **Flux.1 Kontext** (Black Forest Labs)
- **Imagen 4, Imagen 4 Fast** (Google)

## Customization

Edit the `prompt` in the main block of `generate_image.py` to generate different images:

```python
result = generate_image(
    prompt="Your custom image description here"
)
```

## Output

Generated images are saved to `generated_images/` with timestamps:
```
generated_images/
├── generated_image_20251210_103835.jpg
├── generated_image_20251210_104522.jpg
└── ...
```

