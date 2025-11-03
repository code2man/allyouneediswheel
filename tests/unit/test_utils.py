"""
Unit tests for core.utils module
"""

import pytest
from datetime import datetime, timedelta, time as datetime_time
import pytz
from unittest.mock import patch, mock_open
import os
import tempfile
import shutil

from core.utils import (
    rotate_logs,
    rotate_reports,
    setup_logging,
    get_closest_friday,
    get_next_monthly_expiration,
    parse_date_string,
    format_date_string,
    format_currency,
    format_percentage,
    get_strikes_around_price,
    is_market_hours
)


class TestRotateLogs:
    """Tests for rotate_logs function"""
    
    def test_rotate_logs_no_cleanup_needed(self, tmp_path):
        """Should not delete logs when under max limit"""
        logs_dir = tmp_path / 'logs'
        logs_dir.mkdir()
        
        # Create only 3 log files (under max of 5)
        for i in range(3):
            (logs_dir / f'trader_{i}.log').write_text('test')
        
        rotate_logs(str(logs_dir), max_logs=5)
        
        # All files should still exist
        assert len(list(logs_dir.glob('trader_*.log'))) == 3
    
    def test_rotate_logs_cleanup_old_logs(self, tmp_path):
        """Should delete old logs when over max limit"""
        logs_dir = tmp_path / 'logs'
        logs_dir.mkdir()
        
        # Create 7 log files
        log_files = []
        for i in range(7):
            log_file = logs_dir / f'trader_{i}.log'
            log_file.write_text('test')
            log_files.append(log_file)
            # Touch files with different modification times
            import time
            time.sleep(0.01)  # Small delay to ensure different mtimes
        
        rotate_logs(str(logs_dir), max_logs=5)
        
        # Should keep only 5 newest files
        remaining = list(logs_dir.glob('trader_*.log'))
        assert len(remaining) == 5


class TestRotateReports:
    """Tests for rotate_reports function"""
    
    def test_rotate_reports_no_cleanup_needed(self, tmp_path):
        """Should not delete reports when under max limit"""
        reports_dir = tmp_path / 'reports'
        reports_dir.mkdir()
        
        # Create only 3 report files
        for i in range(3):
            (reports_dir / f'options_report_{i}.html').write_text('test')
        
        rotate_reports(str(reports_dir), max_reports=5)
        
        assert len(list(reports_dir.glob('options_report_*.html'))) == 3
    
    def test_rotate_reports_cleanup_old_reports(self, tmp_path):
        """Should delete old reports when over max limit"""
        reports_dir = tmp_path / 'reports'
        reports_dir.mkdir()
        
        # Create 7 report files
        for i in range(7):
            report_file = reports_dir / f'options_report_{i}.html'
            report_file.write_text('test')
            import time
            time.sleep(0.01)
        
        rotate_reports(str(reports_dir), max_reports=5)
        
        remaining = list(reports_dir.glob('options_report_*.html'))
        assert len(remaining) == 5


class TestGetClosestFriday:
    """Tests for get_closest_friday function"""
    
    @patch('core.utils.datetime')
    def test_get_closest_friday_on_monday(self, mock_datetime):
        """Should return Friday of current week when called on Monday"""
        # Mock Monday, Jan 1, 2024
        mock_now = datetime(2024, 1, 1)  # Monday
        mock_datetime.now.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        
        result = get_closest_friday()
        
        # Should be Friday, Jan 5, 2024
        assert result.weekday() == 4  # Friday
        assert result.day == 5
        assert result.month == 1
    
    @patch('core.utils.datetime')
    def test_get_closest_friday_on_friday(self, mock_datetime):
        """Should return current Friday when called on Friday"""
        # Mock Friday, Jan 5, 2024
        mock_now = datetime(2024, 1, 5)  # Friday
        mock_datetime.now.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        
        result = get_closest_friday()
        
        assert result.weekday() == 4  # Friday
        assert result == mock_now.date()
    
    @patch('core.utils.datetime')
    def test_get_closest_friday_on_weekend(self, mock_datetime):
        """Should return next Friday when called on weekend"""
        # Mock Saturday, Jan 6, 2024
        mock_now = datetime(2024, 1, 6)  # Saturday
        mock_datetime.now.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        
        result = get_closest_friday()
        
        # Should be next Friday, Jan 12, 2024
        assert result.weekday() == 4  # Friday
        assert result.day == 12


