# Jamf Pro Terraform - Analysis & Recommendations

## 📊 Analysis Summary

After analyzing both the official Jamf terraform-jamf-platform repository and the deploymenttheory/terraform-provider-jamfpro provider documentation, here are the key findings and recommendations for improving our HCL generation.

---

## 🔍 **Key Findings**

### **1. Provider Configuration (Critical)**

**Official Jamf Recommendation:**

```hcl
provider "jamfpro" {
  jamfpro_instance_fqdn                = "https://your-instance.jamfcloud.com"
  auth_method                          = "basic"  # or "oauth2"
  basic_auth_username                  = var.jamfpro_username
  basic_auth_password                  = var.jamfpro_password
  enable_client_sdk_logs               = false
  hide_sensitive_data                  = true
  token_refresh_buffer_period_seconds  = 5
  jamfpro_load_balancer_lock           = true
  mandatory_request_delay_milliseconds = 100  # IMPORTANT for API rate limiting
}
```

**What We're Currently Generating:**

```hcl
provider "jamfpro" {
  # Automatically reads from environment variables
}
```

**✅ Our approach is correct** - environment variables are the secure way to handle credentials.

---

### **2. Policy Structure (Critical Discovery)**

**Actual Required Fields from Examples:**

```hcl
resource "jamfpro_policy" "example" {
  # REQUIRED
  name    = "Policy Name"
  enabled = true

  # REQUIRED - Scope block
  scope {
    all_computers = false  # Safer default - require explicit targeting
    # User must specify: computer_ids, computer_group_ids, etc.
  }

  # REQUIRED - Payloads block (even if empty!)
  payloads {
    # At least one payload type
  }

  # OPTIONAL but common
  trigger_checkin             = false
  trigger_enrollment_complete = false
  frequency                   = "Once per computer"
  category_id                 = -1
  site_id                     = -1
}
```

**⚠️ Critical Issue:** Our system prompt is **missing the `payloads` block requirement**!

---

### **3. Terraform Best Practices from Official Repo**

#### **Parallelism Control**

```bash
export TF_CLI_ARGS_apply="-parallelism=1"
```

Reduces API errors by limiting concurrent requests.

#### **Provider Delay**

```hcl
mandatory_request_delay_milliseconds = 100
```

Prevents API rate limiting.

#### **Module Structure**

- Use modules for reusable configurations
- Separate concerns (compliance, management, security)
- Use variables for flexibility

---

## 📋 **Recommended System Prompt Updates**

### **Current Issues:**

1. ❌ Missing `payloads` block requirement
2. ❌ Not showing payload structure examples
3. ❌ Limited scope options shown
4. ⚠️ No mention of common optional fields

### **Proposed Enhanced System Prompt:**

```python
SYSTEM_PROMPT = """You are an expert Terraform HCL generator for the Jamf Pro provider (deploymenttheory/jamfpro v0.19.1).

## Output Format
1. Output ONLY valid HCL code - no markdown, no code fences, no explanatory text
2. Always include terraform and provider blocks
3. Use proper formatting and indentation

## Required Blocks

### Terraform Block (ALWAYS REQUIRED)
terraform {
  required_providers {
    jamfpro = {
      source  = "deploymenttheory/jamfpro"
      version = "~> 0.19.0"
    }
  }
}

### Provider Block (ALWAYS REQUIRED)
provider "jamfpro" {
  # Automatically reads from environment variables:
  # JAMF_URL, JAMF_USERNAME, JAMF_PASSWORD
}

## Resource-Specific Requirements

### jamfpro_policy (MOST COMMON)
REQUIRED FIELDS:
- name (String)
- enabled (Boolean)
- scope block (MANDATORY)
- payloads block (MANDATORY - even if minimal)

COMMON OPTIONAL FIELDS:
- trigger_checkin (Boolean) - default: false
- trigger_enrollment_complete (Boolean) - default: false
- frequency (String) - default: "Once per computer"
- category_id (Number) - default: -1

MINIMAL EXAMPLE:
resource "jamfpro_policy" "example" {
  name    = "Example Policy"
  enabled = true

  scope {
    all_computers = true
  }

  payloads {
    maintenance {
      recon = true
    }
  }
}

PACKAGE INSTALL EXAMPLE:
resource "jamfpro_policy" "install_app" {
  name    = "Install Application"
  enabled = true

  scope {
    all_computers = true
  }

  payloads {
    packages {
      distribution_point = "default"
      package {
        id                          = 123
        action                      = "Install"
        fill_user_template          = false
        fill_existing_user_template = false
      }
    }
  }
}

SCRIPT EXECUTION EXAMPLE:
resource "jamfpro_policy" "run_script" {
  name    = "Run Script"
  enabled = true

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = 456
      priority = "After"
    }
  }
}

### jamfpro_category
REQUIRED FIELDS:
- name (String)

OPTIONAL:
- priority (Number) - default: 9

EXAMPLE:
resource "jamfpro_category" "productivity" {
  name     = "Productivity"
  priority = 9
}

### jamfpro_smart_computer_group
REQUIRED FIELDS:
- name (String)
- is_smart (Boolean) - must be true

OPTIONAL:
- site_id (Number) - default: -1
- criteria (Block) - for filtering

EXAMPLE:
resource "jamfpro_smart_computer_group" "macos_14" {
  name     = "macOS 14+ Devices"
  is_smart = true
  site_id  = -1
}

### jamfpro_script
REQUIRED FIELDS:
- name (String)
- script_contents (String)

EXAMPLE:
resource "jamfpro_script" "example" {
  name             = "Install Homebrew"
  script_contents  = <<-EOT
    #!/bin/bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  EOT
}

### jamfpro_package
REQUIRED FIELDS:
- package_file_source (String) - file path or URL
- filename (String)

EXAMPLE:
resource "jamfpro_package" "chrome" {
  package_file_source = "https://dl.google.com/chrome/mac/stable/GoogleChrome.pkg"
  filename            = "GoogleChrome.pkg"
}

## Best Practices
1. Always use descriptive resource names (snake_case)
2. Set enabled = true for active policies
3. Use all_computers = false by default (require explicit targeting for safety)
4. Include at least one payload in policies (maintenance.recon is simplest)
5. Never include sensitive data (tokens, passwords) in HCL
6. Use category_id = -1 and site_id = -1 for default/no category
7. Prompt user to specify scope if not provided

## Validation Checklist
Before outputting HCL, verify:
- Terraform block included with correct provider version
- Provider block included
- All required fields for resource type present
- Scope block included for policies
- Payloads block included for policies (with at least one payload)
- Valid HCL syntax

Generate complete, valid, executable Terraform configurations that follow Jamf Pro best practices.
"""
```

