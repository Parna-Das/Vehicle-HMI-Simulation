# Add Climate Temperature Down Control Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a "Temp -" button and decrease temperature functionality to the HMI climate control section, update the Page Object Model, and add automated tests.

**Architecture:** Modify `app/static/index.html` to include a temperature decrement button and JavaScript handler, update `tests/pages/hmi_page.py` with POM method, and add UI test in `tests/ui/test_hmi_e2e.py`.

**Tech Stack:** Python, Playwright, Pytest, HTML/JavaScript.

**Spec:** User request to add option for temp down along with temp up in the climate section.

## Global Constraints

- Python 3.10+
- Pytest as test runner
- Playwright for UI testing

## Review Focus

- **Temperature Boundary / Lower Limit**: What happens if temperature is decreased repeatedly? (Expected: Decrements by 0.5°C down to minimum limit).

---

### Task 1: Add Temp Down UI and POM Support

**Files:**
- Modify: `app/static/index.html`
- Modify: `tests/pages/hmi_page.py`
- Modify: `tests/ui/test_hmi_e2e.py`

**Interfaces:**
- Produces: `#temp-driver-down` button and `decrease_temp()` JS function, `decrease_temperature()` POM method.

- [ ] **Step 1: Add test for temperature decrease in `tests/ui/test_hmi_e2e.py`**

```python
def test_hmi_climate_temp_down(hmi):
    hmi.click_climate_control()
    initial_temp = float(hmi.page.locator("#temp-driver-display").inner_text())
    hmi.decrease_temperature()
    new_temp = float(hmi.page.locator("#temp-driver-display").inner_text())
    assert new_temp == initial_temp - 0.5
```

- [ ] **Step 2: Run test to verify it fails**
Run: `$env:PYTHONPATH = "."; pytest tests/ui/test_hmi_e2e.py -k test_hmi_climate_temp_down -v`
Expected: FAIL (element or method not found)

- [ ] **Step 3: Update `app/static/index.html` to add Temp - button and `decreaseTemp()` function**

Add button:
```html
<button id="temp-driver-down" onclick="decreaseTemp()">Temp -</button>
```
Add JS function:
```javascript
function decreaseTemp() {
    const el = document.getElementById('temp-driver-display');
    el.innerText = (parseFloat(el.innerText) - 0.5).toFixed(1);
}
```

- [ ] **Step 4: Update `tests/pages/hmi_page.py` to add `temp_driver_down` selector and `decrease_temperature()` method**

```python
self.temp_driver_down = "#temp-driver-down"

def decrease_temperature(self):
    """Decrease driver temperature."""
    self.page.click(self.temp_driver_down)
```

- [ ] **Step 5: Run test to verify it passes**
Run: `$env:PYTHONPATH = "."; pytest tests/ui/test_hmi_e2e.py -k test_hmi_climate_temp_down -v`
Expected: PASS

- [ ] **Step 6: Run full test suite and commit**
Run: `$env:PYTHONPATH = "."; pytest`
Expected: All tests pass.

```bash
git add app/static/index.html tests/pages/hmi_page.py tests/ui/test_hmi_e2e.py
git commit -m "feat(hmi): add temperature down control to climate section"
Co-Authored-By: Claude Code <noreply@anthropic.com>
```
