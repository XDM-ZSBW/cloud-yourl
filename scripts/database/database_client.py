# Database Client for Yourl.Cloud
# ===============================
#
# This script provides a comprehensive database client for Yourl.Cloud
# with support for multiple database types and connection management.
#
# Author: Yourl.Cloud Inc.
# Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

import sqlite3
import mysql.connector
import psycopg2
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Union, Any
import logging
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection(ABC):
    """Abstract base class for database connections."""
    
    @abstractmethod
    def connect(self) -> bool:
        """Establish database connection."""
        pass
    
    @abstractmethod
    def disconnect(self):
        """Close database connection."""
        pass
    
    @abstractmethod
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute a query and return results."""
        pass
    
    @abstractmethod
    def execute_update(self, query: str, params: tuple = None) -> int:
        """Execute an update/insert/delete query and return affected rows."""
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """Check if connection is active."""
        pass

class SQLiteConnection(DatabaseConnection):
    """SQLite database connection implementation."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    
    def connect(self) -> bool:
        """Connect to SQLite database."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            logger.info(f"Connected to SQLite database: {self.db_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to SQLite database: {e}")
            return False
    
    def disconnect(self):
        """Close SQLite connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("SQLite connection closed")
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute a query and return results."""
        if not self.is_connected():
            if not self.connect():
                return []
        
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            results = []
            for row in self.cursor.fetchall():
                results.append(dict(row))
            return results
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return []
    
    def execute_update(self, query: str, params: tuple = None) -> int:
        """Execute an update/insert/delete query and return affected rows."""
        if not self.is_connected():
            if not self.connect():
                return 0
        
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            self.connection.commit()
            return self.cursor.rowcount
        except Exception as e:
            logger.error(f"Update execution failed: {e}")
            self.connection.rollback()
            return 0
    
    def is_connected(self) -> bool:
        """Check if SQLite connection is active."""
        return self.connection is not None and self.cursor is not None

class MySQLConnection(DatabaseConnection):
    """MySQL database connection implementation."""
    
    def __init__(self, host: str, port: int, database: str, user: str, password: str):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
    
    def connect(self) -> bool:
        """Connect to MySQL database."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor(dictionary=True)
            logger.info(f"Connected to MySQL database: {self.database} on {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MySQL database: {e}")
            return False
    
    def disconnect(self):
        """Close MySQL connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("MySQL connection closed")
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute a query and return results."""
        if not self.is_connected():
            if not self.connect():
                return []
        
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return []
    
    def execute_update(self, query: str, params: tuple = None) -> int:
        """Execute an update/insert/delete query and return affected rows."""
        if not self.is_connected():
            if not self.connect():
                return 0
        
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            self.connection.commit()
            return self.cursor.rowcount
        except Exception as e:
            logger.error(f"Update execution failed: {e}")
            self.connection.rollback()
            return 0
    
    def is_connected(self) -> bool:
        """Check if MySQL connection is active."""
        return self.connection is not None and self.cursor is not None

class PostgreSQLConnection(DatabaseConnection):
    """PostgreSQL database connection implementation."""
    
    def __init__(self, host: str, port: int, database: str, user: str, password: str):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
    
    def connect(self) -> bool:
        """Connect to PostgreSQL database."""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            logger.info(f"Connected to PostgreSQL database: {self.database} on {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL database: {e}")
            return False
    
    def disconnect(self):
        """Close PostgreSQL connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("PostgreSQL connection closed")
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute a query and return results."""
        if not self.is_connected():
            if not self.connect():
                return []
        
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            columns = [desc[0] for desc in self.cursor.description]
            results = []
            for row in self.cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return []
    
    def execute_update(self, query: str, params: tuple = None) -> int:
        """Execute an update/insert/delete query and return affected rows."""
        if not self.is_connected():
            if not self.connect():
                return 0
        
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            self.connection.commit()
            return self.cursor.rowcount
        except Exception as e:
            logger.error(f"Update execution failed: {e}")
            self.connection.rollback()
            return 0
    
    def is_connected(self) -> bool:
        """Check if PostgreSQL connection is active."""
        return self.connection is not None and self.cursor is not None

