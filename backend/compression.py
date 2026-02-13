import zlib
import json
import time
import sys

def compress_menu_data(menu_items: list[dict]):
    """
    Compresses a list of menu dictionaries using zlib.
    Returns the compressed bytes and performance stats.
    """
    start_time = time.time()
    json_data = json.dumps(menu_items).encode('utf-8')
    original_size = sys.getsizeof(json_data)
    
    compressed_data = zlib.compress(json_data)
    compressed_size = sys.getsizeof(compressed_data)
    
    end_time = time.time()
    compression_time = (end_time - start_time) * 1000 # ms
    
    stats = {
        "original_size_bytes": original_size,
        "compressed_size_bytes": compressed_size,
        "compression_ratio": f"{original_size / compressed_size:.2f}x" if compressed_size > 0 else "N/A",
        "time_taken_ms": f"{compression_time:.4f}"
    }
    
    return compressed_data, stats

def decompress_menu_data(compressed_data: bytes):
    """
    Decompresses zlib-compressed menu data back to a list of dictionaries.
    """
    start_time = time.time()
    
    decompressed_json = zlib.decompress(compressed_data)
    menu_items = json.loads(decompressed_json)
    
    end_time = time.time()
    decompression_time = (end_time - start_time) * 1000 # ms
    
    return menu_items, decompression_time
