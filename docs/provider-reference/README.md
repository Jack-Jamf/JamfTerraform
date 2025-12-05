# Provider Reference Documentation

This directory contains local copies of Terraform provider repositories for reference and development.

## Contents

### `terraform-provider-jamfpro/`

Local clone of the [deploymenttheory/terraform-provider-jamfpro](https://github.com/deploymenttheory/terraform-provider-jamfpro) repository.

**Purpose:**

- Reference for resource schemas and required fields
- Example Terraform configurations
- Provider documentation
- Schema validation

**Clone Command:**

```bash
cd docs/provider-reference
git clone https://github.com/deploymenttheory/terraform-provider-jamfpro.git
```

**Update Command:**

```bash
cd docs/provider-reference/terraform-provider-jamfpro
git pull
```

## Usage

This reference material is used to:

1. **Validate HCL generation** - Ensure our LLM generates correct resource structures
2. **Update system prompts** - Keep guardrails aligned with provider requirements
3. **Test configurations** - Verify generated HCL against provider examples
4. **Schema reference** - Look up required/optional fields for resources

## Note

The provider reference is gitignored and not committed to this repository. Each developer should clone it locally if needed.

---

**Last Updated**: 2025-12-04
