import os
import json
import time
from app.client.engsel import get_new_token
from app.util import ensure_api_key

# Import the new storage system
try:
    from app.utils.sqlite_storage import storage
    USE_SQLITE = True
    print("✅ Using SQLite storage")
except ImportError:
    USE_SQLITE = False
    print("⚠️ SQLite storage not available, using JSON fallback")

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
            if USE_SQLITE:
                self._init_sqlite()
            else:
                self._init_json()
                
            self.api_key = ensure_api_key()
            self.last_refresh_time = int(time.time())
            self._initialized_ = True
    
    def _init_sqlite(self):
        """Initialize with SQLite storage"""
        # Migrate from JSON if exists
        if os.path.exists("refresh-tokens.json") and not os.path.exists("me_cli.db"):
            print("🔄 Migrating from JSON to SQLite...")
            storage.migrate_from_json()
            
            # Backup original JSON files
            if os.path.exists("refresh-tokens.json"):
                os.rename("refresh-tokens.json", "refresh-tokens.json.backup")
            if os.path.exists("bookmark.json"):
                os.rename("bookmark.json", "bookmark.json.backup")
            
            print("✅ Migration completed! Original files backed up with .backup extension")
        
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
            # Set first user as active
            first_user = self.refresh_tokens[0]
            storage.set_active_user(first_user["number"])
            tokens = get_new_token(first_user["refresh_token"])
            if tokens:
                self.active_user = {
                    "number": int(first_user["number"]),
                    "tokens": tokens
                }
    
    def _init_json(self):
        """Initialize with JSON storage (fallback)"""
        if os.path.exists("refresh-tokens.json"):
            self.load_tokens()
        else:
            # Create empty file
            with open("refresh-tokens.json", "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)

        # Select the first user as active user by default
        if self.refresh_tokens and len(self.refresh_tokens) != 0:
            first_rt = self.refresh_tokens[0]
            tokens = get_new_token(first_rt["refresh_token"])
            if tokens:
                self.active_user = {
                    "number": int(first_rt["number"]),
                    "tokens": tokens
                }
    
    def load_tokens(self):
        """Load tokens from JSON file (legacy method)"""
        if not USE_SQLITE:
            try:
                with open("refresh-tokens.json", "r", encoding="utf-8") as f:
                    self.refresh_tokens = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                print("⚠️ Error loading tokens, creating new file")
                self.refresh_tokens = []
                self._save_tokens_json()
    
    def _save_tokens_json(self):
        """Save tokens to JSON (legacy method)"""
        with open("refresh-tokens.json", "w", encoding="utf-8") as f:
            json.dump(self.refresh_tokens, f, indent=2)

    def add_refresh_token(self, number: int, refresh_token: str):
        """Add refresh token using appropriate storage"""
        if USE_SQLITE:
            success = storage.add_user(number, refresh_token)
            if success:
                # Reload data
                self.refresh_tokens = storage.get_all_users()
                self.set_active_user(number)
            return success
        else:
            # Legacy JSON method
            existing = next((rt for rt in self.refresh_tokens if rt["number"] == number), None)
            if existing:
                existing["refresh_token"] = refresh_token
            else:
                self.refresh_tokens.append({
                    "number": int(number),
                    "refresh_token": refresh_token
                })
            
            self._save_tokens_json()
            self.set_active_user(number)
            
    def remove_refresh_token(self, number: int):
        """Remove refresh token using appropriate storage"""
        if USE_SQLITE:
            success = storage.remove_user(number)
            if success:
                self.refresh_tokens = storage.get_all_users()
                
                # If removed user was active, select new active user
                if self.active_user and self.active_user["number"] == number:
                    if self.refresh_tokens:
                        self.set_active_user(self.refresh_tokens[0]["number"])
                    else:
                        self.active_user = None
            return success
        else:
            # Legacy JSON method
            self.refresh_tokens = [rt for rt in self.refresh_tokens if rt["number"] != number]
            self._save_tokens_json()
            
            if self.active_user and self.active_user["number"] == number:
                if len(self.refresh_tokens) != 0:
                    first_rt = self.refresh_tokens[0]
                    tokens = get_new_token(first_rt["refresh_token"])
                    if tokens:
                        self.active_user = {
                            "number": int(first_rt["number"]),
                            "tokens": tokens
                        }
                else:
                    self.active_user = None

    def set_active_user(self, number: int):
        """Set active user using appropriate storage"""
        if USE_SQLITE:
            success = storage.set_active_user(number)
            if success:
                # Update local active_user
                user_data = next((u for u in self.refresh_tokens if u["number"] == number), None)
                if user_data:
                    tokens = get_new_token(user_data["refresh_token"])
                    if tokens:
                        self.active_user = {
                            "number": int(number),
                            "tokens": tokens
                        }
            return success
        else:
            # Legacy method
            user_rt = next((rt for rt in self.refresh_tokens if rt["number"] == number), None)
            if user_rt:
                tokens = get_new_token(user_rt["refresh_token"])
                if tokens:
                    self.active_user = {
                        "number": int(number),
                        "tokens": tokens
                    }
                    return True
            return False

    def get_active_user(self):
        """Get active user"""
        return self.active_user

    def get_active_tokens(self):
        """Get active user tokens"""
        return self.active_user["tokens"] if self.active_user else None

    def get_all_users(self):
        """Get all users"""
        if USE_SQLITE:
            return storage.get_all_users()
        else:
            return self.refresh_tokens

# Create singleton instance
AuthInstance = Auth()