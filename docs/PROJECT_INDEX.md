# AllYouNeedIsWheel - Project Index

**Last Updated:** 2025-01-27  
**Status:** Indexed and documented

---

## 📋 Project Overview

**AllYouNeedIsWheel** is a financial options trading assistant specifically designed for the "Wheel Strategy" that connects to Interactive Brokers (IB). It helps traders analyze, visualize, and execute the wheel strategy effectively.

### Key Features
- Portfolio Dashboard with positions and performance metrics
- Wheel Strategy tools (cash-secured puts and covered calls)
- Options chain analysis
- Trading recommendations with premium income projections
- Option rollover management
- Interactive web interface
- Backend API for Interactive Brokers integration
- Order management (create, cancel, execute)

---

## 🏗️ Project Architecture

### Technology Stack
- **Backend:** Python 3.10+, Flask 3.0.2+
- **Frontend:** Vanilla JavaScript, HTML5, CSS3
- **Database:** SQLite
- **Trading API:** ib_async (Interactive Brokers)
- **Server:** Gunicorn (Unix/Linux/Mac), Waitress (Windows)

### Architecture Pattern
- **Modular Monolith** with separation of concerns:
  - API layer (Flask blueprints)
  - Business logic layer (Services)
  - Data layer (Database wrapper)
  - Core functionality (IB connection, utilities)

---

## 📁 Directory Structure

```
allyouneediswheel/
├── api/                          # Flask API backend
│   ├── __init__.py               # API factory and initialization
│   ├── routes/                   # API route modules
│   │   ├── __init__.py
│   │   ├── options.py            # Options-related endpoints
│   │   ├── portfolio.py         # Portfolio-related endpoints
│   │   └── recommendations.py   # Recommendation endpoints
│   └── services/                 # Business logic services
│       ├── __init__.py
│       ├── options_service.py   # Options business logic
│       └── portfolio_service.py # Portfolio business logic
│
├── core/                         # Core trading functionality
│   ├── __init__.py
│   ├── connection.py            # Interactive Brokers connection handler
│   ├── currency.py              # Currency conversion utilities
│   ├── logging_config.py        # Logging configuration
│   └── utils.py                 # Utility functions
│
├── db/                           # Database operations
│   ├── __init__.py
│   └── database.py              # SQLite database wrapper
│
├── frontend/                     # Frontend web application
│   ├── static/                   # Static assets
│   │   ├── css/                  # Stylesheets
│   │   │   ├── dashboard.css
│   │   │   ├── main.css
│   │   │   └── style.css
│   │   └── js/                   # JavaScript modules
│   │       ├── dashboard/        # Dashboard-specific JS
│   │       │   ├── account.js
│   │       │   ├── api.js
│   │       │   ├── dashboard.js
│   │       │   ├── options-table.js
│   │       │   └── orders.js
│   │       ├── portfolio/       # Portfolio-specific JS
│   │       │   └── portfolio.js
│   │       ├── rollover/         # Rollover-specific JS
│   │       │   └── rollover.js
│   │       ├── utils/            # Utility functions
│   │       │   ├── alerts.js
│   │       │   ├── formatters.js
│   │       │   └── table-utils.js
│   │       └── main.js           # Main entry point
│   └── templates/                # Jinja2 HTML templates
│       ├── base.html             # Base template
│       ├── dashboard.html        # Dashboard page
│       ├── error.html            # Error page
│       ├── portfolio.html        # Portfolio page
│       ├── rollover.html         # Rollover page
│       └── partials/             # Reusable template partials
│           ├── common/
│           ├── components/
│           └── dashboard/
│
├── app.py                        # Main Flask application entry point
├── run_api.py                    # Production API server runner (cross-platform)
├── config.py                     # Configuration handling
├── requirements.txt              # Python dependencies
├── connection.json.example       # Example IB connection config
├── LICENSE                       # Apache License 2.0
├── README.md                     # Project documentation
└── .gitignore                    # Git ignore rules
```

---

## 🔌 API Endpoints

### Portfolio Endpoints (`/api/portfolio`)
- `GET /api/portfolio/` - Get current portfolio positions and account data
- `GET /api/portfolio/positions` - Get positions (filterable by type: STK, OPT)
- `GET /api/portfolio/weekly-income` - Get weekly option income from short options expiring Friday

