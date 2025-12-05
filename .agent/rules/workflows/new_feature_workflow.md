---
trigger: always_on
---

# Workflow: /new_feature_workflow (Master Script)

**Goal:** Implement a new feature based on the user's last prompt, ensuring all code is clean, tested, and documented.

1.  **Planning Phase (Project Planner):** The Planner Agent interprets the user's prompt and generates a detailed, atomic `Implementation Plan Artifact`. Request user approval.
2.  **Building Phase (Code Builder):** The Builder Agent executes the approved plan, step-by-step.
3.  **Testing Phase (QA Agent):** The QA Agent generates and runs a `Test Case Artifact` against the Builder's changes to ensure all requirements are met.
4.  **Completion & Suggestion:** Upon successful test (PASS), the system will automatically trigger the **Next Step Suggestion Protocol** (Rule #3) to offer the user the next logical action.