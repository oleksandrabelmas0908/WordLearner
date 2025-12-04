"""
Performance tests for process_word function.
Runs 10 requests with different words and measures timing.

Usage:
    pytest tests/test_process_word_performance.py -v -s
    # or directly:
    python -u tests/test_process_word_performance.py
"""

import sys
import os

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
logging.getLogger("services.agents.agents").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

import time
import statistics
from services.agents.agents import process_word


TEST_WORDS = [
    "happy",
    "run",
    "beautiful",
    "consider",
    "important",
    "knowledge",
    "achieve",
    "complex",
    "tradition",
    "opportunity",
]


def test_process_word_performance():
    """Test process_word with 10 different words and measure timing."""
    times = []
    results = []
    
    print("\n" + "=" * 60, flush=True)
    print("PROCESS_WORD PERFORMANCE TEST", flush=True)
    print("=" * 60, flush=True)
    
    for i, word in enumerate(TEST_WORDS, 1):
        print(f"\n[{i}/10] Processing: '{word}'", flush=True)
        
        start = time.perf_counter()
        try:
            result = process_word(word)
            elapsed = time.perf_counter() - start
            times.append(elapsed)
            results.append({"word": word, "success": True, "time": elapsed, "result": result})
            
            print(f"  ✓ Time: {elapsed:.2f}s", flush=True)
            print(f"  ✓ Definitions: {len(result.definitions)}", flush=True)
            for j, defn in enumerate(result.definitions, 1):
                print(f"    {j}. {defn.definition[:50]}...", flush=True)
                print(f"       Example: {defn.example[:50]}...", flush=True)
                if word.lower() in defn.example.lower():
                    print(f"       ✓ Contains '{word}'", flush=True)
                else:
                    print(f"       ✗ Missing '{word}' in example!", flush=True)
                    
        except Exception as e:
            elapsed = time.perf_counter() - start
            times.append(elapsed)
            results.append({"word": word, "success": False, "time": elapsed, "error": str(e)})
            print(f"  ✗ Error after {elapsed:.2f}s: {e}", flush=True)
    
    # Summary
    print("\n" + "=" * 60, flush=True)
    print("SUMMARY", flush=True)
    print("=" * 60, flush=True)
    
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    print(f"\nTotal requests: {len(TEST_WORDS)}", flush=True)
    print(f"Successful: {len(successful)}", flush=True)
    print(f"Failed: {len(failed)}", flush=True)
    
    if times:
        print(f"\nTiming Statistics:", flush=True)
        print(f"  Min time:     {min(times):.2f}s", flush=True)
        print(f"  Max time:     {max(times):.2f}s", flush=True)
        print(f"  Avg time:     {statistics.mean(times):.2f}s", flush=True)
        print(f"  Median time:  {statistics.median(times):.2f}s", flush=True)
        print(f"  Total time:   {sum(times):.2f}s", flush=True)
        if len(times) > 1:
            print(f"  Std dev:      {statistics.stdev(times):.2f}s", flush=True)
    
    print("\nPer-word breakdown:", flush=True)
    print("-" * 40, flush=True)
    for r in results:
        status = "✓" if r["success"] else "✗"
        print(f"  {status} {r['word']:<15} {r['time']:.2f}s", flush=True)
    
    print("=" * 60, flush=True)
    
    # Assertions
    assert len(successful) > 0, "At least one request should succeed"
    assert statistics.mean(times) < 60, "Average time should be under 60 seconds"


if __name__ == "__main__":
    test_process_word_performance()
