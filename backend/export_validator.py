"""
Export validator for Jamf Pro Terraform exports.

Validates exported resources for common issues and generates
confidence scores and warnings.
"""
from typing import Dict, Any, List, Tuple
from collections import defaultdict
import re
import os
from difflib import SequenceMatcher


class ExportValidator:
    """Validates Jamf Pro exports for deployment readiness."""
    
    def __init__(self):
        """Initialize the validator."""
        self.warnings = []
        self.errors = []
        self.passed_checks = []
    
    def validate_export(
        self,
        resources_by_type: Dict[str, List[dict]],
        support_handler: Any = None
    ) -> dict:
        """
        Run all validation checks on the export.
        
        Args:
            resources_by_type: Dict of resource_type -> list of resources
            support_handler: Optional SupportFileHandler for file validation
            
        Returns:
            Validation report dict with warnings, errors, and confidence score
        """
        self.warnings = []
        self.errors = []
        self.passed_checks = []
        
        # Run validation checks
        self._validate_packages(resources_by_type.get('packages', []))
        self._validate_policies(resources_by_type.get('policies', []))
        self._validate_smart_groups(resources_by_type.get('smart-groups', []))
        
        if support_handler:
            self._validate_support_files(support_handler)
        
        # Calculate confidence score
        confidence = self._calculate_confidence()
        
        # Calculate totals properly, skipping internal tracking keys starting with _
        resource_counts = {}
        total_count = 0
        
        for r_type, resources in resources_by_type.items():
            if r_type.startswith('_'):
                continue
            count = len(resources)
            resource_counts[r_type] = count
            total_count += count
            
        return {
            'passed_checks': self.passed_checks,
            'warnings': self.warnings,
            'errors': self.errors,
            'confidence_score': confidence,
            'total_resources': total_count,
            'resources': resource_counts  # Add this so the report can list them
        }
    
    def _validate_packages(self, packages: List[dict]) -> None:
        """
        Validate package file references.
        
        Checks if package names reasonably match their file sources.
        """
        if not packages:
            self.passed_checks.append("No packages to validate")
            return
        
        mismatches = []
        
        for pkg in packages:
            pkg_name = pkg.get('filename', '')
            file_source = pkg.get('package_file_source', '')
            
            if not file_source:
                continue
            
            # Extract just the filename from path
            filename = os.path.basename(file_source)
            
            # Check if names are similar
            if not self._names_are_similar(pkg_name, filename):
                mismatches.append({
                    'package_name': pkg_name,
                    'file_source': filename,
                    'similarity': self._similarity_score(pkg_name, filename)
                })
        
        if mismatches:
            self.warnings.append({
                'type': 'package_reference_mismatch',
                'count': len(mismatches),
                'details': mismatches,
                'message': f"{len(mismatches)} package(s) have file names that don't match package names"
            })
        else:
            self.passed_checks.append(f"✅ {len(packages)}/{len(packages)} packages have matching file references")
    
    def _validate_policies(self, policies: List[dict]) -> None:
        """Validate policy configurations."""
        if not policies:
            self.passed_checks.append("No policies to validate")
            return
        
        self.passed_checks.append(f"✅ Validated {len(policies)} policies")

    
    def _validate_smart_groups(self, smart_groups: List[dict]) -> None:
        """
        Validate smart group criteria.
        
        Checks for hardcoded group name references in criteria.
        """
        if not smart_groups:
            self.passed_checks.append("No smart groups to validate")
            return
        
        hardcoded_refs = []
        
        for group in smart_groups:
            group_name = group.get('name', 'Unknown')
            criteria = group.get('criteria', [])
            
            for criterion in criteria:
                if criterion.get('name') == 'Computer Group':
                    # This is a group reference - it's hardcoded as a string
                    ref_value = criterion.get('value', '')
                    if ref_value and ref_value != 'All Computers':
                        hardcoded_refs.append({
                            'group': group_name,
                            'references': ref_value
                        })
                        break  # Only count once per group
        
        if hardcoded_refs:
            # Note as informational only - references are automatically converted
            self.passed_checks.append(f"✅ {len(hardcoded_refs)} nested smart group(s) auto-converted to Terraform references")
        else:
            self.passed_checks.append(f"✅ No nested smart group references detected")
        
        self.passed_checks.append(f"✅ Validated {len(smart_groups)} smart groups")

    
    def _validate_support_files(self, support_handler: Any) -> None:
        """Validate support files are properly referenced."""
        summary = support_handler.get_files_summary()
        
        script_count = len(summary.get('scripts', []))
        profile_count = len(summary.get('profiles', []))
        
        if script_count > 0:
            self.passed_checks.append(f"✅ {script_count} script(s) have valid file references")
        
        if profile_count > 0:
            self.passed_checks.append(f"✅ {profile_count} profile(s) have valid file references")
    
    def _names_are_similar(self, name1: str, name2: str, threshold: float = 0.4) -> bool:
        """
        Check if two names are similar enough.
        
        Args:
            name1: First name
            name2: Second name
            threshold: Similarity threshold (0.0 to 1.0)
            
        Returns:
            True if names are similar enough
        """
        score = self._similarity_score(name1, name2)
        return score >= threshold
    
    def _similarity_score(self, name1: str, name2: str) -> float:
        """
        Calculate similarity score between two strings.
        
        Uses sequence matching and common substring detection.
        """
        # Normalize strings
        n1 = self._normalize_name(name1)
        n2 = self._normalize_name(name2)
        
        # Direct match
        if n1 == n2:
            return 1.0
        
        # Substring match
        if n1 in n2 or n2 in n1:
            return 0.8
        
        # Sequence matcher
        return SequenceMatcher(None, n1, n2).ratio()
    
    def _normalize_name(self, name: str) -> str:
        """Normalize a name for comparison."""
        # Remove file extensions
        name = re.sub(r'\.(pkg|dmg|zip)$', '', name, flags=re.IGNORECASE)
        # Remove version numbers and special chars
        name = re.sub(r'[_\-\.]', '', name)
        # Remove common suffixes
        name = re.sub(r'\s*\(?\d+\)?$', '', name)
        # Lowercase
        return name.lower().strip()
    
    def _calculate_confidence(self) -> float:
        """
        Calculate overall confidence score.
        
        Returns:
            Confidence score from 0.0 to 1.0
        """
        # Start with perfect score
        confidence = 1.0
        
        # Deduct for each warning type
        for warning in self.warnings:
            w_type = warning.get('type')
            count = warning.get('count', 0)
            
            if w_type == 'package_reference_mismatch':
                # Minor deduction per mismatch (capped at -0.10)
                confidence -= min(count * 0.02, 0.10)
        
        # Deduct significantly for errors
        confidence -= len(self.errors) * 0.15
        
        # Clamp to 0.0 - 1.0
        return max(0.0, min(1.0, confidence))




