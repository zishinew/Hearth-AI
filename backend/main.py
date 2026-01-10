from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import base64
import google.generativeai as genai
from services import audit_room, generate_renovation

# Load environment variables from .env file
load_dotenv()

# Verify environment variables are loaded (for later use)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
STABILITY_KEY = os.getenv("STABILITY_KEY")

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request validation
class AnalyzeRequest(BaseModel):
    image_url: str

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "healthy"}

# List available Gemini models
@app.get("/models")
async def list_models():
    """List all available Gemini models for your API key."""
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        models = genai.list_models()
        
        # Filter and format model information
        available_models = []
        for model in models:
            # Only include models that support generateContent
            if 'generateContent' in model.supported_generation_methods:
                available_models.append({
                    "name": model.name,
                    "display_name": model.display_name,
                    "description": model.description,
                    "supported_methods": list(model.supported_generation_methods)
                })
        
        return {
            "available_models": available_models,
            "total_count": len(available_models)
        }
    except Exception as e:
        return {
            "error": f"Failed to list models: {str(e)}",
            "available_models": []
        }

# Analyze endpoint (temporarily returning only audit JSON for testing)
@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    try:
        # Step 1: Perform accessibility audit using Gemini
        audit_data = audit_room(request.image_url)
        
        # Temporarily return only audit JSON for testing
        return {
            "audit": audit_data
        }
        
        # TODO: Re-enable image generation after testing
        # Step 2: Extract prompts from audit
        # image_gen_prompt = audit_data.get("image_gen_prompt")
        # mask_prompt = audit_data.get("mask_prompt")
        #
        # Step 3: Generate renovated image using Stability AI
        # renovated_image_bytes = None
        # renovated_image_base64 = None
        #
        # if image_gen_prompt and mask_prompt:
        #     try:
        #         renovated_image_bytes = generate_renovation(
        #             request.image_url,
        #             image_gen_prompt,
        #             mask_prompt
        #         )
        #
        #         # Step 4: Encode image to base64
        #         if renovated_image_bytes:
        #             base64_encoded = base64.b64encode(renovated_image_bytes).decode('utf-8')
        #             renovated_image_base64 = f"data:image/webp;base64,{base64_encoded}"
        #     except Exception as e:
        #         # If image generation fails, log error but continue with audit data
        #         print(f"Image generation error: {str(e)}")
        #         renovated_image_base64 = None
        #
        # # Return response with audit and image (or null if generation failed)
        # return {
        #     "audit": audit_data,
        #     "renovated_image_base64": renovated_image_base64
        # }
        
    except Exception as e:
        # If audit fails, return error response
        return {
            "error": f"Analysis failed: {str(e)}",
            "audit": None
        }

