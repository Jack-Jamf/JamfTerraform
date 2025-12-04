"""LLM service for interacting with Gemini API."""
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL, SYSTEM_PROMPT


class LLMService:
    """Service for generating HCL using Gemini API."""
    
    def __init__(self):
        """Initialize the LLM service."""
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=SYSTEM_PROMPT
        )
    
    def generate_hcl(self, user_prompt: str, context: str | None = None) -> str:
        """
        Generate HCL configuration based on user prompt.
        
        Args:
            user_prompt: User's description of desired configuration
            context: Optional context or existing configuration
            
        Returns:
            Generated HCL configuration as a string
            
        Raises:
            Exception: If API call fails
        """
        # Construct the full prompt
        full_prompt = user_prompt
        if context:
            full_prompt = f"Context:\n{context}\n\nRequest:\n{user_prompt}"
        
        # Generate content
        response = self.model.generate_content(full_prompt)
        
        # Extract and return the HCL
        hcl_output = response.text.strip()
        
        # Remove code fences if the model added them despite instructions
        if hcl_output.startswith("```"):
            lines = hcl_output.split("\n")
            # Remove first line (```hcl or ```)
            lines = lines[1:]
            # Remove last line if it's ```
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            hcl_output = "\n".join(lines)
        
        return hcl_output


# Singleton instance
_llm_service = None


def get_llm_service() -> LLMService:
    """Get or create the LLM service singleton."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
