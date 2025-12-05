# Implementation Plan: Recursive HCL Generation with Dependencies

**Goal**: Enable users to download a Terraform file (`.tf`) for a resource that _includes_ all its dependencies (e.g., a Policy + its Scripts + Packages + Categories) in a single, valid configuration.

## 1. Backend: Recursive Dependency Fetching

Currently, `DependencyResolver` identifies dependency IDs but does not fetch their full data.

- [ ] Create `RecursiveResourceFetcher` service.
  - Input: `resource_type`, `resource_id`.
  - Logic: Use BFS/DFS to traverse the dependency graph.
  - Fetch full details for every node visited.
  - Maintain a cache `visited_resources` to avoid duplicates (e.g. multiple policies using same category).
- [ ] Update `JamfClient` if needed to bulk fetch or optimize (optional, iterative is fine for now).

## 2. Backend: Enhanced HCL Generation

- [ ] Update `HCLGenerator.generate_file` (or similar) to accept a list of heterogenous resources.
  - Ensure it sorts them topologically (Categories first, then Packages/Scripts, then Policies).
  - Use `DependencyResolver.topological_sort` (already exists!)
- [ ] Create new endpoint `/api/jamf/resource-bundle` (or update `resource-detail` with `include_dependencies` flag).
  - Returns the combined HCL string for the whole tree.

## 3. Frontend: "Download Full Chain" Feature

- [ ] Update `ResourceDetailPanel.tsx`.
  - Add toggle "Include Dependencies" (default: checked?).
  - When clicking "Download .tf", call the bundle endpoint.
  - Alternatively, fetch the bundle alongside the detail and just switch the view.

## 4. Verification

- [ ] Verify a Policy generates: `resource "jamfpro_policy"`, `resource "jamfpro_script"`, `resource "jamfpro_category"`.
- [ ] Verify `terraform plan` is theoretically possible with the output.

## User Review Required

- Does this scope verify your needs?
