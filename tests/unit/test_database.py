"""
Unit tests for db.database module
"""

import pytest
from datetime import datetime
from db.database import OptionsDatabase


class TestOptionsDatabase:
    """Tests for OptionsDatabase class"""
    
    def test_init_with_path(self, temp_db):
        """Should initialize database with specified path"""
        assert temp_db.db_path is not None
        assert str(temp_db.db_path).endswith('.db')
    
    def test_init_creates_tables(self, temp_db):
        """Should create necessary tables on initialization"""
        # Try to query tables
        import sqlite3
        conn = sqlite3.connect(temp_db.db_path)
        cursor = conn.cursor()
        
        # Check if orders table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='orders'
        """)
        assert cursor.fetchone() is not None
        
        # Check if recommendations table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='recommendations'
        """)
        assert cursor.fetchone() is not None
        
        conn.close()
    
    def test_save_order_basic(self, temp_db, sample_order_data):
        """Should save order to database"""
        order_id = temp_db.save_order(sample_order_data)
        
        assert order_id is not None
        assert isinstance(order_id, int)
        assert order_id > 0
    
    def test_save_order_all_fields(self, temp_db, sample_order_data):
        """Should save all order fields correctly"""
        order_id = temp_db.save_order(sample_order_data)
        
        order = temp_db.get_order(order_id)
        
        assert order is not None
        assert order['ticker'] == sample_order_data['ticker']
        assert order['option_type'] == sample_order_data['option_type']
        assert order['strike'] == sample_order_data['strike']
        assert order['premium'] == sample_order_data['premium']
        assert order['quantity'] == sample_order_data['quantity']
    
    def test_save_order_with_greeks(self, temp_db, sample_order_data):
        """Should save Greeks data correctly"""
        order_id = temp_db.save_order(sample_order_data)
        
        order = temp_db.get_order(order_id)
        
        assert order['delta'] == sample_order_data['delta']
        assert order['gamma'] == sample_order_data['gamma']
        assert order['theta'] == sample_order_data['theta']
        assert order['vega'] == sample_order_data['vega']
        assert order['implied_volatility'] == sample_order_data['implied_volatility']
    
    def test_save_order_default_status(self, temp_db, sample_order_data):
        """Should set default status to 'pending'"""
        order_id = temp_db.save_order(sample_order_data)
        
        order = temp_db.get_order(order_id)
        
        assert order['status'] == 'pending'
        assert order['executed'] == 0  # False
    
    def test_get_order_by_id(self, temp_db, sample_order_data):
        """Should retrieve order by ID"""
        order_id = temp_db.save_order(sample_order_data)
        
        retrieved = temp_db.get_order(order_id)
        
        assert retrieved is not None
        assert retrieved['id'] == order_id
    
    def test_get_order_not_found(self, temp_db):
        """Should return None for non-existent order"""
        result = temp_db.get_order(99999)
        
        assert result is None
    
    def test_get_orders_all(self, temp_db, sample_order_data):
        """Should retrieve all orders"""
        # Save multiple orders
        order_ids = []
        for i in range(5):
            data = sample_order_data.copy()
            data['ticker'] = f'AAPL{i}'
            order_ids.append(temp_db.save_order(data))
        
        orders = temp_db.get_orders()
        
        assert len(orders) >= 5
        assert all(order['id'] in order_ids for order in orders[:5])
    
    def test_get_orders_filter_by_status(self, temp_db, sample_order_data):
        """Should filter orders by status"""
        # Save orders with different statuses
        order_id1 = temp_db.save_order(sample_order_data)
        temp_db.update_order_status(order_id1, 'completed', executed=True)
        
        order_id2 = temp_db.save_order(sample_order_data)
        # Keep as pending
        
        pending_orders = temp_db.get_orders(status='pending')
        completed_orders = temp_db.get_orders(status='completed')
        
        assert len(completed_orders) >= 1
        assert len(pending_orders) >= 1
        assert all(o['status'] == 'pending' for o in pending_orders)
        assert all(o['status'] == 'completed' for o in completed_orders)
    
    def test_get_orders_filter_by_status_list(self, temp_db, sample_order_data):
        """Should filter orders by multiple statuses"""
        order_id1 = temp_db.save_order(sample_order_data)
        temp_db.update_order_status(order_id1, 'completed', executed=True)
        
        order_id2 = temp_db.save_order(sample_order_data)
        temp_db.update_order_status(order_id2, 'cancelled', executed=False)
        
        order_id3 = temp_db.save_order(sample_order_data)
        # Keep as pending
        
        filtered = temp_db.get_orders(status_filter=['pending', 'cancelled'])
        
        assert len(filtered) >= 2
        assert all(o['status'] in ['pending', 'cancelled'] for o in filtered)
    
    def test_get_orders_filter_by_ticker(self, temp_db, sample_order_data):
        """Should filter orders by ticker"""
        # Save orders for different tickers
        data1 = sample_order_data.copy()
        data1['ticker'] = 'AAPL'
        temp_db.save_order(data1)
        
        data2 = sample_order_data.copy()
        data2['ticker'] = 'GOOGL'
        temp_db.save_order(data2)
        
        aapl_orders = temp_db.get_orders(ticker='AAPL')
        
        assert len(aapl_orders) >= 1
        assert all(o['ticker'] == 'AAPL' for o in aapl_orders)
    
    def test_get_orders_filter_by_executed(self, temp_db, sample_order_data):
        """Should filter orders by executed flag"""
        order_id1 = temp_db.save_order(sample_order_data)
        temp_db.update_order_status(order_id1, 'completed', executed=True)
        
        order_id2 = temp_db.save_order(sample_order_data)
        # Keep as not executed
        
        executed = temp_db.get_orders(executed=True)
        not_executed = temp_db.get_orders(executed=False)
        
        assert len(executed) >= 1
        assert len(not_executed) >= 1
        assert all(o['executed'] == 1 for o in executed)
        assert all(o['executed'] == 0 for o in not_executed)
    
    def test_get_orders_filter_by_rollover(self, temp_db, sample_order_data):
        """Should filter orders by isRollover flag"""
        data1 = sample_order_data.copy()
        data1['isRollover'] = True
        order_id1 = temp_db.save_order(data1)
        
        data2 = sample_order_data.copy()
        data2['isRollover'] = False
        order_id2 = temp_db.save_order(data2)
        
        rollover_orders = temp_db.get_orders(isRollover=True)
        non_rollover_orders = temp_db.get_orders(isRollover=False)
        
        assert len(rollover_orders) >= 1
        assert len(non_rollover_orders) >= 1
        assert all(o['isRollover'] == 1 for o in rollover_orders)
        assert all(o['isRollover'] == 0 for o in non_rollover_orders)
    
    def test_get_orders_limit(self, temp_db, sample_order_data):
        """Should limit number of returned orders"""
        # Save 10 orders
        for i in range(10):
            data = sample_order_data.copy()
            data['ticker'] = f'TICK{i}'
            temp_db.save_order(data)
        
        limited = temp_db.get_orders(limit=5)
        
        assert len(limited) == 5
    
    def test_update_order_status(self, temp_db, sample_order_data):
        """Should update order status"""
        order_id = temp_db.save_order(sample_order_data)
        
        success = temp_db.update_order_status(order_id, 'processing')
        
        assert success is True
        
        order = temp_db.get_order(order_id)
        assert order['status'] == 'processing'
    
    def test_update_order_status_with_execution_details(self, temp_db, sample_order_data):
        """Should update order with execution details"""
        order_id = temp_db.save_order(sample_order_data)
        
        execution_details = {
            'ib_order_id': '12345',
            'ib_status': 'Filled',
            'filled': 1,
            'remaining': 0,
            'avg_fill_price': 2.50
        }
        
        success = temp_db.update_order_status(
            order_id,
            'completed',
            executed=True,
            execution_details=execution_details
        )
        
        assert success is True
        
        order = temp_db.get_order(order_id)
        assert order['status'] == 'completed'
        assert order['executed'] == 1
        assert order['ib_order_id'] == '12345'
        assert order['filled'] == 1
    
    def test_update_order_status_not_found(self, temp_db):
        """Should return False for non-existent order"""
        success = temp_db.update_order_status(99999, 'completed')
        
        assert success is False
    
    def test_delete_order(self, temp_db, sample_order_data):
        """Should delete order from database"""
        order_id = temp_db.save_order(sample_order_data)
        
        success = temp_db.delete_order(order_id)
        
        assert success is True
        
        order = temp_db.get_order(order_id)
        assert order is None
    
    def test_delete_order_not_found(self, temp_db):
        """Should return False for non-existent order"""
        success = temp_db.delete_order(99999)
        
        assert success is False
    
    def test_update_order_quantity(self, temp_db, sample_order_data):
        """Should update order quantity"""
        order_id = temp_db.save_order(sample_order_data)
        
        success = temp_db.update_order_quantity(order_id, 5)
        
        assert success is True
        
        order = temp_db.get_order(order_id)
        assert order['quantity'] == 5
    
    def test_update_order_quantity_only_pending(self, temp_db, sample_order_data):
        """Should only allow updating quantity for pending orders"""
        order_id = temp_db.save_order(sample_order_data)
        temp_db.update_order_status(order_id, 'completed', executed=True)
        
        success = temp_db.update_order_quantity(order_id, 5)
        
        assert success is False
    
    def test_get_pending_orders(self, temp_db, sample_order_data):
        """Should retrieve only pending orders"""
        order_id1 = temp_db.save_order(sample_order_data)
        # Keep as pending
        
        order_id2 = temp_db.save_order(sample_order_data)
        temp_db.update_order_status(order_id2, 'completed', executed=True)
        
        pending = temp_db.get_pending_orders()
        
        assert len(pending) >= 1
        assert all(o['status'] in ['pending', 'processing'] for o in pending)
    
    def test_get_pending_orders_executed(self, temp_db, sample_order_data):
        """Should retrieve executed orders when executed=True"""
        order_id1 = temp_db.save_order(sample_order_data)
        temp_db.update_order_status(order_id1, 'completed', executed=True)
        
        order_id2 = temp_db.save_order(sample_order_data)
        # Keep as pending
        
        executed = temp_db.get_pending_orders(executed=True)
        
        assert len(executed) >= 1
        assert all(o['executed'] == 1 for o in executed)

