from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, Dict, Any, Literal, Union

# --- Base Intent ---
class BaseIntent(BaseModel):
    resource_type: Literal['policy', 'script', 'category', 'package', 'smart_group', 'static_group', 'app_installer']

# --- Scope Schema ---
class ScopeIntent(BaseModel):
    all_computers: bool = Field(False, description="Must be False. Use explicit targeting.")
    computer_group_ids: Optional[List[int]] = None
    computer_ids: Optional[List[int]] = None
    building_ids: Optional[List[int]] = None
    department_ids: Optional[List[int]] = None

    @model_validator(mode='after')
    def validate_targeting(self):
        if self.all_computers:
            raise ValueError("Targeting 'All Computers' is strictly forbidden. Please specify a group, building, or department.")
        return self

# --- Payload Schemas ---
class PackagePayload(BaseModel):
    id: Optional[int] = None
    action: Literal['Install', 'Cache', 'Install Cached'] = 'Install'

class ScriptPayload(BaseModel):
    id: Optional[int] = None
    priority: Literal['Before', 'After'] = 'After'
    parameter4: Optional[str] = None
    parameter5: Optional[str] = None
    parameter6: Optional[str] = None
    parameter7: Optional[str] = None
    parameter8: Optional[str] = None
    parameter9: Optional[str] = None
    parameter10: Optional[str] = None
    parameter11: Optional[str] = None

class MaintenancePayload(BaseModel):
    recon: bool = False

class PolicyPayloadsIntent(BaseModel):
    packages: Optional[List[PackagePayload]] = None
    scripts: Optional[List[ScriptPayload]] = None
    maintenance: Optional[MaintenancePayload] = None
    
    @model_validator(mode='after')
    def validate_payloads(self):
        if not any([self.packages, self.scripts, self.maintenance]):
            raise ValueError("Policy must have at least one payload (e.g. packages, scripts, or maintenance).")
        return self

# --- Resource Intents ---

class PolicyIntent(BaseIntent):
    resource_type: Literal['policy']
    name: str
    enabled: bool = True
    scope: ScopeIntent
    payloads: PolicyPayloadsIntent

class ScriptIntent(BaseIntent):
    resource_type: Literal['script']
    name: str
    script_contents: str

class CategoryIntent(BaseIntent):
    resource_type: Literal['category']
    name: str
    priority: int = 9

class PackageIntent(BaseIntent):
    resource_type: Literal['package']
    name: str # filename usually
    package_file_source: str

class SmartGroupIntent(BaseIntent):
    resource_type: Literal['smart_group']
    name: str
    is_smart: bool = True
    criteria: list = [] # Simplified for now

class StaticGroupIntent(BaseIntent):
    resource_type: Literal['static_group']
    name: str

class AppInstallerIntent(BaseIntent):
    resource_type: Literal['app_installer']
    name: str
    enabled: bool = True
    deployment_type: Literal['SELF_SERVICE', 'INSTALL_AUTOMATICALLY'] = 'SELF_SERVICE'
    update_behavior: Literal['AUTOMATIC', 'MANUAL'] = 'AUTOMATIC'
    category_id: int = -1
    site_id: int = -1
    smart_group_id: int = 1

# --- Master Intent ---
class UserIntent(BaseModel):
    """
    The structured intent extracted from the user's prompt.
    If the user's request is incomplete or invalid, the validation error
    will guide the bot's next question.
    """
    intent: Optional[Union[PolicyIntent, ScriptIntent, CategoryIntent, PackageIntent, SmartGroupIntent, StaticGroupIntent, AppInstallerIntent]] = None
    missing_info_question: Optional[str] = Field(None, description="If intent is incomplete/invalid, ask this question.")
