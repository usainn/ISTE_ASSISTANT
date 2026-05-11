import sys
import os
import time

sys.path.append(".")

print("Importing RagEngine...")
from src.rag_engine import RagEngine
print("Import successful.")

print("Initializing RagEngine...")
start = time.time()
try:
    engine = RagEngine()
    print(f"RagEngine initialized in {time.time() - start:.2f} seconds.")
except Exception as e:
    print(f"Initialization failed: {e}")

print("Testing query...")
try:
    result = engine.query("Merhaba")
    print("Query result received.")
    print(result)
except Exception as e:
    print(f"Query failed: {e}")
