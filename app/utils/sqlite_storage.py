import sqlite3
import json
import os
import threading
from typing import List, Dict, Optional, Any
from contextlib import contextmanager

class SQLiteStorage:
    """Thread-safe SQLite storage for me-cli data"""
    
    def __init__(self, db_path: str = "me_cli.db"):
        self.db_path = db_path
        self._lock = threading.Lock()
        self._init_database()
    
    def _init_database(self):
        """Initialize database tables"""
        with self._get_connection() as conn:
            # Users/Auth table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    number INTEGER UNIQUE NOT NULL,
                    refresh_token TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 0
                )
            """)
            
            # Bookmarks table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS bookmarks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    family_code TEXT NOT NULL,
                    is_enterprise BOOLEAN NOT NULL,
                    variant_name TEXT NOT NULL,
                    option_name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(family_code, variant_name, option_name)
                )
            """)
            
            # Settings table for misc data
            conn.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_users_number ON users(number)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_bookmarks_family ON bookmarks(family_code)")
            
            conn.commit()
    
    @contextmanager
    def _get_connection(self):
        """Get database connection with proper locking"""
        with self._lock:
            conn = sqlite3.connect(
                self.db_path, 
                timeout=30.0,  # 30 second timeout
                check_same_thread=False
            )
            conn.row_factory = sqlite3.Row  # Enable dict-like access
            try:
                yield conn
            finally:
                conn.close()
    
    # === USER/AUTH MANAGEMENT ===
    
    def add_user(self, number: int, refresh_token: str) -> bool:
        """Add or update user safely"""
        try:
            with self._get_connection() as conn:
                # First, deactivate all users
                conn.execute("UPDATE users SET is_active = 0")
                
                # Insert or update user
                conn.execute("""
                    INSERT OR REPLACE INTO users (number, refresh_token, updated_at, is_active)
                    VALUES (?, ?, CURRENT_TIMESTAMP, 1)
                """, (number, refresh_token))
                
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"❌ Database error adding user: {e}")
            return False
    
    def remove_user(self, number: int) -> bool:
        """Remove user safely"""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute("DELETE FROM users WHERE number = ?", (number,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"❌ Database error removing user: {e}")
            return False
    
    def get_all_users(self) -> List[Dict]:
        """Get all users"""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute("""
                    SELECT number, refresh_token, created_at, updated_at, is_active
                    FROM users ORDER BY updated_at DESC
                """)
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"❌ Database error getting users: {e}")
            return []
    
    def get_active_user(self) -> Optional[Dict]:
        """Get currently active user"""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute("""
                    SELECT number, refresh_token, created_at, updated_at
                    FROM users WHERE is_active = 1 LIMIT 1
                """)
                row = cursor.fetchone()
                return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"❌ Database error getting active user: {e}")
            return None
    
    def set_active_user(self, number: int) -> bool:
        """Set user as active"""
        try:
            with self._get_connection() as conn:
                # Deactivate all
                conn.execute("UPDATE users SET is_active = 0")
                # Activate specific user
                cursor = conn.execute(
                    "UPDATE users SET is_active = 1, updated_at = CURRENT_TIMESTAMP WHERE number = ?", 
                    (number,)
                )
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"❌ Database error setting active user: {e}")
            return False
    
    # === BOOKMARK MANAGEMENT ===
    
    def add_bookmark(self, family_code: str, is_enterprise: bool, 
                    variant_name: str, option_name: str) -> bool:
        """Add bookmark safely"""
        try:
            with self._get_connection() as conn:
                conn.execute("""
                    INSERT OR IGNORE INTO bookmarks 
                    (family_code, is_enterprise, variant_name, option_name)
                    VALUES (?, ?, ?, ?)
                """, (family_code, is_enterprise, variant_name, option_name))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"❌ Database error adding bookmark: {e}")
            return False
    
    def remove_bookmark(self, bookmark_id: int) -> bool:
        """Remove bookmark by ID"""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute("DELETE FROM bookmarks WHERE id = ?", (bookmark_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"❌ Database error removing bookmark: {e}")
            return False
    
    def remove_bookmark_by_details(self, family_code: str, is_enterprise: bool, 
                                 variant_name: str, option_name: str) -> bool:
        """Remove bookmark by details"""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute("""
                    DELETE FROM bookmarks 
                    WHERE family_code = ? AND is_enterprise = ? 
                    AND variant_name = ? AND option_name = ?
                """, (family_code, is_enterprise, variant_name, option_name))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"❌ Database error removing bookmark: {e}")
            return False
    
    def get_bookmarks(self) -> List[Dict]:
        """Get all bookmarks"""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute("""
                    SELECT id, family_code, is_enterprise, variant_name, option_name, created_at
                    FROM bookmarks ORDER BY created_at DESC
                """)
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"❌ Database error getting bookmarks: {e}")
            return []
    
    # === SETTINGS MANAGEMENT ===
    
    def set_setting(self, key: str, value: Any) -> bool:
        """Set application setting"""
        try:
            with self._get_connection() as conn:
                # Convert value to JSON string if not string
                value_str = value if isinstance(value, str) else json.dumps(value)
                
                conn.execute("""
                    INSERT OR REPLACE INTO settings (key, value, updated_at)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                """, (key, value_str))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"❌ Database error setting {key}: {e}")
            return False
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get application setting"""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute("SELECT value FROM settings WHERE key = ?", (key,))
                row = cursor.fetchone()
                
                if row:
                    value_str = row['value']
                    # Try to parse as JSON, fallback to string
                    try:
                        return json.loads(value_str)
                    except json.JSONDecodeError:
                        return value_str
                return default
        except sqlite3.Error as e:
            print(f"❌ Database error getting {key}: {e}")
            return default
    
    # === MIGRATION FROM JSON ===
    
    def migrate_from_json(self, auth_json_path: str = "refresh-tokens.json", 
                         bookmark_json_path: str = "bookmark.json") -> bool:
        """Migrate existing JSON data to SQLite"""
        print("🔄 Migrating data from JSON to SQLite...")
        
        try:
            # Migrate users
            if os.path.exists(auth_json_path):
                with open(auth_json_path, 'r', encoding='utf-8') as f:
                    users_data = json.load(f)
                
                for user in users_data:
                    self.add_user(user['number'], user['refresh_token'])
                print(f"✅ Migrated {len(users_data)} users")
            
            # Migrate bookmarks
            if os.path.exists(bookmark_json_path):
                with open(bookmark_json_path, 'r', encoding='utf-8') as f:
                    bookmarks_data = json.load(f)
                
                for bookmark in bookmarks_data:
                    self.add_bookmark(
                        bookmark['family_code'],
                        bookmark['is_enterprise'],
                        bookmark['variant_name'],
                        bookmark['option_name']
                    )
                print(f"✅ Migrated {len(bookmarks_data)} bookmarks")
            
            return True
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            return False
    
    def backup_to_json(self, backup_dir: str = "backup") -> bool:
        """Backup SQLite data to JSON files"""
        try:
            os.makedirs(backup_dir, exist_ok=True)
            
            # Backup users
            users = self.get_all_users()
            with open(f"{backup_dir}/users_backup.json", 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=2, default=str)
            
            # Backup bookmarks
            bookmarks = self.get_bookmarks()
            with open(f"{backup_dir}/bookmarks_backup.json", 'w', encoding='utf-8') as f:
                json.dump(bookmarks, f, indent=2, default=str)
            
            print(f"✅ Backup created in {backup_dir}/")
            return True
            
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False


# Global instance
storage = SQLiteStorage()