# Legacy JSON Files Archive

This directory contains the legacy JSON files that were used before migrating to SQLite storage.

## Files:
- `refresh-tokens.json` - Original user authentication tokens (migrated to SQLite)
- `refresh-tokens.json.backup` - Backup created during migration
- `bookmark.json` - Original bookmarks data (migrated to SQLite)  
- `bookmark.json.backup` - Backup created during migration

## Migration Date: September 15, 2025

All data has been successfully migrated to SQLite database (`me_cli.db`).
These files are kept for historical reference and emergency recovery only.

## Current System:
- ✅ Uses SQLite database for all storage
- ✅ No dependency on JSON files
- ✅ Better performance and data integrity
- ✅ ACID compliance for concurrent access

**Note: The application no longer reads from these JSON files.**