class TestGetNextMonthlyExpiration:
    """Tests for get_next_monthly_expiration function"""
    
    @patch('core.utils.datetime')
    def test_get_next_monthly_expiration_before_third_friday(self, mock_datetime):
        """Should return third Friday of current month if not yet passed"""
        # Mock Monday, Jan 1, 2024
        mock_now = datetime(2024, 1, 1)
        mock_datetime.now.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        
        result = get_next_monthly_expiration()
        
        # Third Friday of January 2024 is Jan 19
        assert result == '20240119'
    
    @patch('core.utils.datetime')
    def test_get_next_monthly_expiration_after_third_friday(self, mock_datetime):
        """Should return third Friday of next month if current month's passed"""
        # Mock Monday, Jan 22, 2024 (after third Friday)
        mock_now = datetime(2024, 1, 22)
        mock_datetime.now.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        
        result = get_next_monthly_expiration()
        
        # Third Friday of February 2024 is Feb 16
        assert result == '20240216'


class TestDateParsing:
    """Tests for date parsing and formatting functions"""
    
    def test_parse_date_string(self):
        """Should parse YYYYMMDD format correctly"""
        result = parse_date_string('20241220')
        assert result.year == 2024
        assert result.month == 12
        assert result.day == 20
    
    def test_format_date_string(self):
        """Should format datetime as YYYYMMDD"""
        date_obj = datetime(2024, 12, 20)
        result = format_date_string(date_obj)
        assert result == '20241220'
    
    def test_parse_and_format_roundtrip(self):
        """Should maintain data integrity through parse/format cycle"""
        original = '20241220'
        parsed = parse_date_string(original)
        formatted = format_date_string(parsed)
        assert formatted == original


class TestFormatting:
    """Tests for formatting functions"""
    
    def test_format_currency_positive(self):
        """Should format positive currency correctly"""
        assert format_currency(123.45) == '$123.45'
        assert format_currency(0.01) == '$0.01'
        assert format_currency(1000.0) == '$1000.00'
    
    def test_format_currency_negative(self):
        """Should format negative currency correctly"""
        assert format_currency(-123.45) == '$-123.45'
    
    def test_format_currency_none(self):
        """Should handle None values"""
        assert format_currency(None) == '$0.00'
    
    def test_format_currency_nan(self):
        """Should handle NaN values"""
        import math
        assert format_currency(float('nan')) == '$0.00'
    
    def test_format_percentage_positive(self):
        """Should format positive percentage correctly"""
        assert format_percentage(12.34) == '12.34%'
        assert format_percentage(0.01) == '0.01%'
        assert format_percentage(100.0) == '100.00%'
    
    def test_format_percentage_negative(self):
        """Should format negative percentage correctly"""
        assert format_percentage(-12.34) == '-12.34%'
    
    def test_format_percentage_none(self):
        """Should handle None values"""
        assert format_percentage(None) == '0.00%'
    
    def test_format_percentage_nan(self):
        """Should handle NaN values"""
        import math
        assert format_percentage(float('nan')) == '0.00%'


