import os
import requests
import urllib.parse
from pathlib import Path

def format_filename_for_url(filename):
    name = Path(filename).stem
    name = name.replace('!', '').replace('?', '').replace('%', '')
    name = name.replace(' ', '-')
    return urllib.parse.quote(name)

def generate_image_prompt(blog_content):
    prompt = f"""You are an expert in crafting effective image generation prompts.
Your task is to read the blog post below and write a concise, vivid prompt suitable for an image generation model.

Requirements:

Focus on the main themes, visuals, or metaphors from the blog post

Use clear, concrete language (e.g., "a winding mountain path at dawn" or "a stylized figure reaching toward stars")

Include relevant objects, scenes, or abstract representations

If humans are included, describe them as stylized, cartoon-like, or abstract, not realistic

Limit the prompt to under 150 words

DO NOT instruct the model to generate ANY text in the image.
No words, no letters, nothing of the sort!

Output only the image generation prompt — no extra text or explanation

Blog post:
{blog_content}
"""
    api_key = os.environ.get("OTHER_OPENAI_API_KEY")
    # Call the OpenAI API to generate the prompt
    url = "https://api.openai.com/v1/chat/completions"
    
    payload = {
        "model": "gpt-4.1-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    generated_prompt = data["choices"][0]["message"]["content"].strip()
    
    # Add instruction to avoid letters
    generated_prompt += " No text or letters in the image."
    
    return generated_prompt
        

def generate_image(prompt, output_path="generated_image.jpg"):
    api_key = os.environ.get("OTHER_OPENAI_API_KEY")
    url = "https://api.openai.com/v1/images/generations"

    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024",
        "quality": "standard",
        "response_format": "url"
    }

    # Old Together AI code (commented out):
    # url = "https://api.together.xyz/v1/images/generations"
    # payload = {
    #     "model": "black-forest-labs/FLUX.1-schnell",
    #     "prompt": prompt,
    #     "steps": 4,
    #     "samples": 1,
    #     "height": 512,
    #     "width": 512,
    #     "guidance_scale": 3.5,
    #     "output_format": "jpeg"
    # }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}"
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    image_url = data["data"][0]["url"]
    
    # Download the image
    img_response = requests.get(image_url)
    img_response.raise_for_status()
    
    with open(output_path, "wb") as f:
        f.write(img_response.content)
    
    print(f"✅ Image saved to {output_path}")
    return output_path

def generate_new_images():
    content_dir = os.path.expanduser("~/dropbox/2blog/content/0stack")
    thumbnails_dir = "thumbnails"
    
    content_files = []
    for file_path in Path(content_dir).iterdir():
        if file_path.is_file() and file_path.suffix.lower() == '.md':
            content_files.append(file_path)

    for file_path in content_files:
        print(f"\n{'='*60}")
        print(f"📄 Processing: {file_path.name}")
        print(f"{'='*60}")
        
        # Read the blog content
        with open(file_path, 'r', encoding='utf-8') as f:
            blog_content = f.read().strip()
        
        base_name = format_filename_for_url(file_path.name)
        
        # Get output image name (without _thumbnail)
        output_image = os.path.join(thumbnails_dir, f"{base_name}.jpg")
        prompt_file = os.path.join(thumbnails_dir, f"{base_name}_prompt.txt")
        
        # Check if both image and prompt already exist
        if os.path.exists(output_image) and os.path.exists(prompt_file):
            print(f"⏭️  Skipping {base_name} - image and prompt already exist")
            continue
        
        print("📝 Blog content:")
        print("-" * 50)
        print(blog_content[:200] + "..." if len(blog_content) > 200 else blog_content)
        print("-" * 50)
        
        # Step 1: Generate the image prompt
        print("\n🎨 Generating image prompt...")
        image_prompt = generate_image_prompt(blog_content)
        
        print("Generated prompt:")
        print("-" * 50)
        print(image_prompt)
        print("-" * 50)
        
        # Save the prompt to thumbnails directory
        with open(prompt_file, "w") as f:
            f.write(image_prompt)
        print(f"💾 Prompt saved to {prompt_file}")
        
        # Step 2: Generate the image
        print("\n🖼️  Generating image...")
        result = generate_image(image_prompt, output_image)
        
        print(f"🎉 Success! Image generated: {result}")
        print(f"📁 Files created:")
        print(f"   - {prompt_file} (generated prompt)")
        print(f"   - {output_image} (generated image)")
    
    print(f"\n{'='*60}")
    print("🏁 Processing complete!")
    print(f"{'='*60}")

