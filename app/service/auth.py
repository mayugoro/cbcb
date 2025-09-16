import os
import time
from app.client.engsel import get_new_token
from app.util import ensure_api_key
from app.utils.sqlite_storage import storage

class Auth:
    _instance_ = None
    _initialized_ = False
    
    api_key = ""
    
    refresh_tokens = []
    # Format of refresh_tokens: [{"number": int, "refresh_token": str}]
    
    active_user = None
    # Format of active_user: {"number": int, "tokens": {"refresh_token": str, "access_token": str, "id_token": str}}
    
    last_refresh_time = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance_:
            cls._instance_ = super().__new__(cls)
        return cls._instance_
    
    def __init__(self):
        if not self._initialized_:
            self._init_sqlite()
            self.api_key = ensure_api_key()
            self.last_refresh_time = int(time.time())
            self._initialized_ = True
    
    def _init_sqlite(self):
        """Initialize with pure SQLite storage"""
        print("🗄️ Loading data from SQLite database...")
        
        # Load data from SQLite
        self.refresh_tokens = storage.get_all_users()
        
        # Set active user
        active_user_data = storage.get_active_user()
        if active_user_data:
            tokens = get_new_token(active_user_data["refresh_token"])
            if tokens:
                self.active_user = {
                    "number": int(active_user_data["number"]),
                    "tokens": tokens
                }
        elif self.refresh_tokens:
            # Set first user as active if no active user set
            first_user = self.refresh_tokens[0]
            storage.set_active_user(first_user["number"])
            tokens = get_new_token(first_user["refresh_token"])
            if tokens:
                self.active_user = {
                    "number": int(first_user["number"]),
                    "tokens": tokens
                }
        
        print(f"✅ Loaded {len(self.refresh_tokens)} users from SQLite database")

    def add_user(self, number, refresh_token):
        """Add a new user to SQLite storage"""
        # Add to storage
        success = storage.add_user(number, refresh_token)
        if success:
            # Refresh local data
            self.refresh_tokens = storage.get_all_users()
            return True
        return False

    def add_refresh_token(self, number: int, refresh_token: str):
        """Add refresh token for user (compatibility method)"""
        return self.add_user(number, refresh_token)

    def remove_user(self, number):
        """Remove user from SQLite storage"""
        success = storage.remove_user(number)
        if success:
            # Refresh local data
            self.refresh_tokens = storage.get_all_users()
            
            # Clear active user if it was the removed user
            if self.active_user and self.active_user["number"] == number:
                self.active_user = None
                
                # Set new active user if available
                if self.refresh_tokens:
                    first_user = self.refresh_tokens[0]
                    storage.set_active_user(first_user["number"])
                    tokens = get_new_token(first_user["refresh_token"])
                    if tokens:
                        self.active_user = {
                            "number": int(first_user["number"]),
                            "tokens": tokens
                        }
            return True
        return False

    def set_active_user(self, number):
        """Set active user in SQLite storage"""
        success = storage.set_active_user(number)
        if success:
            # Find user data
            for user in self.refresh_tokens:
                if user["number"] == number:
                    tokens = get_new_token(user["refresh_token"])
                    if tokens:
                        self.active_user = {
                            "number": int(number),
                            "tokens": tokens
                        }
                        return True
        return False

    def get_all_users(self):
        """Get all users from SQLite storage"""
        return storage.get_all_users()

    def get_active_user(self):
        """Get active user"""
        return self.active_user

    def get_user_by_number(self, number):
        """Get specific user by number"""
        return storage.get_user_by_number(number)

    def update_refresh_token(self, number, new_refresh_token):
        """Update refresh token for user"""
        success = storage.add_user(number, new_refresh_token)  # add_user does upsert
        if success:
            self.refresh_tokens = storage.get_all_users()
            
            # Update active user if it's the same number
            if self.active_user and self.active_user["number"] == number:
                tokens = get_new_token(new_refresh_token)
                if tokens:
                    self.active_user["tokens"] = tokens
            return True
        return False

    def refresh_access_token(self):
        """Refresh access token for active user"""
        if not self.active_user:
            return False
            
        user_data = storage.get_user_by_number(self.active_user["number"])
        if user_data:
            tokens = get_new_token(user_data["refresh_token"])
            if tokens:
                self.active_user["tokens"] = tokens
                self.last_refresh_time = int(time.time())
                return True
        return False

    def is_token_expired(self):
        """Check if token needs refresh (every 30 minutes)"""
        if not self.last_refresh_time:
            return True
        return (int(time.time()) - self.last_refresh_time) > 1800  # 30 minutes

    def auto_refresh_if_needed(self):
        """Auto refresh token if needed"""
        if self.is_token_expired():
            return self.refresh_access_token()
        return True

    def get_active_tokens(self):
        """Get active user tokens for API calls"""
        return self.active_user["tokens"] if self.active_user else None

    def load_tokens(self):
        """Load tokens from SQLite storage (compatibility method)"""
        # Refresh data from SQLite
        self.refresh_tokens = storage.get_all_users()
        
        # Refresh active user
        active_user_data = storage.get_active_user()
        if active_user_data:
            tokens = get_new_token(active_user_data["refresh_token"])
            if tokens:
                self.active_user = {
                    "number": int(active_user_data["number"]),
                    "tokens": tokens
                }
                self.last_refresh_time = int(time.time())

# Global instance
AuthInstance = Auth()