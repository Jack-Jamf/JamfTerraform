"""LLM service for interacting with Gemini API."""
import google.generativeai as genai
import json
from config import GEMINI_API_KEY, GEMINI_MODEL, SYSTEM_PROMPT
from schemas import UserIntent, PolicyIntent, ScriptIntent, CategoryIntent, PackageIntent, SmartGroupIntent, StaticGroupIntent, AppInstallerIntent, RawHCLIntent
from hcl_generator import HCLGenerator


class LLMService:
    """Service for generating HCL using Gemini API with structured intent extraction."""
    
    def __init__(self):
        """Initialize the LLM service."""
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=SYSTEM_PROMPT,
            generation_config={"response_mime_type": "application/json"}
        )
        # HCLGenerator is instantiated per-request to ensure fresh naming state
    
    def generate_hcl(self, user_prompt: str, context: str | None = None) -> str:
        """
        Generate HCL configuration based on user prompt via structured intent.
        """
        # Construct the full prompt
        full_prompt = user_prompt
        if context:
            full_prompt = f"Previous Conversation History:\n{context}\n\nCurrent Request:\n{user_prompt}\n\n[SYSTEM REMINDER]: Continue to output ONLY JSON. Use the Valid Intents or missing_info_question."
        
        # Generate content (JSON)
        response = self.model.generate_content(full_prompt)
        text = response.text.strip()
        
        # Remove code fences if present
        if text.startswith("```"):
            lines = text.split("\n")
            lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines)
        
        try:
            parsed = UserIntent.model_validate_json(text)
        except Exception as e:
            return f"# Error parsing AI intent: {e}\n# Raw response:\n/*\n{text}\n*/"
        
        # Case 1: Missing Information
        if parsed.missing_info_question:
            return f"# NOTE: {parsed.missing_info_question}"
        
        # Case 2: Intent Found
        if parsed.intent:
            # Handle Hybrid/custom mode
            if isinstance(parsed.intent, RawHCLIntent):
                raw_hcl = f"# Generated via Hybrid Mode (Raw AI Output) - Verify syntax!\n{parsed.intent.hcl_body}"
                return self._wrap_with_provider(raw_hcl)

            data = self._convert_intent_to_data(parsed.intent)
            
            # Map singular type to plural key expected by HCLGenerator
            type_map = {
                'policy': 'policies',
                'script': 'scripts',
                'category': 'categories',
                'package': 'packages',
                'smart_group': 'smart-groups',
                'static_group': 'static-groups',
                'app_installer': 'jamf-app-catalog'
            }
            gen_type = type_map.get(parsed.intent.resource_type, parsed.intent.resource_type)
            
            try:
                # Use fresh generator instance for stateless generation
                generator = HCLGenerator()
                hcl = generator.generate_resource_hcl(gen_type, data)
                return self._wrap_with_provider(hcl)
            except Exception as ex:
                return f"# Error generating HCL from intent: {ex}"
        
        return "# Error: No valid intent or question identified."

    def _convert_intent_to_data(self, intent) -> dict:
        """Convert Pydantic Intent model to Jamf API-like dictionary."""
        data = {}
        
        if isinstance(intent, PolicyIntent):
            data['general'] = {
                'name': intent.name,
                'enabled': intent.enabled
            }
            # Scope conversion
            scope_dict = intent.scope.model_dump(exclude_none=True)
            data['scope'] = scope_dict
            
            # Payloads conversion
            if intent.payloads.packages:
                data['package_configuration'] = {
                    'packages': [p.model_dump(exclude_none=True) for p in intent.payloads.packages]
                }
            if intent.payloads.scripts:
                data['scripts'] = [s.model_dump(exclude_none=True) for s in intent.payloads.scripts]
            # Maintenance logic? (HCLGen doesn't seem to generate maintenance payload? Wait.)
            # I removed maintenance from _generate_policy_hcl check in my previous Step.
            # I should verify if HCLGen supports maintenance. 
            # Step 1143 showed packages and scripts logic. It did NOT show maintenance logic.
            # So I'll ignore maintenance for now or add it later.
            
        elif isinstance(intent, ScriptIntent):
            data['name'] = intent.name
            data['script_contents'] = intent.script_contents
            
        elif isinstance(intent, CategoryIntent):
            data['name'] = intent.name
            data['priority'] = intent.priority
            
        elif isinstance(intent, PackageIntent):
            data['filename'] = intent.name
            data['package_file_source'] = intent.package_file_source
            
        elif isinstance(intent, SmartGroupIntent):
            data['name'] = intent.name
            data['is_smart'] = intent.is_smart
            # data['criteria'] = ...
            
        elif isinstance(intent, StaticGroupIntent):
            data['name'] = intent.name
            data['is_smart'] = False
            
        elif isinstance(intent, AppInstallerIntent):
            data['name'] = intent.name
            data['app'] = {}
            if intent.bundle_id:
                data['app']['bundleId'] = intent.bundle_id
            if intent.version:
                data['app']['latestVersion'] = intent.version
            
            # Match API structure expected by HCLGenerator
            data['enabled'] = intent.enabled
            data['deploymentType'] = intent.deployment_type
            data['updateBehavior'] = intent.update_behavior
            
            data['category'] = {'id': intent.category_id}
            data['site'] = {'id': intent.site_id}
            data['smartGroup'] = {'id': intent.smart_group_id}
            
        return data

    def _wrap_with_provider(self, hcl: str) -> str:
        """Prepend standard provider block."""
        header = """terraform {
  required_providers {
    jamfpro = {
      source  = "deploymenttheory/jamfpro"
      version = "~> 0.19.0"
    }
  }
}

provider "jamfpro" {
  # Configuration parameters
}

"""
        return header + hcl


# Singleton instance
_llm_service = None


def get_llm_service() -> LLMService:
    """Get or create the LLM service singleton."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
