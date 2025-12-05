# Implementation Plan: Git Integration

**Goal**: Enable the application to commit generated Terraform HCL directly to a connected Git repository.

## 1. Backend: Git Service

- [ ] Create `GitService` class in `backend/git_service.py`.
  - Methods: `clone_or_pull()`, `checkout_branch()`, `commit_file()`, `push()`.
  - Use `subprocess` to execute git commands.
  - workspace: Use a dedicated subdirectory (e.g., `backend/git_workspace`) to check out the repo.
- [ ] Add Configuration Management.
  - Store Repo URL, Branch, User, Email, PAT.
  - Use environment variables (`.env`) or a config file (`git_config.json`) secure handling.

## 2. API Endpoints

- [ ] `POST /api/git/config`: Configure repository settings (and test connection).
- [ ] `POST /api/git/commit`:
  - Input: `filename`, `content`, `message`.
  - Logic: Update repo, write file, commit, push.

## 3. Frontend: Git Configuration

- [ ] Create `GitSettingsModal.tsx`.
  - Inputs: Repository URL, Token/PAT, Branch, Author Name/Email.
  - "Test Connection" button.
- [ ] Add "Settings" button to `ProporterMenu` header.

## 4. Frontend: Commit Action

- [ ] Update `ResourceDetailPanel.tsx`.
  - Add "Commit to Git" button.
  - On click: Open small interface for "Commit Message" and "File Path".
  - Execute API call.

## Security Note

- Credentials will be handled securely (environment variables or session-based).

## Questions for User

- Should we use a specific folder structure in the repo (e.g. `terraform/resources/`)?
- Do you prefer `GitPython` library or native `git` CLI calls? (Will assume CLI for minimal deps).
