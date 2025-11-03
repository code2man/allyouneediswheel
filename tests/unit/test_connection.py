"""
Unit tests for core.connection module (mocked)
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, PropertyMock
from core.connection import IBConnection, suppress_ib_logs


class TestSuppressIBLogs:
    """Tests for suppress_ib_logs function"""
    
    @patch('core.connection.logging')
    def test_suppress_ib_logs_sets_levels(self, mock_logging):
        """Should set IB loggers to WARNING level"""
        suppress_ib_logs()
        
        # Check that setLevel was called for various IB loggers
        assert mock_logging.getLogger.call_count >= 5


class TestIBConnection:
    """Tests for IBConnection class"""
    
    def test_init_default_params(self):
        """Should initialize with default parameters"""
        with patch('core.connection.IB') as mock_ib:
            conn = IBConnection()
            
            assert conn.host == '127.0.0.1'
            assert conn.port == 7497
            assert conn.client_id == 1
            assert conn.timeout == 20
            assert conn.readonly is True
            assert conn._connected is False
    
    def test_init_custom_params(self):
        """Should initialize with custom parameters"""
        with patch('core.connection.IB') as mock_ib:
            conn = IBConnection(
                host='192.168.1.1',
                port=7496,
                client_id=5,
                timeout=30,
                readonly=False
            )
            
            assert conn.host == '192.168.1.1'
            assert conn.port == 7496
            assert conn.client_id == 5
            assert conn.timeout == 30
            assert conn.readonly is False
    
    @patch('core.connection.IB')
    def test_connect_success(self, mock_ib_class):
        """Should connect successfully"""
        mock_ib = MagicMock()
        mock_ib.isConnected.return_value = True
        mock_ib_class.return_value = mock_ib
        
        conn = IBConnection()
        conn.ib = mock_ib
        
        with patch.object(conn, '_ensure_event_loop'):
            result = conn.connect()
            
            assert result is True
            assert conn._connected is True
            mock_ib.connect.assert_called_once()
    
    @patch('core.connection.IB')
    def test_connect_failure(self, mock_ib_class):
        """Should handle connection failure"""
        mock_ib = MagicMock()
        mock_ib.isConnected.return_value = False
        mock_ib_class.return_value = mock_ib
        
        conn = IBConnection()
        conn.ib = mock_ib
        
        with patch.object(conn, '_ensure_event_loop'):
            result = conn.connect()
            
            assert result is False
            assert conn._connected is False
    
    @patch('core.connection.IB')
    def test_connect_already_connected(self, mock_ib_class):
        """Should return True if already connected"""
        mock_ib = MagicMock()
        mock_ib.isConnected.return_value = True
        mock_ib_class.return_value = mock_ib
        
        conn = IBConnection()
        conn.ib = mock_ib
        conn._connected = True
        
        result = conn.connect()
        
        assert result is True
        mock_ib.connect.assert_not_called()
    
    @patch('core.connection.IB')
    def test_disconnect(self, mock_ib_class):
        """Should disconnect from IB"""
        mock_ib = MagicMock()
        mock_ib_class.return_value = mock_ib
        
        conn = IBConnection()
        conn.ib = mock_ib
        conn._connected = True
        
        conn.disconnect()
        
        mock_ib.disconnect.assert_called_once()
        assert conn._connected is False
    
    @patch('core.connection.IB')
    def test_is_connected_true(self, mock_ib_class):
        """Should return True when connected"""
        mock_ib = MagicMock()
        mock_ib.isConnected.return_value = True
        mock_ib_class.return_value = mock_ib
        
        conn = IBConnection()
        conn.ib = mock_ib
        conn._connected = True
        
        assert conn.is_connected() is True
    
    @patch('core.connection.IB')
    def test_is_connected_false(self, mock_ib_class):
        """Should return False when not connected"""
        mock_ib = MagicMock()
        mock_ib.isConnected.return_value = False
        mock_ib_class.return_value = mock_ib
        
        conn = IBConnection()
        conn.ib = mock_ib
        conn._connected = False
        
        assert conn.is_connected() is False
    
    @patch('core.connection.IB')
    @patch('core.connection.is_market_hours')
    def test_set_market_data_type_live(self, mock_market_hours, mock_ib_class):
        """Should set market data type to live during market hours"""
        mock_ib = MagicMock()
        mock_ib_class.return_value = mock_ib
        
        conn = IBConnection()
        conn.ib = mock_ib
        conn._connected = True
        
        conn.set_market_data_type(1)
        
        mock_ib.reqMarketDataType.assert_called_once_with(1)
    
    @patch('core.connection.IB')
    def test_set_market_data_type_not_connected(self, mock_ib_class):
        """Should return False when not connected"""
        mock_ib = MagicMock()
        mock_ib_class.return_value = mock_ib
        
        conn = IBConnection()
        conn.ib = mock_ib
        conn._connected = False
        
        result = conn.set_market_data_type(1)
        
        assert result is False
        mock_ib.reqMarketDataType.assert_not_called()
    
    @patch('core.connection.IB')
    @patch('core.connection.is_market_hours')
    @patch('core.connection.Stock')
    @patch('core.connection.Contract')
    def test_get_stock_price_success(
        self, mock_contract, mock_stock, mock_market_hours, mock_ib_class
    ):
        """Should get stock price successfully"""
        mock_market_hours.return_value = True
        
        mock_ib = MagicMock()
        mock_ticker = MagicMock()
        mock_ticker.marketPrice.return_value = 150.0
        mock_ticker.last = 150.0
        mock_ticker.close = 149.5
        mock_ticker.bid = 149.95
        mock_ticker.ask = 150.05
        
        mock_ib.qualifyContracts.return_value = [MagicMock()]
        mock_ib.reqMktData.return_value = mock_ticker
        mock_ib.sleep = lambda x: None
        
        mock_ib_class.return_value = mock_ib
        
        conn = IBConnection()
        conn.ib = mock_ib
        conn._connected = True
        
        with patch.object(conn, '_ensure_event_loop'):
            with patch.object(conn, 'set_market_data_type'):
                price = conn.get_stock_price('AAPL')
                
                assert price == 150.0
                mock_ib.reqMktData.assert_called()
                mock_ib.cancelMktData.assert_called()
    
    @patch('core.connection.IB')
    def test_get_stock_price_not_connected(self, mock_ib_class):
        """Should return None when not connected"""
        mock_ib = MagicMock()
        mock_ib_class.return_value = mock_ib
        
        conn = IBConnection()
        conn.ib = mock_ib
        conn._connected = False
        
        with patch.object(conn, 'connect', return_value=False):
            price = conn.get_stock_price('AAPL')
            
            assert price is None
    
    @patch('core.connection.IB')
    @patch('core.connection.Option')
    def test_create_option_contract_call(self, mock_option, mock_ib_class):
        """Should create call option contract"""
        mock_ib_class.return_value = MagicMock()
        
        conn = IBConnection()
        
        contract = conn.create_option_contract('AAPL', '20241220', 150.0, 'CALL')
        
        assert contract is not None
        mock_option.assert_called_once()
    
    @patch('core.connection.IB')
    @patch('core.connection.Option')
    def test_create_option_contract_put(self, mock_option, mock_ib_class):
        """Should create put option contract"""
        mock_ib_class.return_value = MagicMock()
        
        conn = IBConnection()
        
        contract = conn.create_option_contract('AAPL', '20241220', 150.0, 'PUT')
        
        assert contract is not None
        mock_option.assert_called_once()
    
    @patch('core.connection.IB')
    def test_create_option_contract_invalid_type(self, mock_ib_class):
        """Should return None for invalid option type"""
        mock_ib_class.return_value = MagicMock()
        
        conn = IBConnection()
        
        contract = conn.create_option_contract('AAPL', '20241220', 150.0, 'INVALID')
        
        assert contract is None
    
    @patch('core.connection.IB')
    @patch('ib_async.LimitOrder')
    def test_create_order_limit(self, mock_limit_order, mock_ib_class):
        """Should create limit order"""
        mock_ib_class.return_value = MagicMock()
        
        conn = IBConnection()
        
        order = conn.create_order('SELL', 1, 'LMT', limit_price=2.50)
        
        assert order is not None
        mock_limit_order.assert_called_once()
    
    @patch('core.connection.IB')
    @patch('ib_async.MarketOrder')
    def test_create_order_market(self, mock_market_order, mock_ib_class):
        """Should create market order"""
        mock_ib_class.return_value = MagicMock()
        
        conn = IBConnection()
        
        order = conn.create_order('SELL', 1, 'MKT')
        
        assert order is not None
        mock_market_order.assert_called_once()
    
    @patch('core.connection.IB')
    def test_create_order_limit_no_price(self, mock_ib_class):
        """Should return None for limit order without price"""
        mock_ib_class.return_value = MagicMock()
        
        conn = IBConnection()
        
        order = conn.create_order('SELL', 1, 'LMT')
        
        assert order is None
    
    @patch('core.connection.IB')
    def test_create_order_invalid_type(self, mock_ib_class):
        """Should return None for unsupported order type"""
        mock_ib_class.return_value = MagicMock()
        
        conn = IBConnection()
        
        order = conn.create_order('SELL', 1, 'INVALID')
        
        assert order is None
    
    @patch('core.connection.IB')
    def test_place_order_not_connected(self, mock_ib_class):
        """Should return None when not connected"""
        mock_ib = MagicMock()
        mock_ib_class.return_value = mock_ib
        
        conn = IBConnection()
        conn.ib = mock_ib
        conn._connected = False
        
        result = conn.place_order(MagicMock(), MagicMock())
        
        assert result is None
    
    @patch('core.connection.IB')
    def test_cancel_order_not_connected(self, mock_ib_class):
        """Should return error when not connected"""
        mock_ib = MagicMock()
        mock_ib_class.return_value = mock_ib
        
        conn = IBConnection()
        conn.ib = mock_ib
        conn._connected = False
        
        result = conn.cancel_order(12345)
        
        assert result['success'] is False
        assert 'Not connected' in result['error']