class DatabaseClient:
    """Main database client class that manages different database connections."""
    
    def __init__(self, db_type: str = "sqlite", **kwargs):
        self.db_type = db_type.lower()
        self.connection = None
        self.connection_params = kwargs
        
        # Initialize connection based on type
        if self.db_type == "sqlite":
            db_path = kwargs.get('db_path', 'yourl_cloud.db')
            self.connection = SQLiteConnection(db_path)
        elif self.db_type == "mysql":
            self.connection = MySQLConnection(
                host=kwargs.get('host', 'localhost'),
                port=kwargs.get('port', 3306),
                database=kwargs.get('database', 'yourl_cloud'),
                user=kwargs.get('user', 'root'),
                password=kwargs.get('password', '')
            )
        elif self.db_type == "postgresql":
            self.connection = PostgreSQLConnection(
                host=kwargs.get('host', 'localhost'),
                port=kwargs.get('port', 5432),
                database=kwargs.get('database', 'yourl_cloud'),
                user=kwargs.get('user', 'postgres'),
                password=kwargs.get('password', '')
            )
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
    
    def connect(self) -> bool:
        """Connect to the database."""
        if self.connection:
            return self.connection.connect()
        return False
    
    def disconnect(self):
        """Disconnect from the database."""
        if self.connection:
            self.connection.disconnect()
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute a query and return results."""
        if self.connection:
            return self.connection.execute_query(query, params)
        return []
    
    def execute_update(self, query: str, params: tuple = None) -> int:
        """Execute an update/insert/delete query and return affected rows."""
        if self.connection:
            return self.connection.execute_update(query, params)
        return 0
    
    def is_connected(self) -> bool:
        """Check if connected to database."""
        if self.connection:
            return self.connection.is_connected()
        return False
    
    def get_connection_info(self) -> Dict[str, Any]:
        """Get connection information."""
        info = {
            'type': self.db_type,
            'connected': self.is_connected(),
            'parameters': self.connection_params
        }
        
        if self.connection:
            info['connection'] = str(self.connection)
        
        return info
    
    def test_connection(self) -> Dict[str, Any]:
        """Test database connection and return status."""
        try:
            if self.connect():
                # Try a simple query
                result = self.execute_query("SELECT 1 as test")
                if result:
                    return {
                        'status': 'success',
                        'message': 'Database connection successful',
                        'test_query': result[0]
                    }
                else:
                    return {
                        'status': 'warning',
                        'message': 'Connected but test query failed'
                    }
            else:
                return {
                    'status': 'error',
                    'message': 'Failed to establish database connection'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Connection test failed: {str(e)}'
            }

def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Database Client for Yourl.Cloud')
    parser.add_argument('action', choices=['test', 'query', 'update', 'info'],
                       help='Action to perform')
    parser.add_argument('--type', '-t', default='sqlite', choices=['sqlite', 'mysql', 'postgresql'],
                       help='Database type')
    parser.add_argument('--query', '-q', help='SQL query to execute')
    parser.add_argument('--db-path', help='Database file path (for SQLite)')
    parser.add_argument('--host', help='Database host')
    parser.add_argument('--port', type=int, help='Database port')
    parser.add_argument('--database', help='Database name')
    parser.add_argument('--user', help='Database user')
    parser.add_argument('--password', help='Database password')
    
    args = parser.parse_args()
    
    # Build connection parameters
    connection_params = {}
    if args.db_path:
        connection_params['db_path'] = args.db_path
    if args.host:
        connection_params['host'] = args.host
    if args.port:
        connection_params['port'] = args.port
    if args.database:
        connection_params['database'] = args.database
    if args.user:
        connection_params['user'] = args.user
    if args.password:
        connection_params['password'] = args.password
    
    try:
        # Initialize database client
        client = DatabaseClient(args.type, **connection_params)
        
        if args.action == 'test':
            result = client.test_connection()
            print(json.dumps(result, indent=2))
            
        elif args.action == 'query':
            if not args.query:
                print("❌ Query required for query action")
                return
            results = client.execute_query(args.query)
            print(json.dumps(results, indent=2))
            
        elif args.action == 'update':
            if not args.query:
                print("❌ Query required for update action")
                return
            affected_rows = client.execute_update(args.query)
            print(json.dumps({'affected_rows': affected_rows}, indent=2))
            
        elif args.action == 'info':
            info = client.get_connection_info()
            print(json.dumps(info, indent=2))
        
        # Clean up
        client.disconnect()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
