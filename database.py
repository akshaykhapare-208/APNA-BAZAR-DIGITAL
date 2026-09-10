import os
import sys
import certifi
from bson.objectid import ObjectId
import pymongo
from config import Config

# Global database reference
_db = None
_client = None
DB_STATUS_MESSAGE = ""

def init_db():
    """
    Initializes connection to MongoDB (Atlas or Local).
    Falls back to mongomock if remote cluster is unreachable (e.g. Atlas IP whitelist restricted).
    """
    global _db, _client, DB_STATUS_MESSAGE
    if _db is not None:
        return _db

    uri = Config.MONGO_URI
    db_name = Config.DATABASE_NAME

    # Attempt to connect to MongoDB Atlas / Remote MongoDB
    if uri:
        try:
            print(f"[DB] Attempting connection to MongoDB: {uri.split('@')[-1] if '@' in uri else uri}...")
            # Use certifi CA file if available for secure SSL connection
            ca = certifi.where() if certifi else None
            _client = pymongo.MongoClient(
                uri,
                tlsCAFile=ca,
                serverSelectionTimeoutMS=4000,
                connectTimeoutMS=4000
            )
            # Force a ping command to verify credentials and connectivity
            _client.admin.command('ping')
            _db = _client[db_name]
            DB_STATUS_MESSAGE = "Connected to MongoDB Atlas successfully"
            print(f"[DB] [OK] {DB_STATUS_MESSAGE} (Database: {db_name})")
            return _db
        except Exception as e:
            print(f"[DB] ! MongoDB Connection Note: Could not connect to remote Atlas cluster directly ({e}).")
            print("[DB] ! (Tip: Ensure '0.0.0.0/0' is added in MongoDB Atlas -> Network Access tab).")

    # Fallback to mongomock for smooth local operation without crashes
    try:
        import mongomock
        print("[DB] Initializing high-fidelity local Mock MongoDB for offline/local stability...")
        _client = mongomock.MongoClient()
        _db = _client[db_name]
        DB_STATUS_MESSAGE = "Running on Local Database Engine (Fallback Active)"
        print(f"[DB] [OK] {DB_STATUS_MESSAGE}")
        return _db
    except Exception as mock_err:
        print(f"[DB] Critical: Failed to initialize fallback database: {mock_err}")
        raise mock_err

def get_db():
    """Returns the initialized database instance."""
    global _db
    if _db is None:
        return init_db()
    return _db

def to_object_id(val):
    """Safely converts string or ObjectId to ObjectId."""
    if not val:
        return None
    if isinstance(val, ObjectId):
        return val
    try:
        return ObjectId(str(val))
    except Exception:
        return None
