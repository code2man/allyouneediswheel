"""
Unit tests for core.currency module
"""

import pytest
from unittest.mock import Mock, patch
from core.currency import CurrencyHelper, BASE_CURRENCY


class TestCurrencyHelper:
    """Tests for CurrencyHelper class"""
    
    def test_get_exchange_rate_same_currency(self):
        """Should return 1.0 for same currency"""
        result = CurrencyHelper.get_exchange_rate('USD', 'USD')
        assert result == 1.0
    
    @patch('core.currency.CurrencyHelper.converter')
    def test_get_exchange_rate_conversion(self, mock_converter):
        """Should convert between different currencies"""
        # Mock conversion rate: 1 EUR = 1.10 USD
        mock_converter.convert.return_value = 1.10
        
        result = CurrencyHelper.get_exchange_rate('EUR', 'USD')
        
        assert result == 1.10
        mock_converter.convert.assert_called_once_with(1, 'EUR', 'USD')
    
    @patch('core.currency.CurrencyHelper.converter')
    def test_get_exchange_rate_error_handling(self, mock_converter):
        """Should return 1.0 on conversion error"""
        mock_converter.convert.side_effect = Exception("Conversion error")
        
        result = CurrencyHelper.get_exchange_rate('UNKNOWN', 'USD')
        
        assert result == 1.0
    
    def test_convert_amount_same_currency(self):
        """Should return same amount for same currency"""
        result = CurrencyHelper.convert_amount(100.0, 'USD', 'USD')
        assert result == 100.0
    
    @patch.object(CurrencyHelper, 'get_exchange_rate')
    def test_convert_amount_different_currency(self, mock_get_rate):
        """Should convert amount using exchange rate"""
        # Mock: 1 EUR = 1.10 USD
        mock_get_rate.return_value = 1.10
        
        result = CurrencyHelper.convert_amount(100.0, 'EUR', 'USD')
        
        assert result == pytest.approx(110.0)
        mock_get_rate.assert_called_once_with('EUR', 'USD')
    
    @patch.object(CurrencyHelper, 'get_exchange_rate')
    def test_convert_amount_to_base_currency_default(self, mock_get_rate):
        """Should default to BASE_CURRENCY when to_currency not specified"""
        mock_get_rate.return_value = 1.10
        
        result = CurrencyHelper.convert_amount(100.0, 'EUR')
        
        assert result == pytest.approx(110.0)
        mock_get_rate.assert_called_once_with('EUR', BASE_CURRENCY)
    
    @patch.object(CurrencyHelper, 'get_exchange_rate')
    def test_convert_amount_zero_amount(self, mock_get_rate):
        """Should handle zero amount correctly"""
        mock_get_rate.return_value = 1.10
        
        result = CurrencyHelper.convert_amount(0.0, 'EUR', 'USD')
        
        assert result == 0.0
    
    @patch.object(CurrencyHelper, 'get_exchange_rate')
    def test_convert_amount_negative_amount(self, mock_get_rate):
        """Should handle negative amounts correctly"""
        mock_get_rate.return_value = 1.10
        
        result = CurrencyHelper.convert_amount(-100.0, 'EUR', 'USD')
        
        assert result == pytest.approx(-110.0)
    
    def test_base_currency_constant(self):
        """Should have USD as base currency"""
        assert BASE_CURRENCY == 'USD'