### Options Endpoints (`/api/options`)
- `GET /api/options/otm` - Get option data based on OTM percentage
- `GET /api/options/stock-price` - Get current stock price(s)
- `GET /api/options/orders` - Get orders with optional filters
- `POST /api/options/order` - Create a new order
- `DELETE /api/options/order/<order_id>` - Cancel an order
- `PUT /api/options/order/<order_id>` - Update an order status
- `POST /api/options/execute/<order_id>` - Execute an order through TWS
- `POST /api/options/rollover` - Create rollover orders

### Recommendations Endpoints (`/api/recommendations`)
- (Implementation details in `api/routes/recommendations.py`)

### Health Check
- `GET /health` - Health check endpoint

---

## 🗄️ Database Schema

### Tables

#### `orders` Table
Primary table for storing option orders with comprehensive fields:
- **Basic Info:** id, timestamp, ticker, option_type, action, strike, expiration, premium, quantity
- **Status:** status, executed, ib_order_id, ib_status
- **Price Data:** bid, ask, last
- **Greeks:** delta, gamma, theta, vega, implied_volatility
- **Market Data:** open_interest, volume, is_mock
- **Earnings Data:** earnings_max_contracts, earnings_premium_per_contract, earnings_total_premium, earnings_return_on_cash, earnings_return_on_capital
- **Execution Data:** filled, remaining, avg_fill_price
- **Rollover Data:** isRollover

#### `recommendations` Table
Stores option recommendations:
- id, timestamp, ticker, option_type, action, strike, expiration, premium, details

---

## 🔧 Core Components

### IBConnection (`core/connection.py`)
Manages connection to Interactive Brokers TWS/IB Gateway:
- **Connection Management:** connect(), disconnect(), is_connected()
- **Market Data:** get_stock_price(), get_option_chain(), set_market_data_type()
- **Portfolio:** get_portfolio() - retrieves positions and account info
- **Order Management:** create_option_contract(), create_order(), place_order(), check_order_status(), cancel_order()
- **Market Hours:** Automatically switches between live (1) and frozen (2) data based on market hours

### OptionsDatabase (`db/database.py`)
SQLite database wrapper for order management:
- **Order CRUD:** save_order(), get_order(), get_orders(), update_order_status(), delete_order()
- **Filtering:** Supports filtering by status, executed flag, ticker, isRollover
- **Migrations:** Automatic schema migrations for backward compatibility

### OptionsService (`api/services/options_service.py`)
Business logic for options operations:
- Option chain retrieval
- OTM options calculation
- Stock price retrieval
- Order management integration

### PortfolioService (`api/services/portfolio_service.py`)
Business logic for portfolio operations:
- Portfolio summary generation
- Position filtering and aggregation
- Weekly income calculations

---

## 🎨 Frontend Structure

### Pages
1. **Dashboard** (`/`) - Overview of portfolio and key metrics
2. **Portfolio** (`/portfolio`) - Detailed view of all positions
3. **Rollover** (`/rollover`) - Interface for managing option positions approaching strike price

### JavaScript Modules

#### Dashboard (`frontend/static/js/dashboard/`)
- `dashboard.js` - Main dashboard logic
- `account.js` - Account summary handling
- `options-table.js` - Options table display
- `orders.js` - Order management
- `api.js` - API communication helpers

#### Utilities (`frontend/static/js/utils/`)
- `formatters.js` - Data formatting utilities
- `table-utils.js` - Table manipulation helpers
- `alerts.js` - Alert/notification system

---

## 📦 Dependencies

### Core Dependencies
- `ib_async>=0.9.0` - Interactive Brokers API
- `flask>=3.0.2` - Web framework
- `pandas>=2.2.0` - Data manipulation
- `numpy>=1.26.4` - Numerical operations

### Supporting Libraries
- `jinja2>=3.1.3` - Template engine
- `flask-cors>=4.0.0` - CORS support
- `loguru>=0.7.2` - Enhanced logging
- `python-dotenv>=1.1.0` - Environment variable management
- `pytz>=2024.1` - Timezone handling
- `currencyconverter>=0.5.0` - Currency conversion

### Server Dependencies
- `gunicorn>=21.2.0` - Unix/Linux/Mac WSGI server
- `waitress>=2.1.2` - Windows-compatible WSGI server
- `werkzeug>=3.0.1` - WSGI utilities

---

## 🚀 Running the Application

### Development Mode
```bash
python app.py
```

### Production Mode (Paper Trading)
```bash
python run_api.py
```

### Production Mode (Real Money)
```bash
python run_api.py --realmoney
```

