# Root Cause Analysis: Proporter Export Hanging

## Issue Summary

Instance export via Proporter hangs during generation and downloads a file with no extension containing what appears to be a UDID (likely an error response or request ID).

## Root Cause

**Request Timeout + Error Response Mishandling**

The bug has **two components**:

### 1. Backend Timeout (Primary Issue)

**Location**: Railway hosting platform + `/api/jamf/bulk-export` endpoint

the `bulk_export_resources` function in `backend/main.py` performs these operations synchronously:

1. Authenticates with Jamf Pro
2. Fetches ALL requested resources recursively (lines 360-376)
3. Processes support files for each resource (lines 379-392)
4. Performs topological sort
5. Generates HCL for all resources
6. Creates ZIP file with all content
7. Returns StreamingResponse

For large Jamf instances (e.g., 100+ policies, 50+ scripts, 30+ profiles), this can easily take **5-10+ minutes**.

**Railway has a request timeout limit** (typically 300 seconds / 5 minutes for hobby tier). When the request exceeds this, Railway returns an error response (likely JSON with an error ID/message or request ID that looks like a UDID).

### 2. Frontend Error Handling (Secondary Issue)

**Location**: `frontend/src/services/ExecutionService.ts` lines 19-50

The `bulkExport` method checks `response.ok` and logs errors, but when the backend times out:

- Railway might return a 504 Gateway Timeout with JSON body
- The frontend still calls `response.blob()` on line 45
- This creates a Blob from the JSON error response
- The Blob is treated as a file and downloaded

**The frontend never checks the Content-Type header** to verify it's actually receiving `application/zip`.

## Evidence

1. **Backend logs** (line 359): `print(f"[BULK EXPORT] Received {len(request.resources)} resources to export")` - likely shows the request started
2. **No response returned** before timeout
3. **File downloaded** contains text/JSON instead of ZIP binary data
4. **No file extension** - the error response doesn't have Content-Disposition header with filename

## Impact

- **Severity**: High (feature completely broken for medium-to-large instances)
- **Scope**: All instance exports via Proporter
- **Affected Users**: Anyone with >50 total resources in their Jamf instance

## Why It Worked Before (Hypothesis)

- Smaller test instances completed within timeout window
- Testing was done on instances with <20 resources total
