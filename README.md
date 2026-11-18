# Automotive HMI & Backend API Automation Suite

Comprehensive test automation framework for modern automotive infotainment Human-Machine Interfaces (HMI) and vehicle backend APIs.

## Architecture & Tech Stack

- **UI Automation**: Playwright (Python) for HMI touch display simulation, dashboard controls, climate control, media playback, and navigation testing.
- **API Automation**: Pytest, Requests, and FastAPI/Uvicorn for backend telemetry, vehicle status services, and command-and-control APIs.
- **Reporting**: Allure Reports for detailed test execution metrics, step logging, and screenshots.

## Installation & Setup

1. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

## Running Tests

- Run all tests:
  ```bash
  pytest
  ```
- Run API tests:
  ```bash
  pytest -m api
  ```
- Run HMI UI tests:
  ```bash
  pytest -m hmi
  ```

## License
Proprietary / Internal Automation Suite.