class TestGetStrikesAroundPrice:
    """Tests for get_strikes_around_price function"""
    
    def test_get_strikes_around_price_default(self):
        """Should generate strikes around price correctly"""
        price = 100.0
        interval = 5.0
        num_strikes = 5
        
        result = get_strikes_around_price(price, interval, num_strikes)
        
        # Should generate strikes: 95, 100, 105, 110, 115 (or similar)
        assert len(result) == num_strikes
        assert 100.0 in result  # Should include price level
    
    def test_get_strikes_around_price_symmetric(self):
        """Should generate symmetric strikes around price"""
        price = 150.0
        interval = 10.0
        num_strikes = 5
        
        result = get_strikes_around_price(price, interval, num_strikes)
        
        # Should be symmetric around nearest strike below price
        assert len(result) == num_strikes
        assert result == sorted(result)  # Should be sorted
    
    def test_get_strikes_around_price_odd_number(self):
        """Should handle odd number of strikes"""
        price = 200.0
        interval = 25.0
        num_strikes = 7
        
        result = get_strikes_around_price(price, interval, num_strikes)
        
        assert len(result) == num_strikes


class TestIsMarketHours:
    """Tests for is_market_hours function"""
    
    @patch('core.utils.datetime')
    def test_is_market_hours_regular_hours(self, mock_datetime):
        """Should return True during regular market hours (9:30 AM - 4:00 PM ET)"""
        # Mock Wednesday, Jan 10, 2024, 12:00 PM ET
        eastern = pytz.timezone('US/Eastern')
        mock_now = eastern.localize(datetime(2024, 1, 10, 12, 0, 0))
        mock_datetime.now.return_value = mock_now
        
        result = is_market_hours()
        
        assert result is True
    
    @patch('core.utils.datetime')
    def test_is_market_hours_before_open(self, mock_datetime):
        """Should return False before market open"""
        # Mock Wednesday, Jan 10, 2024, 8:00 AM ET
        eastern = pytz.timezone('US/Eastern')
        mock_now = eastern.localize(datetime(2024, 1, 10, 8, 0, 0))
        mock_datetime.now.return_value = mock_now
        
        result = is_market_hours()
        
        assert result is False
    
    @patch('core.utils.datetime')
    def test_is_market_hours_after_close(self, mock_datetime):
        """Should return False after market close"""
        # Mock Wednesday, Jan 10, 2024, 5:00 PM ET
        eastern = pytz.timezone('US/Eastern')
        mock_now = eastern.localize(datetime(2024, 1, 10, 17, 0, 0))
        mock_datetime.now.return_value = mock_now
        
        result = is_market_hours()
        
        assert result is False
    
    @patch('core.utils.datetime')
    def test_is_market_hours_weekend(self, mock_datetime):
        """Should return False on weekends"""
        # Mock Saturday, Jan 13, 2024, 12:00 PM ET
        eastern = pytz.timezone('US/Eastern')
        mock_now = eastern.localize(datetime(2024, 1, 13, 12, 0, 0))
        mock_datetime.now.return_value = mock_now
        
        result = is_market_hours()
        
        assert result is False
    
    @patch('core.utils.datetime')
    def test_is_market_hours_with_extended_hours(self, mock_datetime):
        """Should return True during extended hours if include_after_hours=True"""
        # Mock Wednesday, Jan 10, 2024, 7:00 AM ET (pre-market)
        eastern = pytz.timezone('US/Eastern')
        mock_now = eastern.localize(datetime(2024, 1, 10, 7, 0, 0))
        mock_datetime.now.return_value = mock_now
        
        result = is_market_hours(include_after_hours=True)
        
        assert result is True
    
    @patch('core.utils.datetime')
    def test_is_market_hours_extended_after_hours(self, mock_datetime):
        """Should return True during after-hours if include_after_hours=True"""
        # Mock Wednesday, Jan 10, 2024, 6:00 PM ET (after-hours)
        eastern = pytz.timezone('US/Eastern')
        mock_now = eastern.localize(datetime(2024, 1, 10, 18, 0, 0))
        mock_datetime.now.return_value = mock_now
        
        result = is_market_hours(include_after_hours=True)
        
        assert result is True