---

## 🎯 **Immediate Action Items**

### **Priority 1: Fix System Prompt**

1. ✅ Add `payloads` block requirement
2. ✅ Add payload examples (packages, scripts, maintenance)
3. ✅ Add common optional fields
4. ✅ Update provider version to ~> 0.19.0

### **Priority 2: Test with Real Examples**

1. Generate policy with package install
2. Generate policy with script execution
3. Generate policy with maintenance (recon)
4. Verify all have required fields

### **Priority 3: Update Documentation**

1. Update `JAMF_RESOURCE_REQUIREMENTS.md` with payload info
2. Add examples to `USER_GUIDE.md`
3. Update cookbook recipes with proper payloads

---

## 📚 **Resource Examples from Official Repo**

### **Simple Category**

```hcl
resource "jamfpro_category" "communication" {
  name     = "Communication"
  priority = 9
}
```

### **Policy with Recon (Simplest)**

```hcl
resource "jamfpro_policy" "inventory_update" {
  name    = "Update Inventory"
  enabled = true

  scope {
    all_computers = true
  }

  payloads {
    maintenance {
      recon = true
    }
  }
}
```

### **Policy with Package**

```hcl
resource "jamfpro_policy" "install_chrome" {
  name    = "Install Google Chrome"
  enabled = true

  scope {
    all_computers = true
  }

  payloads {
    packages {
      distribution_point = "default"
      package {
        id     = 123  # Package ID from Jamf Pro
        action = "Install"
      }
    }
  }
}
```

---

## 🔧 **Configuration Improvements**

### **Agent Terraform Execution**

Add these to the agent's terraform execution:

```rust
// Before terraform apply
Command::new("terraform")
    .arg("init")
    .arg("-upgrade")
    .current_dir(temp_dir.path())
    .output()
    .await?;

// Then apply with parallelism control
Command::new("terraform")
    .arg("apply")
    .arg("-auto-approve")
    .arg("-parallelism=1")  // Add this!
    .current_dir(temp_dir.path())
    .env("JAMF_URL", jamf_url)
    .env("JAMF_USERNAME", jamf_username)
    .env("JAMF_PASSWORD", jamf_password)
    .output()
    .await?;
```

---

## 📊 **Comparison: Our Approach vs Official**

| Aspect           | Our Approach            | Official Jamf      | Recommendation                          |
| ---------------- | ----------------------- | ------------------ | --------------------------------------- |
| Provider config  | Env vars                | Explicit config    | ✅ Keep ours (more secure)              |
| Scope default    | `all_computers = false` | Specific targeting | ✅ Safer - require explicit scope       |
| Payloads         | ❌ Sometimes missing    | ✅ Always present  | ⚠️ **FIX THIS**                         |
| Module structure | Single file             | Modular            | ✅ Single file is fine for our use case |
| Parallelism      | Default (10)            | 1                  | ⚠️ Add `-parallelism=1`                 |
| API delay        | Not set                 | 100ms              | ⚠️ Consider adding                      |

---

## ✅ **What We're Doing Right**

1. ✅ Using environment variables for credentials
2. ✅ Including terraform + provider blocks
3. ✅ Safe default: `all_computers = false` (requires explicit targeting)
4. ✅ Generating clean, readable HCL
5. ✅ Including scope block

## ⚠️ **What Needs Fixing**

1. ❌ **Missing `payloads` block** in policies
2. ❌ Not showing payload structure options
3. ❌ No examples of common payloads (packages, scripts, maintenance)
4. ⚠️ Could add `-parallelism=1` to agent execution

---

## 🚀 **Next Steps**

1. **Update system prompt** with enhanced version above
2. **Redeploy backend** to Railway
3. **Test generation** with:
   - "Create a policy to install Chrome"
   - "Create a policy to run inventory update"
   - "Create a policy to execute a script"
4. **Verify** all generated policies have `payloads` block
5. **Update agent** to use `-parallelism=1`

---

**Last Updated**: 2025-12-04  
**Provider Version Analyzed**: v0.19.1  
**Status**: Ready for implementation