### Environment Variables
- `PORT` - Server port (default: 8000)
- `WORKERS` - Number of worker processes (default: 4)
- `CONNECTION_CONFIG` - Path to connection config file

---

## 📝 Configuration

### Connection Configuration (`connection.json`)
```json
{
    "host": "127.0.0.1",
    "port": 7497,
    "client_id": 1,
    "readonly": true,
    "account_id": "YOUR_ACCOUNT_ID",
    "db_path": "options_dev.db"
}
```

**Configuration Files:**
- `connection.json` - Paper trading (default)
- `connection_real.json` - Real money trading

---

## 🧪 Testing Status

**⚠️ CRITICAL: NO TESTS FOUND**

The project currently has **zero test files**. This violates TDD principles and requires immediate attention.

### Missing Test Coverage
- No unit tests for core modules
- No integration tests for API endpoints
- No tests for database operations
- No tests for IB connection handling
- No tests for business logic services

### Recommended Test Structure
```
tests/
├── unit/
│   ├── test_connection.py
│   ├── test_database.py
│   ├── test_options_service.py
│   └── test_portfolio_service.py
├── integration/
│   ├── test_api_options.py
│   ├── test_api_portfolio.py
│   └── test_api_recommendations.py
└── fixtures/
    └── test_data.py
```

---

## 🔒 Security Considerations

### Current Security Measures
- Connection config files in `.gitignore`
- Readonly mode default for safety
- Separate config files for paper/real trading

### Security Recommendations
- Implement input validation and sanitization
- Add rate limiting for API endpoints
- Implement authentication/authorization
- Add request logging and monitoring
- Review dependency security (use `pip-audit` or `safety`)
- Encrypt sensitive database fields

---

## 📊 Code Quality Metrics

### Current Status
- **Test Coverage:** 0% (CRITICAL)
- **Code Organization:** Good (modular structure)
- **Documentation:** Partial (README exists, inline docs vary)
- **Type Hints:** Minimal (not used consistently)

### Recommended Improvements
1. **Add comprehensive test suite** (Priority: CRITICAL)
2. **Add type hints** throughout codebase
3. **Implement code linting** (flake8, pylint, mypy)
4. **Add API documentation** (OpenAPI/Swagger)
5. **Implement CI/CD pipeline**
6. **Add error handling** standards
7. **Add logging** standards and structured logging

---

## 🔄 Version Control

### Current Status
- **Repository:** Initialized with Git
- **Branch:** main
- **Status:** Clean working tree
- **Remote:** Connected to origin

### Branch Strategy
- Single main branch detected
- **Recommendation:** Implement feature branch workflow per TDD guidelines

---

## 📚 Documentation Files

### Existing Documentation
- `README.md` - Comprehensive project documentation
- `LICENSE` - Apache License 2.0
- `.gitignore` - Git ignore patterns

### Missing Documentation
- `CONTRIBUTING.md` - Contribution guidelines
- `CHANGELOG.md` - Version history
- `SECURITY.md` - Security policy
- `API.md` - API documentation
- `ARCHITECTURE.md` - Architecture documentation
- Test documentation

---

## 🎯 Next Steps & Recommendations

### Immediate Priorities (Critical)
1. **Implement Test Suite** - Add comprehensive tests following TDD principles
2. **Add Input Validation** - Validate all API inputs
3. **Error Handling** - Standardize error handling across all modules
4. **Logging Standards** - Implement structured logging

### Short-term Improvements
1. Add type hints throughout codebase
2. Implement CI/CD pipeline
3. Add API documentation (OpenAPI/Swagger)
4. Code linting and formatting (black, isort, mypy)
5. Add unit tests for all core modules
6. Add integration tests for API endpoints

### Long-term Enhancements
1. Add authentication/authorization
2. Implement rate limiting
3. Add monitoring and alerting
4. Performance optimization
5. Add more comprehensive error recovery
6. Implement database migrations system

---

## 📞 Project Metadata

- **License:** Apache License 2.0
- **Primary Language:** Python 3.10+
- **Framework:** Flask 3.0.2+
- **Database:** SQLite
- **Frontend:** Vanilla JavaScript
- **Deployment:** Cross-platform (Windows/Unix/Linux/Mac)

---

## ✅ Index Completion Status

- [x] Project structure mapped
- [x] API endpoints documented
- [x] Database schema documented
- [x] Core components identified
- [x] Dependencies listed
- [x] Configuration documented
- [x] Security considerations noted
- [x] Testing gaps identified
- [x] Recommendations provided

---

*This index is a living document. Update it as the project evolves.*

