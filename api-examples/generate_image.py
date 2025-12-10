"""
Langdock API - Image Generation Example

This script demonstrates how to generate images using the Langdock API.
It uses an existing Assistant that has image generation capability enabled.

Available image models in Langdock:
- DALL-E 3 (OpenAI)
- GPT Image 1 (OpenAI)  
- Flux1.1 Pro Ultra (Black Forest Labs)
- Flux.1 Kontext (Black Forest Labs)
- Imagen 4, Imagen 4 Fast (Google)
"""

import os
import json
import base64
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
# The load_dotenv() function reads the .env file in the current directory
# and makes those variables available via os.getenv()
load_dotenv()

# The Assistant ID for the image generation assistant
# This assistant is pre-configured in the Langdock platform with image generation enabled
# You can find this ID in the URL when editing your assistant:
# https://app.langdock.com/assistants/ASSISTANT_ID/edit
ASSISTANT_ID = "d83d3338-a103-4619-9e3d-2eff0a0238e9"


def generate_image(prompt: str) -> dict:
    """
    Generate an image using the Langdock Assistant API.
    
    This function sends a request to an existing Assistant that has
    image generation capability enabled. The assistant will process
    the prompt and generate an image using the configured image model.
    
    Parameters:
    -----------
    prompt : str
        The text description of the image you want to generate.
        Be descriptive - the more details you provide, the better the result.
    
    Returns:
    --------
    dict: Contains the response from the API including the generated image data
    """
    
    # Get the API key from environment variables
    api_key = os.getenv("LANGDOCK_API_KEY")
    
    if not api_key:
        raise ValueError(
            "LANGDOCK_API_KEY environment variable is not set. "
            "Please create a .env file with your API key or set it in your environment."
        )
    
    # The Langdock Assistant API endpoint
    url = "https://api.langdock.com/assistant/v1/chat/completions"
    
    # Request headers with Bearer token authorization
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Request body using an existing assistant
    # assistantId: The unique identifier of your pre-configured assistant
    # messages: The conversation - a single user message asking for an image
    # stream: Set to False to get a complete response
    payload = {
        "assistantId": ASSISTANT_ID,
        "messages": [
            {
                "role": "user",
                "content": f"Generate an image of: {prompt}"
            }
        ],
        "stream": False
    }
    
    print(f"Using Assistant ID: {ASSISTANT_ID}")
    print(f"Prompt: {prompt}")
    print("-" * 50)
    print("Generating image (this may take a few seconds)...")
    
    # Send the POST request to the API
    response = requests.post(url, headers=headers, json=payload, timeout=120)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error: HTTP {response.status_code}")
        print(f"Response: {response.text[:500]}")
        raise Exception(f"API request failed with status {response.status_code}")
    
    # Parse the JSON response
    result = response.json()
    
    return result


def extract_base64_images(response: dict) -> list:
    """
    Extract base64-encoded images from the Langdock API response.
    
    The API response structure is:
    - result[0]: The assistant's tool-call (requesting image generation)
    - result[1]: The tool-result containing the generated image(s)
    
    The image data is in: result[1].content[0].output.value.images[0].base64
    
    Parameters:
    -----------
    response : dict
        The full response from the Langdock API
    
    Returns:
    --------
    list: List of base64 image strings found in the response
    """
    images = []
    
    # Navigate through the response structure
    if "result" in response:
        for message in response["result"]:
            # Look for tool-result messages
            if message.get("role") == "tool":
                for content_part in message.get("content", []):
                    if content_part.get("type") == "tool-result":
                        # Get the output value which contains the images
                        output = content_part.get("output", {})
                        value = output.get("value", {})
                        
                        # Extract images from the value
                        image_list = value.get("images", [])
                        for img in image_list:
                            if "base64" in img:
                                images.append(img["base64"])
                            elif "url" in img and img["url"] != "N/A":
                                # Some responses might include URLs
                                images.append({"type": "url", "value": img["url"]})
    
    return images


def save_base64_image(base64_data: str, filename: str = None) -> str:
    """
    Save a base64-encoded image to a file in the generated_images folder.
    
    Base64 is a way to encode binary data (like images) as text.
    This function decodes that text back into binary and saves it.
    
    Parameters:
    -----------
    base64_data : str
        The base64-encoded image data
    
    filename : str, optional
        The filename to save as. If not provided, generates one based on timestamp.
    
    Returns:
    --------
    str: The path to the saved image file
    """
    # Create the output directory if it doesn't exist
    # os.path.dirname(__file__) gets the directory where this script is located
    # This ensures the folder is created relative to the script, not the working directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "generated_images")
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_image_{timestamp}.jpg"
    
    # Create full path in the output directory
    filepath = os.path.join(output_dir, filename)
    
    # Decode the base64 string to binary data
    # base64.b64decode() converts the text representation back to raw bytes
    image_data = base64.b64decode(base64_data)
    
    # Write the binary image data to a file
    # 'wb' mode means "write binary" - images are binary data, not text
    with open(filepath, 'wb') as f:
        f.write(image_data)
    
    print(f"Image saved to: {filepath}")
    return filepath


# Main execution block
# This code only runs when you execute this file directly (not when importing it)
if __name__ == "__main__":
    print("=" * 60)
    print("LANGDOCK IMAGE GENERATION EXAMPLE")
    print("=" * 60)
    print()
    
    # Generate an image with a detailed prompt
    result = generate_image(
        prompt="A serene Japanese garden with cherry blossoms, a small wooden bridge over a koi pond, and Mount Fuji visible in the background at sunset"
    )
    
    print("\nImage generation complete!")
    print("-" * 50)
    
    # Extract the base64 images from the response
    images = extract_base64_images(result)
    
    if images:
        print(f"\nFound {len(images)} image(s) in the response!")
        
        for i, img_data in enumerate(images):
            if isinstance(img_data, dict) and img_data.get("type") == "url":
                # Handle URL-based images
                print(f"  Image {i+1}: URL - {img_data['value'][:80]}...")
            else:
                # Handle base64 images
                print(f"  Image {i+1}: Base64 data ({len(img_data)} characters)")
                
                # Save the first image
                if i == 0:
                    saved_file = save_base64_image(img_data)
                    print(f"\n✓ Image saved successfully!")
                    print(f"  File: {saved_file}")
                    print(f"  You can open this file to view the generated image.")
    else:
        print("\nNo images found in the response.")
        print("This might happen if image generation failed or the assistant")
        print("is not configured for image generation.")
        
        # Show some debug info
        print("\nResponse structure:")
        if "result" in result:
            for i, msg in enumerate(result["result"]):
                print(f"  Message {i}: role={msg.get('role')}")
