import json
import os
import tempfile
import shutil
from typing import Any, Dict, List
import fcntl  # Unix-like systems
import msvcrt  # Windows

class SafeJSONStorage:
    """Thread-safe, corruption-resistant JSON storage"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.backup_filepath = f"{filepath}.backup"
        
    def _atomic_write(self, data: Any) -> bool:
        """Write data atomically to prevent corruption"""
        try:
            # Create temporary file in same directory
            temp_dir = os.path.dirname(self.filepath)
            with tempfile.NamedTemporaryFile(
                mode='w', 
                dir=temp_dir, 
                delete=False,
                encoding='utf-8',
                suffix='.tmp'
            ) as temp_file:
                # Write to temporary file
                json.dump(data, temp_file, indent=2, ensure_ascii=False)
                temp_filename = temp_file.name
            
            # Atomic move (rename) - this is atomic on most filesystems
            shutil.move(temp_filename, self.filepath)
            return True
            
        except Exception as e:
            # Clean up temp file if exists
            if 'temp_filename' in locals() and os.path.exists(temp_filename):
                try:
                    os.unlink(temp_filename)
                except:
                    pass
            print(f"❌ Error writing to {self.filepath}: {e}")
            return False
    
    def _create_backup(self) -> bool:
        """Create backup before writing"""
        try:
            if os.path.exists(self.filepath):
                shutil.copy2(self.filepath, self.backup_filepath)
            return True
        except Exception as e:
            print(f"⚠️ Failed to create backup: {e}")
            return False
    
    def _restore_from_backup(self) -> bool:
        """Restore from backup if main file is corrupted"""
        try:
            if os.path.exists(self.backup_filepath):
                shutil.copy2(self.backup_filepath, self.filepath)
                print(f"✅ Restored {self.filepath} from backup")
                return True
        except Exception as e:
            print(f"❌ Failed to restore from backup: {e}")
        return False
    
    def load(self, default: Any = None) -> Any:
        """Load data with corruption recovery"""
        for attempt in range(2):  # Try main file, then backup
            try:
                filepath = self.filepath if attempt == 0 else self.backup_filepath
                
                if not os.path.exists(filepath):
                    if attempt == 0:
                        continue  # Try backup
                    return default if default is not None else []
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # If we used backup, restore main file
                if attempt == 1:
                    self._atomic_write(data)
                    
                return data
                
            except (json.JSONDecodeError, OSError) as e:
                print(f"⚠️ Error reading {filepath}: {e}")
                if attempt == 0:
                    print("🔄 Trying backup file...")
                    continue
                else:
                    print("❌ Both main and backup files failed")
                    return default if default is not None else []
        
        return default if default is not None else []
    
    def save(self, data: Any) -> bool:
        """Save data safely with backup"""
        # Create backup first
        self._create_backup()
        
        # Write atomically
        success = self._atomic_write(data)
        
        if not success:
            print("❌ Failed to save, attempting restore from backup...")
            self._restore_from_backup()
            
        return success
    
    def validate_and_repair(self) -> bool:
        """Validate JSON and repair if possible"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                json.load(f)
            return True
        except:
            print("🔧 Attempting to repair from backup...")
            return self._restore_from_backup()


class SafeAuthStorage(SafeJSONStorage):
    """Specialized storage for authentication data"""
    
    def add_refresh_token(self, number: int, refresh_token: str) -> bool:
        """Add or update refresh token safely"""
        data = self.load([])
        
        # Find existing or add new
        existing = next((item for item in data if item.get("number") == number), None)
        if existing:
            existing["refresh_token"] = refresh_token
        else:
            data.append({"number": number, "refresh_token": refresh_token})
        
        return self.save(data)
    
    def remove_refresh_token(self, number: int) -> bool:
        """Remove refresh token safely"""
        data = self.load([])
        data = [item for item in data if item.get("number") != number]
        return self.save(data)
    
    def get_refresh_tokens(self) -> List[Dict]:
        """Get all refresh tokens"""
        return self.load([])


class SafeBookmarkStorage(SafeJSONStorage):
    """Specialized storage for bookmarks"""
    
    def add_bookmark(self, family_code: str, is_enterprise: bool, 
                    variant_name: str, option_name: str) -> bool:
        """Add bookmark safely"""
        bookmarks = self.load([])
        
        # Check if already exists
        new_bookmark = {
            "family_code": family_code,
            "is_enterprise": is_enterprise,
            "variant_name": variant_name,
            "option_name": option_name
        }
        
        # Avoid duplicates
        for bookmark in bookmarks:
            if (bookmark.get("family_code") == family_code and 
                bookmark.get("variant_name") == variant_name and
                bookmark.get("option_name") == option_name):
                return True  # Already exists
        
        bookmarks.append(new_bookmark)
        return self.save(bookmarks)
    
    def remove_bookmark(self, index: int) -> bool:
        """Remove bookmark by index"""
        bookmarks = self.load([])
        if 0 <= index < len(bookmarks):
            bookmarks.pop(index)
            return self.save(bookmarks)
        return False
    
    def get_bookmarks(self) -> List[Dict]:
        """Get all bookmarks"""
        return self.load([])