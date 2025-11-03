# AllYouNeedIsWheel Test Suite

This directory contains comprehensive tests for the AllYouNeedIsWheel application, following TDD principles and best practices.

## Structure

```
tests/
├── __init__.py                    # Test package initialization
├── conftest.py                    # Pytest configuration and shared fixtures
├── fixtures/                      # Test data factories and fixtures
│   ├── __init__.py
│   └── test_data_factories.py    # Data factory functions
├── unit/                          # Unit tests for individual components
│   ├── __init__.py
│   ├── test_utils.py             # Tests for core.utils
│   ├── test_currency.py          # Tests for core.currency
│   ├── test_logging_config.py   # Tests for core.logging_config
│   ├── test_database.py          # Tests for db.database
│   └── test_connection.py        # Tests for core.connection (mocked)
└── integration/                  # Integration tests for API endpoints
    ├── __init__.py
    ├── test_api_options.py       # Tests for /api/options endpoints
    └── test_api_portfolio.py     # Tests for /api/portfolio endpoints
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run with Coverage Report
```bash
pytest --cov=. --cov-report=html
```

### Run Specific Test Suite
```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/
```

### Run Specific Test File
```bash
pytest tests/unit/test_database.py
```

### Run Specific Test
```bash
pytest tests/unit/test_database.py::TestOptionsDatabase::test_save_order_basic
```

### Run Tests with Verbose Output
```bash
pytest -v
```

### Run Tests and Show Print Statements
```bash
pytest -s
```

## Test Categories

### Unit Tests
Unit tests are located in `tests/unit/` and test individual components in isolation:
- **test_utils.py**: Utility functions (date parsing, formatting, market hours, etc.)
- **test_currency.py**: Currency conversion utilities
- **test_logging_config.py**: Logging configuration
- **test_database.py**: Database operations (CRUD, filtering, etc.)
- **test_connection.py**: IB connection handling (mocked)

### Integration Tests
Integration tests are located in `tests/integration/` and test API endpoints:
- **test_api_options.py**: Options API endpoints (OTM options, orders, execution)
- **test_api_portfolio.py**: Portfolio API endpoints (summary, positions, weekly income)

## Test Fixtures

Fixtures are defined in `conftest.py` and can be used across all tests:
- `temp_db`: Temporary SQLite database for testing
- `sample_order_data`: Sample order data dictionary
- `sample_portfolio_data`: Sample portfolio data dictionary
- `mock_ib_connection`: Mock Interactive Brokers connection
- `mock_config`: Mock configuration dictionary
- `flask_app`: Flask application instance for testing
- `client`: Flask test client
- `mock_ticker`: Mock ticker object
- `mock_contract`: Mock contract object
- `mock_option_contract`: Mock option contract object

## Test Data Factories

Test data factories are in `tests/fixtures/test_data_factories.py`:
- `create_order_data()`: Create order data with customizable overrides
- `create_call_order_data()`: Create CALL option order data
- `create_rollover_order_data()`: Create rollover order data
- `create_portfolio_data()`: Create portfolio data
- `create_option_chain_data()`: Create option chain data
- `create_account_summary_data()`: Create account summary data
- `get_future_friday()`: Get next Friday date
- `get_future_monthly_expiration()`: Get next monthly expiration

## Writing New Tests

### Unit Test Example
```python
def test_function_name(self, fixture_name):
    """Should describe expected behavior"""
    # Arrange
    input_data = "test"
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_value
```

### Integration Test Example
```python
def test_api_endpoint(self, client, mock_ib_connection):
    """Should return expected response"""
    with patch('module.Service._ensure_connection', return_value=mock_ib_connection):
        response = client.get('/api/endpoint')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'expected_field' in data
```

## Test Coverage

Current test coverage targets:
- **Unit Tests**: 90%+ coverage for core modules
- **Integration Tests**: 80%+ coverage for API endpoints
- **Critical Paths**: 100% coverage (order execution, portfolio retrieval)

View coverage reports:
```bash
# HTML report
pytest --cov=. --cov-report=html
open htmlcov/index.html  # Mac/Linux
start htmlcov/index.html  # Windows
```

## Continuous Integration

Tests are designed to run in CI/CD pipelines:
- Fast execution (< 5 minutes for full suite)
- No external dependencies required (mocked)
- Deterministic results
- Clear failure messages

## Troubleshooting

### Import Errors
If you encounter import errors:
```bash
# Ensure you're in the project root
cd /path/to/allyouneediswheel

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Database Errors
Tests use temporary databases that are automatically cleaned up. If you see database errors:
- Ensure SQLite is available
- Check file permissions in temp directory

### Mock Connection Errors
Integration tests mock the IB connection. If tests fail:
- Ensure mocks are properly configured in `conftest.py`
- Check that patch decorators match actual import paths

## Best Practices

1. **Follow AAA Pattern**: Arrange, Act, Assert
2. **One Assertion per Test**: Focus each test on one behavior
3. **Descriptive Names**: Test names should describe what is being tested
4. **Use Fixtures**: Reuse test data and mocks via fixtures
5. **Mock External Dependencies**: Never use real IB connections in tests
6. **Clean Up**: Tests should leave no side effects
7. **Fast Tests**: Unit tests should run in < 1 second each
8. **Independent Tests**: Tests should not depend on each other

## Maintenance

### Adding Tests for New Features
1. Write failing test first (TDD Red phase)
2. Implement minimal code to pass (TDD Green phase)
3. Refactor while keeping tests green (TDD Blue phase)
4. Ensure test coverage > 90%

### Updating Tests for Code Changes
1. Update tests when APIs change
2. Maintain backward compatibility tests
3. Update fixtures when data structures change
4. Keep test data factories in sync with production data

---

For more information, see the main [README.md](../README.md) and [PROJECT_INDEX.md](../PROJECT_INDEX.md).

