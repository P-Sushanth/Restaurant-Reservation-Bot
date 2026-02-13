import requests
import time
import sys

BASE_URL = "http://localhost:8000"

def benchmark_menu():
    print("--- Benchmark: Menu Compression ---")
    
    # 1. Uncompressed
    start = time.time()
    r1 = requests.get(f"{BASE_URL}/menu")
    duration1 = (time.time() - start) * 1000
    size1 = len(r1.content)
    print(f"Standard Menu: {duration1:.2f}ms, Size: {size1} bytes")
    
    # 2. Compressed Stats (Simulated transfer of compressed data)
    # The endpoint returns stats, but let's emulate fetching compressed blob if we had one.
    # We'll just fetch the stats endpoint which computes compression.
    start = time.time()
    r2 = requests.get(f"{BASE_URL}/menu/compressed")
    stats = r2.json()
    duration2 = (time.time() - start) * 1000
    
    print(f"Compressed Menu (Simulated): {duration2:.2f}ms")
    print(f"  Original Size: {stats.get('original_size_bytes')} bytes")
    print(f"  Compressed Size: {stats.get('compressed_size_bytes')} bytes")
    print(f"  Ratio: {stats.get('compression_ratio')}")
    print(f"  Backend Compression Time: {stats.get('time_taken_ms')} ms")
    
    full_savings = 1 - (int(stats.get('compressed_size_bytes')) / int(stats.get('original_size_bytes')))
    print(f"  Space Savings: {full_savings:.2%}")

def benchmark_availability():
    print("\n--- Benchmark: Availability Check ---")
    # Check for today
    from datetime import date
    today = date.today().isoformat()
    
    start = time.time()
    r = requests.get(f"{BASE_URL}/availability?check_date={today}&guests=2")
    duration = (time.time() - start) * 1000
    print(f"Availability Check: {duration:.2f}ms")
    # print(r.json())

if __name__ == "__main__":
    try:
        benchmark_menu()
        benchmark_availability()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to backend. Is it running on port 8000?")
