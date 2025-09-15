import os
from typing import List, Dict
from app.utils.sqlite_storage import storage

print("🔖 Using SQLite storage for bookmarks")

class Bookmark:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.packages: List[Dict] = []
            self.load_bookmark()
            self._initialized = True

    def load_bookmark(self):
        """Load bookmarks from SQLite storage."""
        self.packages = storage.get_bookmarks()

    def save_bookmark(self):
        """Save current bookmarks to SQLite storage."""
        # Note: Individual bookmarks are already saved via add_bookmark/remove_bookmark
        # This method exists for compatibility but doesn't need to do anything
        pass

    def add_bookmark(
        self,
        family_code: str,
        is_enterprise: bool,
        variant_name: str,
        option_name: str,
    ) -> bool:
        """Add a bookmark if it does not already exist."""
        # Check if bookmark already exists in SQLite
        existing_bookmarks = storage.get_bookmarks()
        key = (family_code, variant_name, option_name)

        if any(
            (p["family_code"], p["variant_name"], p["option_name"]) == key
            for p in existing_bookmarks
        ):
            print("Bookmark already exists.")
            return False

        # Add to SQLite storage
        success = storage.add_bookmark(family_code, is_enterprise, variant_name, option_name)
        if success:
            # Refresh local cache
            self.packages = storage.get_bookmarks()
            print("Bookmark added.")
            return True
        else:
            print("Failed to add bookmark.")
            return False

    def remove_bookmark(
        self,
        family_code: str,
        is_enterprise: bool,
        variant_name: str,
        option_name: str,
    ) -> bool:
        """Remove a bookmark if it exists. Returns True if removed."""
        success = storage.remove_bookmark_by_details(family_code, is_enterprise, variant_name, option_name)
        if success:
            # Refresh local cache
            self.packages = storage.get_bookmarks()
            print("Bookmark removed.")
            return True
        else:
            print("Bookmark not found.")
            return False

    def get_bookmarks(self) -> List[Dict]:
        """Return all bookmarks."""
        return self.packages.copy()

BookmarkInstance = Bookmark()