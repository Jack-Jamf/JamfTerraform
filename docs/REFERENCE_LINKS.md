# Jamf Terraform Reference Links

## Training & Guides

- [Terraform Training - Jamf Pro](https://github.com/deploymenttheory/terraform-training-jamfpro/tree/main/training_materials_v2) - Official training materials
- [Terraform 101: Resources and Data Sources](https://macadminmusings.com/blog/2025/10/28/terraform-101-resources-and-data-sources/) - Blog post on Mac Admin Musings
- [Reverse Engineering Infrastructure to Terraform HCL](https://medium.com/@xpiotrkleban/reverse-engineering-existing-infrastructure-to-terraform-hcl-files-453420059ef9) - Medium article

## Example Repositories

- [terraform-demo-jamfpro-v2](./terraform-demo-jamfpro-v2) - Replication demo with dependencies
- [terraform-jamfpro-starter](./terraform-jamfpro-starter) - Starter template by Neil Martin
- [terraform-jamfplatform-examples](./terraform-jamfplatform-examples) - Platform examples by Neil Martin

## Import Tools

- [jamftf-python-terraform-importer](./jamftf-python-terraform-importer) - **Python tool for importing Jamf Pro to Terraform**
  - Supports: Scripts, Policies, Config Profiles, Categories, Computer Groups, Searches, Extension Attributes
  - Generates Terraform import blocks
  - Uses Classic Jamf API
- [Terraformer](https://github.com/GoogleCloudPlatform/terraformer) - General infrastructure-to-Terraform tool

## Key Insights

### From jamftf-python-terraform-importer

- Uses `jamfpy` library for API access
- Generates Terraform `import` blocks (not full HCL resource definitions)
- Modular resource design with base `Resource` class
- Each resource type has its own class extending `Resource`
- Output format: Terraform import statements that can be run with `terraform import`

### Import vs Generate

- **Import blocks** reference existing state: `import { to = resource_type.name; id = "123" }`
- **HCL generation** creates full resource definitions with all attributes
- Our Proporter should generate full HCL, not just import blocks