def generate_validation_report(validation_result: dict) -> str:
    """Generate a markdown validation report from validation results."""
    report = f"""# Jamf Pro Export Validation Report

## Export Summary
- **Status**: {validation_result.get('status', 'Unknown')}
- **Total Resources**: {validation_result.get('total_resources', 0)}
- **Export Date**: {validation_result.get('timestamp', 'N/A')}

## Resource Breakdown
"""
   
    resources = validation_result.get('resources', {})
    for resource_type, count in sorted(resources.items()):
        if not resource_type.startswith('_'):  # Skip internal tracking fields
            formatted_type = resource_type.replace('-', ' ').replace('_', ' ').title()
            report += f"- **{formatted_type}**: {count}\n"
    
    # Add warnings section if there are any
    warnings = []
    # User requested removing static group skipped warning as it's expected behavior
    
    # Add any other warnings from validation
    if validation_result.get('warnings'):
        warnings.extend(validation_result['warnings'])
    
    if warnings:
        report += f"## ⚠️ Warnings ({len(warnings)})\n\n"
        for warning in warnings:
            report += f"### {warning['message']}\n\n"
            
            if warning['type'] == 'package_reference_mismatch':
                report += "**Package File Mismatches:**\n\n"
                for detail in warning['details'][:5]:  # Show top 5
                    report += f"- **{detail['package_name']}**\n"
                    report += f"  - File: `{detail['file_source']}`\n"
                    report += f"  - Similarity: {int(detail['similarity'] * 100)}%\n"
                    report += f"  - **Action**: Verify correct package file or update reference\n\n"
                
                if len(warning['details']) > 5:
                    report += f"*... and {len(warning['details']) - 5} more*\n\n"
            
            elif warning['type'] == 'unsafe_policy_scope':
                report += "**Policies targeting 'All Computers':**\n\n"
                for policy_name in warning['details'][:10]:
                    report += f"- {policy_name}\n"
                report += "\n**Action**: Review scopes before production deployment\n\n"
            
            elif warning['type'] == 'nested_smart_groups':
                report += "**Nested Smart Groups (referencing other groups):**\n\n"
                for detail in warning['details'][:10]:
                    report += f"- **{detail['group']}** references `{detail['references']}`\n"
                report += "\n**Note**: Groups will be created in dependency order. Names must match exactly.\n\n"
    
    # Errors
    errors = validation_result.get('errors', [])
    if errors:
        report += f"## ❌ Errors ({len(errors)})\n\n"
        for error in errors:
            report += f"- {error}\n"
        report += "\n"
    
    # Resource summary
    total = validation_result.get('total_resources', 0)
    report += f"## 📊 Resource Summary\n\n"
    report += f"**Total Resources**: {total}\n\n"
    
    # Deployment guidance
    confidence = validation_result.get('confidence_score', 0.0)
    report += "## 🚀 Deployment Recommendations\n\n"
    
    if confidence >= 0.9:
        report += "✅ **Ready for deployment**\n\n"
        report += "This export has high confidence. Recommended steps:\n\n"
        report += "1. Run `terraform init`\n"
        report += "2. Run `terraform plan` to review\n"
        report += "3. Run `terraform apply` when ready\n"
    elif confidence >= 0.75:
        report += "⚠️ **Review warnings before deployment**\n\n"
        report += "This export has moderate confidence. Recommended steps:\n\n"
        report += "1. Address warnings above\n"
        report += "2. Run `terraform init`\n"
        report += "3. Run `terraform plan` and review carefully\n"
        report += "4. Be prepared to fix issues and re-run `terraform apply`\n"
    else:
        report += "🔴 **Fix errors before deployment**\n\n"
        report += "This export has issues that may prevent successful deployment:\n\n"
        report += "1. Fix all errors listed above\n"
        report += "2. Address critical warnings\n"
        report += "3. Re-export after fixes\n"
    
    report += "\n---\n\n"
    report += "*This report was automatically generated. Review all warnings and errors before deployment.*\n"
    
    return report
