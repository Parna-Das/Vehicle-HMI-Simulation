# Playwright UI End-to-End Test Suite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement robust end-to-end UI tests for the Automotive HMI using Playwright and Pytest.

**Architecture:** Create a simple HTML-based HMI Simulation page (`app/templates/index.html` or served by FastAPI) to act as the Infotainment System interface, then run Playwright tests against it using the `hmi_page` POM fixture.

**Tech Stack:** Playwright, Pytest, FastAPI, Python.

**Spec:** [Based on simulated infotainment requirements]

## Global Constraints

- Python 3.10+
- Pytest as the test runner
- Playwright for UI tests
- POM-based browser test design using `BasePage` and `HmiPage`

## Review Focus

- **UI Button Event Failures**: What happens if a button does not trigger the expected state change? Expected: Playwright selector fails or assertion fails. (Test: `test_climate_button_failures` in `tests/ui/test_hmi_e2e.py`)
- **Slow Endpoint Mock**: What happens if the API reacts slowly? Expected: Page objects handles asynchronous state loading. (Test: `test_navigation_async_loading` in `tests/ui/test_hmi_e2e.py`)
- **Invalid State/Input Handling**: What happens if invalid input is entered into navigation? Expected: UI shows error styling or state does not submit. (Test: `test_hmi_invalid_navigation_input` in `tests/ui/test_hmi_e2e.py`)

---

### Task 5.1: Create Infotainment HMI Web Interface

**Files:**
- Modify: `app/main.py` (Add HTML route / index serving)
- Create: `app/static/index.html` (Mock simulated infotainment dashboard)

**Interfaces:**
- Produces: HTML UI with elements matching selectors in `HmiPage` (`#climate-tab`, `#media-tab`, `#nav-tab`, `#ac-toggle`, etc.)

- [ ] **Step 1: Create `app/static/index.html` representing HMI control panel**

- [ ] **Step 2: Add static file mount or HTML response to `app/main.py`**

- [ ] **Step 3: Run FastAPI and verify dashboard loads**

- [ ] **Step 4: Commit**

```bash
git add app/
git commit -m "feat(hmi): create mock dashboard interface for UI tests"
```

### Task 5.2: Implement End-to-End UI Test Suite

**Files:**
- Create: `tests/ui/test_hmi_e2e.py`

**Interfaces:**
- Consumes: `hmi_page` from `tests/conftest.py`
- Produces: Complete Playwright tests verifying AC toggles, Temperature adjust, Navigation destination settings, and Media Play/Pause action.

- [ ] **Step 1: Write failing Playwright test for AC Toggle**

- [ ] **Step 2: Implement full E2E Playwright test suite in `tests/ui/test_hmi_e2e.py`**

- [ ] **Step 3: Run full Playwright test suite**

Run: `pytest tests/ui/ -v`
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add tests/ui/
git commit -m "feat(test): add Playwright end-to-end UI tests"
```
