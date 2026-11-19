# Task 3: Test Fixtures & Page Object Model (POM) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement test fixtures and Page Object Model (POM) for HMI UI and API tests.

**Architecture:** Use pytest fixtures for setup/teardown and a POM structure to encapsulate UI interactions.

**Tech Stack:** Playwright, Pytest, Python.

**Spec:** [Based on requirements from initial project scaffolding]

## Global Constraints

- Python 3.10+
- Pytest as the test runner
- Playwright for UI automation
- Follow established project structure (`app/` for backend, `tests/` for tests)

## Review Focus

- **Fixture Setup Failure**: What happens if the mock server doesn't start? Expected: Test suite fails gracefully with clear error. (Test: `test_api_connection_failure` in `tests/conftest.py`)
- **Page Object Timeout**: What happens if a UI element takes too long to load? Expected: Playwright timeout is reached, test fails with element not found. (Test: `test_hmi_element_timeout` in `tests/pages/hmi_page.py`)
- **Invalid State Setup**: What happens if an invalid state is set for a fixture? Expected: Fixture raises an exception or test assertion fails. (Test: `test_invalid_fixture_state` in `tests/conftest.py`)

---

### Task 3.1: Configure Pytest Fixtures

**Files:**
- Create: `tests/conftest.py`

**Interfaces:**
- Produces: `pytest_fixture` (e.g., `api_client`, `hmi_page`)

- [ ] **Step 1: Create `tests/conftest.py` with FastAPI test client fixture**

- [ ] **Step 2: Add Playwright page fixture for HMI UI testing**

- [ ] **Step 3: Run pytest to ensure fixtures are discovered**

Run: `pytest --fixtures`
Expected: `api_client` and `hmi_page` are listed.

- [ ] **Step 4: Commit**

```bash
git add tests/conftest.py
git commit -m "feat(test): configure pytest fixtures"
```

### Task 3.2: Implement Page Object Model (POM)

**Files:**
- Create: `tests/pages/base_page.py`
- Create: `tests/pages/hmi_page.py`

**Interfaces:**
- Consumes: `page` (Playwright Page)
- Produces: `HmiPage` class with methods for HMI interactions (e.g., `click_climate_control`, `play_media`)

- [ ] **Step 1: Implement `BasePage` in `tests/pages/base_page.py`**

- [ ] **Step 2: Implement `HmiPage` in `tests/pages/hmi_page.py` inheriting from `BasePage`**

- [ ] **Step 3: Add basic UI interaction methods to `HmiPage`**

- [ ] **Step 4: Run pytest (no tests yet) to check for syntax errors**

Run: `pytest`
Expected: Passes (no collected tests)

- [ ] **Step 5: Commit**

```bash
git add tests/pages/base_page.py tests/pages/hmi_page.py
git commit -m "feat(test): implement Page Object Model"
```
