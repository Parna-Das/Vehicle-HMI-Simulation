# Automotive API Test Suite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a comprehensive, robust pytest API test suite covering telemetry, climate, navigation, and media endpoints with boundary validation, error handling, and stateful verification.

**Architecture:** Expand API tests into dedicated test modules (`tests/api/test_telemetry.py`, `tests/api/test_climate.py`, `tests/api/test_navigation.py`, `tests/api/test_media.py`) using the `api_client` pytest fixture from `tests/conftest.py`.

**Tech Stack:** Pytest, FastAPI TestClient, Python.

**Spec:** [Based on backend API specifications in `app/main.py`]

## Global Constraints

- Python 3.10+
- Pytest as the test runner
- Use `api_client` fixture for all endpoint tests
- Follow established project structure (`tests/api/` or `tests/`)

## Review Focus

- **Boundary Overflow / Underflow**: What happens if telemetry speed exceeds 240.0 or drops below 0.0? Expected: HTTP 422 Unprocessable Entity. (Test: `test_telemetry_boundaries` in `tests/api/test_telemetry.py`)
- **Malformed JSON Payload**: What happens if climate settings send invalid types (string instead of float)? Expected: HTTP 422 Unprocessable Entity. (Test: `test_climate_malformed_payload` in `tests/api/test_climate.py`)
- **Missing Navigation Destination**: What happens if navigation request lacks required `destination` field? Expected: HTTP 422 Unprocessable Entity. (Test: `test_navigation_missing_destination` in `tests/api/test_navigation.py`)
- **Invalid Media Action**: What happens if media control action is unknown? Expected: HTTP 422 Unprocessable Entity. (Test: `test_media_invalid_action` in `tests/api/test_media.py`)
- **Concurrent / Sequential State Persistence**: What happens if state updates are chained sequentially? Expected: Each endpoint correctly maintains updated state. (Test: `test_state_persistence_chain` in `tests/api/test_telemetry.py`)

---

### Task 4.1: Telemetry API Test Suite

**Files:**
- Create: `tests/api/__init__.py`
- Create: `tests/api/test_telemetry.py`

**Interfaces:**
- Consumes: `api_client` fixture from `tests/conftest.py`
- Produces: Comprehensive telemetry tests covering GET/PUT, valid updates, gear validation, tire pressure validation, and boundary limits.

- [ ] **Step 1: Write failing test for telemetry speed boundary overflow in `tests/api/test_telemetry.py`**

```python
def test_telemetry_speed_boundary_overflow(api_client):
    payload = {
        "speed": 250.0, # Exceeds max 240.0
        "rpm": 2200,
        "gear": "D",
        "fuel_level": 78.5,
        "battery_level": 95.0,
        "tire_pressure": {"fl": 32.0, "fr": 32.0, "rl": 31.5, "rr": 31.5},
        "headlights": True,
        "doors_locked": True,
        "timestamp": 1234567890.0
    }
    response = api_client.put("/api/v1/telemetry", json=payload)
    assert response.status_code == 422
```

- [ ] **Step 2: Run test to verify it passes (or fails if not implemented)**

Run: `pytest tests/api/test_telemetry.py -v`
Expected: PASS (since validation is already in FastAPI model) or FAIL if endpoint requires implementation.

- [ ] **Step 3: Add full telemetry test suite to `tests/api/test_telemetry.py`**
Include tests for gear validation (P, R, N, D, S), tire pressure bounds (15-50), and state persistence.

- [ ] **Step 4: Run pytest on telemetry tests**

Run: `pytest tests/api/test_telemetry.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/api/
git commit -m "feat(test): add telemetry API test suite"
```

### Task 4.2: Climate API Test Suite

**Files:**
- Create: `tests/api/test_climate.py`

**Interfaces:**
- Consumes: `api_client` fixture
- Produces: Climate test suite covering GET/POST/PUT, temperature ranges (16-30), fan speed (0-7), and seat heaters (0-3).

- [ ] **Step 1: Create `tests/api/test_climate.py` with temperature range and fan speed tests**

- [ ] **Step 2: Run pytest on climate tests**

Run: `pytest tests/api/test_climate.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/api/test_climate.py
git commit -m "feat(test): add climate API test suite"
```

### Task 4.3: Navigation & Media API Test Suites

**Files:**
- Create: `tests/api/test_navigation.py`
- Create: `tests/api/test_media.py`

**Interfaces:**
- Consumes: `api_client` fixture
- Produces: Navigation tests (set destination, cancel, active status) and Media tests (play, pause, next, prev, volume adjustment).

- [ ] **Step 1: Create `tests/api/test_navigation.py` and `tests/api/test_media.py`**

- [ ] **Step 2: Run full API test suite**

Run: `pytest tests/api/ -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add tests/api/test_navigation.py tests/api/test_media.py
git commit -m "feat(test): add navigation and media API test suites"
```
