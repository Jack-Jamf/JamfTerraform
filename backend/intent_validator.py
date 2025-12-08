"""
Validator for UserIntents to enforce strict Proporter business logic and safety checks.
"""
from typing import Optional, List
import difflib
from schemas import (
    UserIntent, PolicyIntent, ScriptIntent, CategoryIntent, 
    PackageIntent, SmartGroupIntent, StaticGroupIntent, 
    AppInstallerIntent, RawHCLIntent
)

class IntentValidator:
    """Validates structured UserIntents before HCL generation."""

    def __init__(self, app_catalog: Optional[List[str]] = None):
        """
        Initialize the validator.
        
        Args:
            app_catalog: List of valid app names from the Jamf App Catalog.
        """
        self.app_catalog = app_catalog or []

    def validate(self, intent_wrapper: UserIntent) -> Optional[str]:
        """
        Validate the user intent.
        
        Returns:
            None if valid, or an error message string if invalid.
        """
        # If the LLM already identified missing info, pass that through (or let caller handle it)
        if intent_wrapper.missing_info_question:
            # We don't validate if there's already a question, 
            # but usually the caller checks this first. 
            # If we return None, the caller proceeds. 
            # If we return a string, the caller stops.
            # In this case, if there is a question, it's "valid" in the sense that we don't block it,
            # but the caller should use the question.
            return None

        intent = intent_wrapper.intent
        if not intent:
            return "No intent identified."

        if isinstance(intent, PolicyIntent):
            return self._validate_policy(intent)
        elif isinstance(intent, ScriptIntent):
            return self._validate_script(intent)
        elif isinstance(intent, AppInstallerIntent):
            return self._validate_app_installer(intent)
        elif isinstance(intent, SmartGroupIntent):
            return self._validate_smart_group(intent)
        elif isinstance(intent, PackageIntent):
            return self._validate_package(intent)
        
        # RawHCLIntent is "use at your own risk", but we could add syntax checks later.
        
        return None

    def _validate_policy(self, intent: PolicyIntent) -> Optional[str]:
        """Validate Policy constraints."""
        # Scope Safety check
        if intent.scope.all_computers:
            return "Safety Violation: Targeting 'All Computers' in a policy is restricted. Please target a specific group or use a Smart Group ID."
        
        if not any([
            intent.scope.computer_group_ids,
            intent.scope.computer_ids,
            intent.scope.building_ids,
            intent.scope.department_ids
        ]):
            # If explicit "empty scope" is allowed by schema but practically useless without a note:
            # We might allow it if it's a "draft" policy, but usually users want it deployed.
            # Let's verify if the user explicitly meant "create with no scope". 
            # For now, strict validation:
            return "Policy must have a defined scope (Smart Group, Static Group, or Computer IDs)."
            
        return None

    def _validate_script(self, intent: ScriptIntent) -> Optional[str]:
        """Validate Script content."""
        if not intent.script_contents or len(intent.script_contents.strip()) < 5:
            return "Script content is empty or too short. Please provide the actual shell script."
            
        forbidden = ["rm -rf /", "mkfs", ":(){ :|:& };:"] # Simple safety set
        for term in forbidden:
            if term in intent.script_contents:
                return f"Safety Violation: Script contains potentially dangerous command: '{term}'"
                
        return None

    def _validate_app_installer(self, intent: AppInstallerIntent) -> Optional[str]:
        """Validate App Installer against Catalog."""
        if not self.app_catalog:
            return None # Cannot validate without catalog
            
        if intent.name not in self.app_catalog:
            # Fuzzy match suggestion
            suggestions = difflib.get_close_matches(intent.name, self.app_catalog, n=3, cutoff=0.4)
            if suggestions:
                return f"I cannot verify '{intent.name}' in the Jamf App Catalog. Did you mean: {', '.join(suggestions)}? Please use an exact title from the official list."
            else:
                return f"I cannot verify '{intent.name}' in the Jamf App Catalog. It does not appear to be a supported App Installer title."
        
        return None

    def _validate_smart_group(self, intent: SmartGroupIntent) -> Optional[str]:
        """Validate Smart Group criteria."""
        # Currently criteria is a raw list, so we can't strict validate deeply yet.
        # But we can check basic sanity.
        if intent.is_smart and not intent.criteria:
            # A smart group with no criteria is effectively "All Computers" or "None" depending on logic.
            # Jamf usually requires at least one criterion for a Useful smart group.
            return "Smart Group must have at least one criterion defined."
            
        return None

    def _validate_package(self, intent: PackageIntent) -> Optional[str]:
        """Validate Package."""
        if not intent.package_file_source or intent.package_file_source.strip() == "":
             # Although 'package_file_source' is a string, we might want to ensure it looks like a path?
             # But the schema might allow it to be just a name? 
             # Schema says 'package_file_source: str'
             if not intent.name.endswith(('.pkg', '.dmg', '.zip')):
                 # Warning only? Or enforcement?
                 pass
        return None
