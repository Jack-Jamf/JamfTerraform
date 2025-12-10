# Proporter Bug Reproduction Steps

## Reported Issue

When attempting to export a Jamf instance via Proporter ("Instance Summary" → "Download as Terraform (ZIP)"), the process:

1. Hangs during the "Generating Export" phase
2. Eventually downloads a file with no extension
3. The file contains what appears to be a UDID instead of a ZIP archive

## Steps to Reproduce

1. Navigate to `http://localhost:5173`
2. Connect to Jamf Pro with valid credentials
3. Click "📦 Proporter" button
4. Click "📊 Instance Summary" to scan the instance
5. Wait for scan to complete and show resource summary
6. Click "⬇️ Download as Terraform (ZIP)" button
7. Observe loading spinner with "📦 Generating Export" message
8. Wait for process to complete
9. **Result**: Downloads a file with no extension containing unexpected content (UDID-like string)

## Expected Behavior

- Backend should generate a ZIP file containing:
  - Terraform .tf files for each resource type
  - provider.tf with configuration
  - README.md with usage instructions
  - support_files/ directory with scripts and config profiles
  - VALIDATION_REPORT.md
- Frontend should download a properly named ZIP file (e.g., `jamf_terraform_instance_20251210_082334.zip`)
- File should be a valid ZIP archive

## Actual Behavior

- Request appears to hang/timeout
- Downloads file with no extension
- File content appears to be JSON or plain text (possibly an error response or request ID)

## Potential Root Causes

1. **Backend Timeout**: Large instance exports may exceed request timeout limits
2. **Error Response Mishandling**: Backend returns JSON error, but frontend treats it as a blob
3. **Content-Type Mismatch**: Response has wrong content-type header
4. **Streaming Issue**: StreamingResponse not properly handled by fetch API

## Environment

- **Frontend**: React + Vite (localhost:5173)
- **Backend**: FastAPI on Railway (https://jamfaform-production.up.railway.app)
- **Endpoint**: `/api/jamf/bulk-export`
- **Response Type**: `StreamingResponse` with `application/zip` media type
