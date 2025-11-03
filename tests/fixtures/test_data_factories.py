"""
Test data factories for creating test data
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional


def create_order_data(overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create sample order data for testing
    
    Args:
        overrides: Dictionary of fields to override
        
    Returns:
        Dictionary with order data
    """
    default = {
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
        'is_mock': False,
        'isRollover': False
    }
    
    if overrides:
        default.update(overrides)
    
    return default


def create_call_order_data(overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Create sample CALL order data"""
    return create_order_data({
        'option_type': 'CALL',
        'delta': 0.25,
        **({} if overrides is None else overrides)
    })


def create_rollover_order_data(overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Create sample rollover order data"""
    return create_order_data({
        'isRollover': True,
        **({} if overrides is None else overrides)
    })


def create_portfolio_data(overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create sample portfolio data for testing
    
    Args:
        overrides: Dictionary of fields to override
        
    Returns:
        Dictionary with portfolio data
    """
    from unittest.mock import Mock
    
    default = {
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
    
    if overrides:
        default.update(overrides)
    
    return default


def create_option_chain_data(overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create sample option chain data for testing
    
    Args:
        overrides: Dictionary of fields to override
        
    Returns:
        Dictionary with option chain data
    """
    default = {
        'symbol': 'AAPL',
        'expiration': '20241220',
        'stock_price': 150.0,
        'right': 'P',
        'options': [
            {
                'strike': 145.0,
                'expiration': '20241220',
                'option_type': 'PUT',
                'bid': 1.50,
                'ask': 1.60,
                'last': 1.55,
                'volume': 1000,
                'open_interest': 5000,
                'implied_volatility': 0.25,
                'delta': -0.20,
                'gamma': 0.02,
                'theta': -0.12,
                'vega': 0.28
            },
            {
                'strike': 150.0,
                'expiration': '20241220',
                'option_type': 'PUT',
                'bid': 2.45,
                'ask': 2.55,
                'last': 2.50,
                'volume': 2000,
                'open_interest': 10000,
                'implied_volatility': 0.25,
                'delta': -0.25,
                'gamma': 0.02,
                'theta': -0.15,
                'vega': 0.30
            },
            {
                'strike': 155.0,
                'expiration': '20241220',
                'option_type': 'PUT',
                'bid': 3.50,
                'ask': 3.60,
                'last': 3.55,
                'volume': 1500,
                'open_interest': 7500,
                'implied_volatility': 0.25,
                'delta': -0.30,
                'gamma': 0.02,
                'theta': -0.18,
                'vega': 0.32
            }
        ]
    }
    
    if overrides:
        default.update(overrides)
    
    return default


def create_account_summary_data(overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create sample account summary data
    
    Args:
        overrides: Dictionary of fields to override
        
    Returns:
        Dictionary with account summary data
    """
    default = {
        'account_id': 'TEST123',
        'cash_balance': 50000.0,
        'account_value': 100000.0,
        'excess_liquidity': 75000.0,
        'initial_margin': 25000.0,
        'leverage_percentage': 25.0,
        'is_frozen': False
    }
    
    if overrides:
        default.update(overrides)
    
    return default


def get_future_friday() -> str:
    """
    Get the next Friday date in YYYYMMDD format
    
    Returns:
        Date string in YYYYMMDD format
    """
    today = datetime.now().date()
    weekday = today.weekday()
    
    if weekday < 4:  # Monday to Thursday
        days_to_add = 4 - weekday
    elif weekday == 4:  # Friday
        days_to_add = 7  # Next Friday
    else:  # Weekend
        days_to_add = 4 + (7 - weekday)
    
    next_friday = today + timedelta(days=days_to_add)
    return next_friday.strftime('%Y%m%d')


def get_future_monthly_expiration() -> str:
    """
    Get the next monthly expiration (3rd Friday) in YYYYMMDD format
    
    Returns:
        Date string in YYYYMMDD format
    """
    today = datetime.now().date()
    year = today.year
    month = today.month
    
    # Find third Friday of current month
    first_day = datetime(year, month, 1).date()
    weekday = first_day.weekday()
    
    if weekday < 4:
        days_to_first_friday = 4 - weekday
    else:
        days_to_first_friday = 4 + (7 - weekday)
    
    first_friday = first_day + timedelta(days=days_to_first_friday)
    third_friday = first_friday + timedelta(days=14)
    
    # If third Friday is in the past, move to next month
    if third_friday < today:
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
        
        first_day = datetime(year, month, 1).date()
        weekday = first_day.weekday()
        
        if weekday < 4:
            days_to_first_friday = 4 - weekday
        else:
            days_to_first_friday = 4 + (7 - weekday)
        
        first_friday = first_day + timedelta(days=days_to_first_friday)
        third_friday = first_friday + timedelta(days=14)
    
    return third_friday.strftime('%Y%m%d')

