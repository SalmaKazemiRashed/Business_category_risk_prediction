# dalle_api.py - Updated with GPT Image models (FIXED)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from openai import OpenAI
import os
import base64
import requests
from datetime import datetime
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI(title="GPT Image Generation API")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Valid config
VALID_SIZES = ["1024x1024", "1024x1536", "1536x1024"]
VALID_MODELS = ["gpt-image-2", "gpt-image-1.5", "gpt-image-1-mini"]


class ImageRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    model: str = Field("gpt-image-2")
    size: str = Field("1024x1024")
    quality: str = Field("medium")
    n: int = Field(1, description="Number of images (keep 1 for stability)")
    save_to_file: bool = Field(True)


@app.post("/generate")
async def generate_image(request: ImageRequest):
    """Generate image using GPT Image models"""

    # Validate model
    if request.model not in VALID_MODELS:
        raise HTTPException(400, f"Invalid model. Use: {VALID_MODELS}")

    # Validate size
    if request.size not in VALID_SIZES:
        raise HTTPException(400, f"Invalid size. Use: {VALID_SIZES}")

    try:
        # IMPORTANT FIX:
        # Do NOT pass response_format for gpt-image models
        response = client.images.generate(
            model=request.model,
            prompt=request.prompt,
            size=request.size,
            n=request.n,
            quality=request.quality
        )

        images = []
        saved_paths = []

        for img in response.data:
            image_bytes = None

            # Handle URL output (preferred)
            if hasattr(img, "url") and img.url:
                image_bytes = requests.get(img.url).content

            # Handle base64 output fallback
            elif hasattr(img, "b64_json") and img.b64_json:
                image_bytes = base64.b64decode(img.b64_json)

            if image_bytes is None:
                raise HTTPException(500, "No image data returned from model")

            filename = f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"

            if request.save_to_file:
                with open(filename, "wb") as f:
                    f.write(image_bytes)
                saved_paths.append(filename)

            images.append({
                "revised_prompt": getattr(img, "revised_prompt", None),
                "url": getattr(img, "url", None)
            })

        return {
            "success": True,
            "model": request.model,
            "images": images,
            "saved_paths": saved_paths,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(500, detail=str(e))


@app.get("/models")
async def list_available():
    """List available models"""
    try:
        models = client.models.list()
        image_models = [
            m.id for m in models.data
            if "image" in m.id or "dall" in m.id
        ]
        return {
            "available": image_models,
            "recommended": VALID_MODELS
        }
    except Exception:
        return {"recommended": VALID_MODELS}


if __name__ == "__main__":
    uvicorn.run("dalle_api:app", host="0.0.0.0", port=8000, reload=True)