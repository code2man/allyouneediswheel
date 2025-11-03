
# Test Coverage Checklist

**Last Updated:** 2025-01-27
**Overall Coverage:** 62%
**Target Coverage:** 80%+


## 1. Fully Tested Modules (90%+ Coverage)

### Core Modules

* `core/currency.py` — **100%** — All currency conversion functions tested.
* `core/logging_config.py` — **96%** — Logging configuration comprehensively verified.
* `core/utils.py` — **76%** — Core utilities well covered.
* `db/database.py` — **80%** — Database operations thoroughly validated.

### Test Files

* `tests/unit/test_utils.py` — **100%** — Complete documentation coverage.
* `tests/unit/test_currency.py` — **100%** — Complete documentation coverage.
* `tests/unit/test_database.py` — **100%** — Complete documentation coverage.
* `tests/unit/test_connection.py` — **100%** — Complete documentation coverage.
* `tests/integration/test_api_options.py` — **100%** — Fully documented integration tests.
* `tests/integration/test_api_portfolio.py` — **96%** — Fully documented integration tests.

---

## 2. Partially Tested Modules (50–80% Coverage)

### API Routes

* `api/routes/options.py` — **43%**
  **Missing tests for:**

  * `/rollover` endpoint (POST)
  * `/cancel/<id>` endpoint (POST)
  * `/order/<id>/quantity` endpoint (PUT)
  * `/expirations` endpoint (GET)
  * `/check-orders` endpoint (POST)
  * Error handling (400, 500 responses)
  * Edge cases (invalid data, missing fields)

* `api/routes/portfolio.py` — **77%**
  **Missing tests for:**

  * Error scenarios
  * Edge cases

### Services

* `api/services/options_service.py` — **31%**
  **Missing tests for:**

  * `get_otm_options()` — Edge cases and error handling
  * `execute_order()` — Success and failure paths
  * `check_pending_orders()` — Order status updates
  * `cancel_order()` — Cancellation logic
  * `get_option_expirations()` — Expiration retrieval
  * Connection timeout and invalid input validation

* `api/services/portfolio_service.py` — **82%**
  **Missing tests for:**

  * Error handling edge cases
  * Connection retry logic

### Core

* `core/connection.py` — **34%**
  **Missing tests for:**

  * Asynchronous operations (low priority; external dependencies)
  * Reconnection logic
  * Error recovery

### Configuration

* `config.py` — **44%**
  **Missing tests for:**

  * Configuration file loading
  * Environment variable handling
  * Default value fallbacks
  * Validation error handling

### Utilities

* `core/utils.py` — **76%**
  **Missing tests for:**

  * Lines 82–123 (utility functions)
  * Line 169 (edge case)
  * Line 324 (specific utility function)

---

## 3. Untested Modules (<50% Coverage)

### Application Entry Points (Optional)

* `app.py` — **0%**

  * Optional: Add smoke tests for initialization.
  * Recommended: Keep as-is (configuration focus).

* `run_api.py` — **0%**

  * Optional: Add server startup tests.
  * Recommended: Keep as-is (server configuration).

---

## 4. Test Categories Overview

### Unit Tests

| Module                   | Coverage | Status            | Priority                    |
| ------------------------ | -------- | ----------------- | --------------------------- |
| `core/utils.py`          | 76%      | Good              | Medium                      |
| `core/currency.py`       | 100%     | Complete          | High                        |
| `core/logging_config.py` | 96%      | Complete          | High                        |
| `core/connection.py`     | 34%      | Incomplete        | Low (external dependencies) |
| `db/database.py`         | 80%      | Good              | High                        |
| `config.py`              | 44%      | Needs Improvement | High                        |

### Integration Tests

| Module                              | Coverage | Status            | Priority |
| ----------------------------------- | -------- | ----------------- | -------- |
| `api/routes/options.py`             | 43%      | Needs Improvement | High     |
| `api/routes/portfolio.py`           | 77%      | Good              | Medium   |
| `api/services/options_service.py`   | 31%      | Needs Improvement | High     |
| `api/services/portfolio_service.py` | 82%      | Good              | Low      |

