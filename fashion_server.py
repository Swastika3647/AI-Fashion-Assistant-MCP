import os
import google.generativeai as genai
from mcp.server.fastmcp import FastMCP
from typing import Optional

# 1. Initialize the MCP Server
mcp = FastMCP("Fashion Assistant MCP")

# 2. Configure Google Gemini (The logic engine)
# Make sure to set GOOGLE_API_KEY in your environment variables
# Create this variable directly
GOOGLE_API_KEY = "AIzaSyDoXBDF_G7836osOper4cKHsyHlClQ_U4E"

# Then update the next line to use it directly (remove the 'if' check if you want)
genai.configure(api_key=GOOGLE_API_KEY)

# Define the "VogueGPT" persona from your repo
STYLIST_INSTRUCTION = """
You are a high-end digital stylist. 
Analyze the user's request (and image if provided) to extract:
- Body shape, Face shape, Undertone, Hair texture.
Your tone is confident, chic, and helpful (like a Vogue editor).
Avoid harsh neons for warm undertones. Suggest earthy palettes or structured fits where appropriate.
"""

@mcp.tool()
async def get_fashion_advice(query: str, image_path: Optional[str] = None) -> str:
    """
    Get personalized fashion advice based on a query and an optional image.
    Args:
        query: The user's fashion question (e.g., "What should I wear to a wedding?").
        image_path: (Optional) Absolute path to a local image file of the user or outfit.
    """
    if not GOOGLE_API_KEY:
        return "Error: GOOGLE_API_KEY environment variable not set."

    try:
        model = genai.GenerativeModel('models/gemini-3-flash-preview')
        
        # Prepare content for the model
        content = [STYLIST_INSTRUCTION, f"User Query: {query}"]
        
        # If an image is provided, load it
        if image_path:
            if not os.path.exists(image_path):
                return f"Error: Image not found at {image_path}"
                
            # Load image data for Gemini
            import PIL.Image
            img = PIL.Image.open(image_path)
            content.append(img)
            content.append("Analyze the physical features in this image to inform your advice.")

        # Generate response
        response = model.generate_content(content)
        return response.text

    except Exception as e:
        return f"Error processing fashion request: {str(e)}"

if __name__ == "__main__":
    mcp.run()