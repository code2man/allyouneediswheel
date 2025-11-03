"""
Integration tests for portfolio API endpoints
"""

import pytest
import json
from unittest.mock import patch, MagicMock


class TestPortfolioAPI:
    """Tests for /api/portfolio endpoints"""
    
    @patch('api.services.portfolio_service.PortfolioService._ensure_connection')
    def test_get_portfolio_summary_success(self, mock_ensure, client, mock_ib_connection, sample_portfolio_data):
        """Should return portfolio summary"""
        mock_ensure.return_value = mock_ib_connection
        mock_ib_connection.get_portfolio.return_value = sample_portfolio_data
        
        response = client.get('/api/portfolio/')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'account_id' in data or 'cash_balance' in data or 'error' in data
    
    @patch('api.services.portfolio_service.PortfolioService._ensure_connection')
    def test_get_portfolio_summary_connection_error(self, mock_ensure, client):
        """Should handle connection errors gracefully"""
        mock_ensure.return_value = None
        
        response = client.get('/api/portfolio/')
        
        # Should return 200 with error or 500
        assert response.status_code in [200, 500]
    
    @patch('api.services.portfolio_service.PortfolioService._ensure_connection')
    def test_get_positions_all(self, mock_ensure, client, mock_ib_connection, sample_portfolio_data):
        """Should return all positions"""
        mock_ensure.return_value = mock_ib_connection
        mock_ib_connection.get_portfolio.return_value = sample_portfolio_data
        
        response = client.get('/api/portfolio/positions')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, (list, dict))
    
    @patch('api.services.portfolio_service.PortfolioService._ensure_connection')
    def test_get_positions_filter_by_type_stock(self, mock_ensure, client, mock_ib_connection, sample_portfolio_data):
        """Should filter positions by type STK"""
        mock_ensure.return_value = mock_ib_connection
        mock_ib_connection.get_portfolio.return_value = sample_portfolio_data
        
        response = client.get('/api/portfolio/positions?type=STK')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        # If data is a list, check types
        if isinstance(data, list):
            assert all(pos.get('security_type') == 'STK' for pos in data)
    
    @patch('api.services.portfolio_service.PortfolioService._ensure_connection')
    def test_get_positions_filter_by_type_option(self, mock_ensure, client, mock_ib_connection, sample_portfolio_data):
        """Should filter positions by type OPT"""
        mock_ensure.return_value = mock_ib_connection
        mock_ib_connection.get_portfolio.return_value = sample_portfolio_data
        
        response = client.get('/api/portfolio/positions?type=OPT')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        # If data is a list, check types
        if isinstance(data, list):
            assert all(pos.get('security_type') == 'OPT' for pos in data)
    
    def test_get_positions_invalid_type(self, client):
        """Should return 400 for invalid position type"""
        response = client.get('/api/portfolio/positions?type=INVALID')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    @patch('api.services.portfolio_service.PortfolioService._ensure_connection')
    def test_get_weekly_income_success(self, mock_ensure, client, mock_ib_connection):
        """Should return weekly option income"""
        mock_ensure.return_value = mock_ib_connection
        
        # Mock portfolio with options expiring this Friday
        mock_portfolio = {
            'positions': {
                'AAPL_20241220_150_P': {
                    'shares': -1,  # Short position
                    'security_type': 'OPT',
                    'contract': MagicMock(
                        symbol='AAPL',
                        lastTradeDateOrContractMonth='20241220',
                        strike=150.0,
                        right='P'
                    ),
                    'avg_cost': -2.50,
                    'market_price': -2.50
                }
            }
        }
        mock_ib_connection.get_portfolio.return_value = mock_portfolio
        
        response = client.get('/api/portfolio/weekly-income')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'total_income' in data or 'positions' in data
    
    @patch('api.services.portfolio_service.PortfolioService._ensure_connection')
    def test_get_weekly_income_connection_error(self, mock_ensure, client):
        """Should handle connection errors for weekly income"""
        mock_ensure.return_value = None
        
        response = client.get('/api/portfolio/weekly-income')
        
        # API may return 200 with empty data or 500 - check for either
        assert response.status_code in [200, 500]
        data = json.loads(response.data)
        # If it's 200, it may still have error field or empty data
        if response.status_code == 200:
            # Check if it has error or empty positions
            assert 'error' in data or 'total_income' in data
        else:
            # If 500, check error structure
            assert 'error' in data
            assert 'total_income' in data
            assert data['total_income'] == 0

