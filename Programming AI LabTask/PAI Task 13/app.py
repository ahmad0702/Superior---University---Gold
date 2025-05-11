from flask import Flask, render_template, request
import requests
import base64
import math

app = Flask(__name__)
API_KEY = "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"

example_prompts = [
    "A magic forest with glowing plants and fairy homes among giant mushrooms",
    "An old steampunk airship floating through golden clouds at sunset",
    "A future Mars colony with glass domes and gardens against red mountains",
    "A dragon sleeping on gold coins in a crystal cave",
    "An underwater kingdom with merpeople and glowing coral buildings",
    "A floating island with waterfalls pouring into clouds below",
    "A witch's cottage in fall with magic herbs in the garden",
    "A robot painting in a sunny studio with art supplies around it",
    "A magical library with floating glowing books and spiral staircases",
    "A Japanese shrine during cherry blossom season with lanterns and misty mountains",
    "A cosmic beach with glowing sand and an aurora in the night sky",
    "A medieval marketplace with colorful tents and street performers",
    "A cyberpunk city with neon signs and flying cars at night",
    "A peaceful bamboo forest with a hidden ancient temple",
    "A giant turtle carrying a village on its back in the ocean",
]

available_models = [
    "black-forest-labs/FLUX.1-dev",
    "black-forest-labs/FLUX.1-schnell",
    "stabilityai/stable-diffusion-xl-base-1.0",
    "runwayml/stable-diffusion-v1-5",
    "stabilityai/stable-diffusion-3-medium-diffusers"
]

def get_image_dimensions(aspect_ratio, base_size=512):
    width, height = map(int, aspect_ratio.split("/"))
    scale = base_size / math.sqrt(width * height)
    width = int((width * scale) // 16 * 16)
    height = int((height * scale) // 16 * 16)
    return width, height

@app.route("/", methods=["GET", "POST"])
def index():
    images = []
    prompt = ""
    model = ""
    count = 1
    ratio = "1/1"
    if request.method == "POST":
        prompt = request.form.get("prompt")
        model = request.form.get("model")
        count = int(request.form.get("count", 1))
        ratio = request.form.get("ratio", "1/1")

        width, height = get_image_dimensions(ratio)

        for _ in range(count):
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{model}",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json",
                    "x-use-cache": "false"
                },
                json={
                    "inputs": prompt,
                    "parameters": {"width": width, "height": height}
                }
            )
            if response.ok:
                img_data = base64.b64encode(response.content).decode("utf-8")
                images.append(f"data:image/png;base64,{img_data}")
            else:
                images.append(None)

    return render_template(
        "index.html",
        example_prompts=example_prompts,
        available_models=available_models,
        prompt=prompt,
        model=model,
        count=count,
        ratio=ratio,
        images=images
    )

if __name__ == "__main__":
    app.run(debug=True)