---

## 5. Missing Test Scenarios

### API Endpoints Not Tested

**`/api/options/rollover` (POST)**

* Successful creation
* Missing fields
* Invalid option data
* Database error handling

**`/api/options/cancel/<id>` (POST)**

* Successful cancellation
* Order not found
* Already cancelled orders
* Connection errors

**`/api/options/order/<id>/quantity` (PUT)**

* Successful update
* Invalid quantity (negative or zero)
* Order not found
* Non-pending order update attempts

**`/api/options/expirations` (GET)**

* Successful retrieval
* Missing ticker parameter
* Invalid ticker
* Connection errors

**`/api/options/check-orders` (POST)**

* Successful status check
* No pending orders
* Connection errors
* Partial status updates

---

## 6. Service Methods Not Tested

**`OptionsService.get_otm_options()`**

* Multiple tickers
* OTM percentage variations
* Option type and expiration filtering
* Connection and input validation

**`OptionsService.execute_order()`**

* Successful execution
* Invalid status or missing order
* API and connection errors

**`OptionsService.check_pending_orders()`**

* Multiple orders and transitions
* Partial fills and error handling

**`OptionsService.cancel_order()`**

* Successful and failed cancellations
* API errors and invalid states

---

## 7. Error Scenarios Not Tested

* Database connection failures and query timeouts
* Constraint violations and rollbacks
* API timeouts and authentication failures
* Invalid or missing input fields
* Out-of-range or malformed data

---

## 8. Test Documentation Status

### Files with Complete Docstrings

* `tests/unit/test_utils.py`
* `tests/unit/test_currency.py`
* `tests/unit/test_database.py`
* `tests/unit/test_connection.py`
* `tests/integration/test_api_options.py`
* `tests/integration/test_api_portfolio.py`

### Files Needing Docstring Review

* `tests/unit/test_logging_config.py`

  * Minor documentation gaps in `mock_path_join` (lines 89–93, 106).

---

## 9. Test Isolation Status

### Well Isolated

* Unit tests: Independent fixtures per test.
* Database tests: Temporary databases per run.
* Integration tests: Flask app recreated per session.

### Potential Issues

* Shared `options_service` instance across tests.

  * **Status:** Currently safe (isolated databases).
  * **Recommendation:** Continue monitoring for shared state issues.

---

## 10. Priority Actions

### High Priority

1. Add tests for `api/services/options_service.py` (31% → 70%+).

   * Estimated effort: 6–8 hours.
   * Critical for business logic validation.

2. Expand `api/routes/options.py` tests (43% → 70%+).

   * Estimated effort: 4–5 hours.
   * Key API endpoints coverage improvement.

3. Add `config.py` tests (44% → 80%+).

   * Estimated effort: 2–3 hours.
   * Improves configuration reliability.

### Medium Priority

4. Add comprehensive error scenario tests (3–4 hours).
5. Expand edge case coverage (2–3 hours).

### Low Priority

6. Add light tests for entry points (`app.py`, `run_api.py`) (2–3 hours).

---

## 11. Coverage Goals

### Current State

* Overall: **62%**
* Core Modules: **76–100%**
* API Routes: **43–77%**
* Services: **31–82%**

### Target State (Phase 1)

* Overall: **70%+**
* Core Modules: **80%+**
* API Routes: **70%+**
* Services: **70%+**

### Target State (Phase 2)

* Overall: **80%+**
* Core Modules: **90%+**
* API Routes: **80%+**
* Services: **80%+**

---

## 12. Quick Reference

### Generate Coverage Reports

```bash
# Terminal summary
pytest --cov=. --cov-report=term-missing

# HTML report
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

### Identify Missing Lines

Use the coverage output to locate untested sections:

* `api/routes/options.py`: Lines 75–78, 89, 103–107, etc.
* `api/services/options_service.py`: Lines 39–80, 118–339, etc.
* `config.py`: Lines 27–28, 32–34, 46–55, etc.

---

**Next Steps:** Refer to `NEXT_STEPS.md` for detailed implementation guidance.

---
