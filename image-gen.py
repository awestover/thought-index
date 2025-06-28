"""
Wilson says that I should ask an AI to generate a prompt from the blog instead
of feeding the whole dang content in. This makes sense.

blog plan:
- a pretty clean site

It has curated posts, I generate an image for each of the posts. 
I write a 1 line description of each post. 
Approximately weekly releases.

I write these in obsidian but they are compiled with a new compiler thing. 

Not totally sure that this is the way to do it. But this is what I'm thinking about trying for now. 
"""

import requests
import os

api_key = os.environ["TOGETHER_API_KEY"]

prompt = """

Make a studio Ghibli themed blog post thumbnail from the blog post content below:

---

life
What determines the goodness of the universe?
The goodness of the universe is determined by the quantity times quality of conscious experience.
People with hopes and dreams.
People who create art, connect with other humans and care about other humans and various projects.
People who experience and share joy and excitement.
People who rise to challenges, and become better people.
This is what makes the universe good.

And I desire to make the universe more good
"""

url = "https://api.together.xyz/v1/images/generations"

payload = {
    "model": "black-forest-labs/FLUX.1-schnell",
    "prompt": prompt,
    "steps": 4,
    "samples": 1,
    "height": 512,
    "width": 512,
    "guidance_scale": 3.5,
    "output_format": "jpeg"
}

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {api_key}"
}

response = requests.post(url, json=payload, headers=headers)

# Print full response or only image URLs
data = response.json()
print("Image URLs:")
for i, img in enumerate(data.get("data", [])):
    print(f"{i+1}: {img['url']}")

