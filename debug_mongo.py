from pymongo import MongoClient
import os
import certifi
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGODB_URL")
print(f"Testing connection to: {uri.split('@')[1] if '@' in uri else 'LOCAL/INVALID'}")

try:
    # Try connecting with strict SSL first
    client = MongoClient(uri, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("SUCCESS! Connected to MongoDB.")
except Exception as e:
    print(f"\nFAILURE (Secure): {e}")
    with open("debug_log.txt", "w") as f:
        f.write(f"SECURE FAILED: {e}\n")

    print("\nAttempting INSECURE connection (to rule out firewall)...")
    try:
        client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("SUCCESS! Connected (INSECURE mode).")
        with open("debug_log.txt", "a") as f:
            f.write("INSECURE SUCCEEDED\n")
    except Exception as e2:
        print(f"FAILURE (Insecure): {e2}")
        with open("debug_log.txt", "a") as f:
            f.write(f"INSECURE FAILED: {e2}\n")
