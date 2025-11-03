"""
Pytest configuration and shared fixtures
"""

import pytest
import os
import sys
import tempfile
import sqlite3
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from db.database import OptionsDatabase
from api import create_app
from config import Config


@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    db = OptionsDatabase(db_path)
    yield db
    
    # Ensure database connection is closed before cleanup
    import sqlite3
    try:
        # Try to close any open connections
        conn = sqlite3.connect(db_path)
        conn.close()
    except:
        pass
    
    # Cleanup - add retry for Windows file locking
    import time
    for _ in range(5):
        try:
            os.unlink(db_path)
            break
        except PermissionError:
            time.sleep(0.1)
        except FileNotFoundError:
            break


@pytest.fixture
def sample_order_data():
    """Sample order data for testing"""
    return {
        'ticker': 'AAPL',
        'option_type': 'PUT',
        'action': 'SELL',
        'strike': 150.0,
        'expiration': '20241220',
        'premium': 2.50,
        'quantity': 1,
        'bid': 2.45,
        'ask': 2.55,
        'last': 2.50,
        'delta': -0.25,
        'gamma': 0.02,
        'theta': -0.15,
        'vega': 0.30,
        'implied_volatility': 0.25,
        'open_interest': 1000,
        'volume': 500,
        'is_mock': False
    }


@pytest.fixture
def sample_portfolio_data():
    """Sample portfolio data for testing"""
    return {
        'account_id': 'TEST123',
        'available_cash': 50000.0,
        'account_value': 100000.0,
        'excess_liquidity': 75000.0,
        'initial_margin': 25000.0,
        'leverage_percentage': 25.0,
        'positions': {
            'AAPL': {
                'shares': 100,
                'avg_cost': 150.0,
                'market_price': 155.0,
                'market_value': 15500.0,
                'unrealized_pnl': 500.0,
                'realized_pnl': 0.0,
                'security_type': 'STK',
                'contract': Mock(symbol='AAPL', currency='USD')
            }
        },
        'is_frozen': False
    }


@pytest.fixture
def mock_ib_connection():
    """Mock Interactive Brokers connection"""
    mock_conn = MagicMock()
    mock_conn.is_connected.return_value = True
    mock_conn.connect.return_value = True
    
    # Mock portfolio data
    mock_conn.get_portfolio.return_value = {
        'account_id': 'TEST123',
        'available_cash': 50000.0,
        'account_value': 100000.0,
        'excess_liquidity': 75000.0,
        'initial_margin': 25000.0,
        'leverage_percentage': 25.0,
        'positions': {},
        'is_frozen': False
    }
    
    # Mock stock price
    mock_conn.get_stock_price.return_value = 150.0
    
    # Mock option chain
    mock_conn.get_option_chain.return_value = {
        'symbol': 'AAPL',
        'expiration': '20241220',
        'stock_price': 150.0,
        'right': 'P',
        'options': [
            {
                'strike': 150.0,
                'expiration': '20241220',
                'option_type': 'PUT',
                'bid': 2.45,
                'ask': 2.55,
                'last': 2.50,
                'volume': 500,
                'open_interest': 1000,
                'implied_volatility': 0.25,
                'delta': -0.25,
                'gamma': 0.02,
                'theta': -0.15,
                'vega': 0.30
            }
        ]
    }
    
    return mock_conn


@pytest.fixture
def mock_config():
    """Mock configuration"""
    config = {
        'host': '127.0.0.1',
        'port': 7497,
        'client_id': 9999,
        'readonly': True,
        'account_id': 'TEST123',
        'db_path': ':memory:',
        'timeout': 20
    }
    return config


@pytest.fixture
def flask_app(mock_config, temp_db):
    """Create Flask app for testing"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['CONNECTION_CONFIG'] = mock_config
    
    # Use temporary database from fixture
    app.config['database'] = temp_db
    
    yield app


@pytest.fixture
def client(flask_app):
    """Create test client"""
    return flask_app.test_client()


@pytest.fixture
def runner(flask_app):
    """Create test CLI runner"""
    return flask_app.test_cli_runner()


class MockTicker:
    """Mock ticker object for IB API"""
    def __init__(self, price=150.0, bid=149.95, ask=150.05):
        self.bid = bid
        self.ask = ask
        self.last = price
        self.close = price
        self.marketPrice = lambda: price
        self.volume = 1000
        self.openInterest = 5000
        self.impliedVolatility = 0.25
        self.modelGreeks = Mock()
        self.modelGreeks.delta = -0.25
        self.modelGreeks.gamma = 0.02
        self.modelGreeks.theta = -0.15
        self.modelGreeks.vega = 0.30
        self.lastRTHTrade = Mock()
        self.lastRTHTrade.price = price


@pytest.fixture
def mock_ticker():
    """Mock ticker fixture"""
    return MockTicker()


@pytest.fixture
def mock_contract():
    """Mock contract object"""
    contract = Mock()
    contract.symbol = 'AAPL'
    contract.secType = 'STK'
    contract.exchange = 'SMART'
    contract.currency = 'USD'
    contract.conId = 12345
    return contract


@pytest.fixture
def mock_option_contract():
    """Mock option contract object"""
    contract = Mock()
    contract.symbol = 'AAPL'
    contract.lastTradeDateOrContractMonth = '20241220'
    contract.strike = 150.0
    contract.right = 'P'
    contract.exchange = 'SMART'
    contract.currency = 'USD'
    contract.secType = 'OPT'
    return contract

