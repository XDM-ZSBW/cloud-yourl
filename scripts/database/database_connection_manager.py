# Database Connection Manager for Yourl.Cloud
# ===========================================
#
# This script provides connection pooling and management for database
# connections in Yourl.Cloud applications.
#
# Author: Yourl.Cloud Inc.
# Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

import threading
import time
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import queue

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConnectionPool:
    """Connection pool for managing database connections."""
    
    def __init__(self, max_connections: int = 10, connection_timeout: int = 300):
        self.max_connections = max_connections
        self.connection_timeout = connection_timeout
        self.connections = queue.Queue(maxsize=max_connections)
        self.active_connections = 0
        self.lock = threading.Lock()
        self.connection_stats = {
            'created': 0,
            'reused': 0,
            'expired': 0,
            'errors': 0
        }
    
    def get_connection(self) -> Optional[Any]:
        """Get a connection from the pool."""
        try:
            # Try to get an existing connection
            connection = self.connections.get_nowait()
            with self.lock:
                self.connection_stats['reused'] += 1
            return connection
        except queue.Empty:
            # Create new connection if pool is not full
            if self.active_connections < self.max_connections:
                try:
                    connection = self._create_connection()
                    if connection:
                        with self.lock:
                            self.active_connections += 1
                            self.connection_stats['created'] += 1
                        return connection
                except Exception as e:
                    logger.error(f"Failed to create connection: {e}")
                    with self.lock:
                        self.connection_stats['errors'] += 1
            return None
    
    def return_connection(self, connection: Any):
        """Return a connection to the pool."""
        if connection:
            try:
                self.connections.put_nowait(connection)
            except queue.Full:
                # Pool is full, close the connection
                self._close_connection(connection)
                with self.lock:
                    self.active_connections -= 1
    
    def _create_connection(self) -> Optional[Any]:
        """Create a new database connection."""
        # This is a placeholder - actual implementation would create real connections
        return {'id': f'conn_{int(time.time())}', 'created_at': datetime.now()}
    
    def _close_connection(self, connection: Any):
        """Close a database connection."""
        # This is a placeholder - actual implementation would close real connections
        logger.info(f"Closing connection: {connection.get('id', 'unknown')}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get connection pool statistics."""
        with self.lock:
            return {
                'max_connections': self.max_connections,
                'active_connections': self.active_connections,
                'available_connections': self.connections.qsize(),
                'stats': self.connection_stats.copy()
            }
    
    def cleanup_expired_connections(self):
        """Clean up expired connections."""
        # This is a placeholder - actual implementation would check connection age
        pass

class DatabaseConnectionManager:
    """Main database connection manager class."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.pools: Dict[str, ConnectionPool] = {}
        self.connection_factories: Dict[str, Any] = {}
        self.health_check_interval = config.get('health_check_interval', 60)
        self.health_check_thread = None
        self.running = False
        
        # Initialize connection pools
        self._initialize_pools()
    
    def _initialize_pools(self):
        """Initialize connection pools based on configuration."""
        for pool_name, pool_config in self.config.get('pools', {}).items():
            max_connections = pool_config.get('max_connections', 10)
            connection_timeout = pool_config.get('connection_timeout', 300)
            
            self.pools[pool_name] = ConnectionPool(max_connections, connection_timeout)
            logger.info(f"Initialized connection pool: {pool_name}")
    
    def get_connection(self, pool_name: str) -> Optional[Any]:
        """Get a connection from a specific pool."""
        if pool_name not in self.pools:
            logger.error(f"Connection pool not found: {pool_name}")
            return None
        
        return self.pools[pool_name].get_connection()
    
    def return_connection(self, pool_name: str, connection: Any):
        """Return a connection to a specific pool."""
        if pool_name in self.pools:
            self.pools[pool_name].return_connection(connection)
    
    def execute_with_connection(self, pool_name: str, operation: callable, *args, **kwargs):
        """Execute an operation with a managed connection."""
        connection = self.get_connection(pool_name)
        if not connection:
            raise Exception(f"Could not get connection from pool: {pool_name}")
        
        try:
            result = operation(connection, *args, **kwargs)
            return result
        finally:
            self.return_connection(pool_name, connection)
    
    def start_health_monitoring(self):
        """Start health monitoring for all connection pools."""
        if self.running:
            return
        
        self.running = True
        self.health_check_thread = threading.Thread(target=self._health_monitor_loop)
        self.health_check_thread.daemon = True
        self.health_check_thread.start()
        logger.info("Started database connection health monitoring")
    
    def stop_health_monitoring(self):
        """Stop health monitoring."""
        self.running = False
        if self.health_check_thread:
            self.health_check_thread.join()
        logger.info("Stopped database connection health monitoring")
    
    def _health_monitor_loop(self):
        """Health monitoring loop."""
        while self.running:
            try:
                self._check_pool_health()
                time.sleep(self.health_check_interval)
            except Exception as e:
                logger.error(f"Health monitoring error: {e}")
    
    def _check_pool_health(self):
        """Check health of all connection pools."""
        for pool_name, pool in self.pools.items():
            try:
                stats = pool.get_stats()
                logger.debug(f"Pool {pool_name} health: {stats}")
                
                # Check if pool is healthy
                if stats['active_connections'] > stats['max_connections'] * 0.9:
                    logger.warning(f"Pool {pool_name} is near capacity: {stats['active_connections']}/{stats['max_connections']}")
                
                # Clean up expired connections
                pool.cleanup_expired_connections()
                
            except Exception as e:
                logger.error(f"Health check failed for pool {pool_name}: {e}")
    
    def get_all_stats(self) -> Dict[str, Any]:
        """Get statistics for all connection pools."""
        stats = {}
        for pool_name, pool in self.pools.items():
            stats[pool_name] = pool.get_stats()
        return stats
    
    def shutdown(self):
        """Shutdown the connection manager."""
        self.stop_health_monitoring()
        
        # Close all connections in all pools
        for pool_name, pool in self.pools.items():
            try:
                while not pool.connections.empty():
                    connection = pool.connections.get_nowait()
                    pool._close_connection(connection)
                logger.info(f"Shutdown pool: {pool_name}")
            except Exception as e:
                logger.error(f"Error shutting down pool {pool_name}: {e}")
        
        logger.info("Database connection manager shutdown complete")

def main():
    """Main function for command-line usage."""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description='Database Connection Manager')
    parser.add_argument('action', choices=['start', 'stop', 'status', 'test'],
                       help='Action to perform')
    parser.add_argument('--config', '-c', help='Configuration file path')
    parser.add_argument('--pool', '-p', help='Specific pool name for status/test')
    
    args = parser.parse_args()
    
    # Load configuration
    config = {}
    if args.config:
        try:
            with open(args.config, 'r') as f:
                config = json.load(f)
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            exit(1)
    else:
        # Default configuration
        config = {
            'pools': {
                'default': {
                    'max_connections': 10,
                    'connection_timeout': 300
                }
            },
            'health_check_interval': 60
        }
    
    try:
        manager = DatabaseConnectionManager(config)
        
        if args.action == 'start':
            manager.start_health_monitoring()
            print("✅ Database connection manager started")
            
            # Keep running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n⏹️ Shutting down...")
                manager.shutdown()
                
        elif args.action == 'stop':
            manager.shutdown()
            print("✅ Database connection manager stopped")
            
        elif args.action == 'status':
            stats = manager.get_all_stats()
            if args.pool and args.pool in stats:
                print(json.dumps(stats[args.pool], indent=2))
            else:
                print(json.dumps(stats, indent=2))
                
        elif args.action == 'test':
            pool_name = args.pool or 'default'
            if pool_name not in manager.pools:
                print(f"❌ Pool not found: {pool_name}")
                exit(1)
            
            # Test connection
            connection = manager.get_connection(pool_name)
            if connection:
                print(f"✅ Successfully got connection from pool: {pool_name}")
                manager.return_connection(pool_name, connection)
            else:
                print(f"❌ Failed to get connection from pool: {pool_name}")
                exit(1)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
