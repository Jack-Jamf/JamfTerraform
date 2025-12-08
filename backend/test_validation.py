import pytest
from intent_validator import IntentValidator
from schemas import (
    UserIntent, PolicyIntent, ScopeIntent, PolicyPayloadsIntent,
    ScriptIntent, AppInstallerIntent, PackagePayload
)

@pytest.fixture
def validator():
    catalog = ["Google Chrome", "Mozilla Firefox", "Slack"]
    return IntentValidator(app_catalog=catalog)

def test_validate_empty_intent(validator):
    intent = UserIntent(intent=None)
    assert validator.validate(intent) == "No intent identified."

def test_validate_policy_safety_all_computers(validator):
    # scope.all_computers = True should fail
    # Note: Pydantic might catch this first if model_validator is robust, 
    # but IntentValidator adds a second layer logic if Pydantic allowed it (or if checking raw dicts).
    # Since schemas.py has a validator that raises ValueError, we might not even reach IntentValidator
    # if we parse JSON first. 
    # But let's construct an object manually that bypasses pydantic validation if possible,
    # OR catch the pydantic error. 
    # Actually, IntentValidator takes a Validated Pydantic Object.
    # So if Pydantic allows it (e.g. if we remove that validator later), this catches it.
    
    # Let's try to construct one. Pydantic validator runs on init/assignment.
    # So we can't easily make an invalid one to pass to IntentValidator if schemas.py forbids it.
    # But wait, schemas.py raises ValueError on 'all_computers: True'.
    # So the LLMService.py `model_validate_json` would explode before hitting `validator.validate`.
    # That is GOOD. validation is happening.
    # But IntentValidator checks logic that isn't in Pydantic.
    # e.g. "Empty Scope".
    scope = ScopeIntent(all_computers=False) # Empty ids
    payloads = PolicyPayloadsIntent(packages=[PackagePayload(id=1)])
    policy = PolicyIntent(resource_type="policy", name="Bad Policy", scope=scope, payloads=payloads)
    
    wrapper = UserIntent(intent=policy)
    error = validator.validate(wrapper)
    assert error == "Policy must have a defined scope (Smart Group, Static Group, or Computer IDs)."

def test_validate_script_safety_forbidden_content(validator):
    script = ScriptIntent(resource_type="script", name="Malicious", script_contents="rm -rf /")
    wrapper = UserIntent(intent=script)
    error = validator.validate(wrapper)
    assert "Safety Violation" in error

def test_validate_script_empty(validator):
    script = ScriptIntent(resource_type="script", name="Empty", script_contents="   ")
    wrapper = UserIntent(intent=script)
    error = validator.validate(wrapper)
    assert "content is empty" in error

def test_validate_app_installer_valid(validator):
    app = AppInstallerIntent(resource_type="app_installer", name="Google Chrome")
    wrapper = UserIntent(intent=app)
    assert validator.validate(wrapper) is None

def test_validate_app_installer_invalid(validator):
    app = AppInstallerIntent(resource_type="app_installer", name="Flappy Bird")
    wrapper = UserIntent(intent=app)
    error = validator.validate(wrapper)
    assert "cannot verify 'Flappy Bird'" in error
    assert "supported App Installer" in error

def test_validate_app_installer_fuzzy(validator):
    app = AppInstallerIntent(resource_type="app_installer", name="Google Chrm")
    wrapper = UserIntent(intent=app)
    error = validator.validate(wrapper)
    assert "Did you mean: Google Chrome?" in error
