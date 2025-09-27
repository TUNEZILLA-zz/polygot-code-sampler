#!/usr/bin/env python3
"""
Code Live Stress Test - Push the system to its limits and watch the performance spectrum!
"""

import asyncio
import random
import statistics
import sys
import time
from typing import Any, Dict, List

import aiohttp


class CodeLiveStressTest:
    def __init__(self, base_url: str = "http://localhost:8787"):
        self.base_url = base_url
        self.results = []
        self.start_time = time.time()

    async def single_render(
        self,
        session: aiohttp.ClientSession,
        backend: str,
        code: str,
        parallel: bool = False,
    ) -> Dict[str, Any]:
        """Single render request"""
        payload = {"target": backend, "code": code, "parallel": parallel}

        start_time = time.time()
        try:
            async with session.post(
                f"{self.base_url}/render", json=payload
            ) as response:
                result = await response.json()
                duration = time.time() - start_time

                return {
                    "backend": backend,
                    "code": code,
                    "parallel": parallel,
                    "duration": duration,
                    "status": response.status,
                    "code_length": len(result.get("code", "")),
                    "latency_ms": result.get("metrics", {}).get("latency_ms", 0),
                    "success": response.status == 200,
                }
        except Exception as e:
            return {
                "backend": backend,
                "code": code,
                "parallel": parallel,
                "duration": time.time() - start_time,
                "status": 500,
                "code_length": 0,
                "latency_ms": 0,
                "success": False,
                "error": str(e),
            }

    async def batch_render(
        self, session: aiohttp.ClientSession, tracks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Batch render request"""
        payload = {"tracks": tracks}

        start_time = time.time()
        try:
            async with session.post(
                f"{self.base_url}/render/batch", json=payload
            ) as response:
                result = await response.json()
                duration = time.time() - start_time

                return {
                    "track_count": len(tracks),
                    "duration": duration,
                    "status": response.status,
                    "success": response.status == 200,
                    "tracks": result.get("tracks", []),
                }
        except Exception as e:
            return {
                "track_count": len(tracks),
                "duration": time.time() - start_time,
                "status": 500,
                "success": False,
                "error": str(e),
            }

    def generate_test_codes(self) -> List[str]:
        """Generate various test codes for stress testing"""
        return [
            # Simple list comprehension
            "[x * x for x in range(100)]",
            # Complex nested comprehension
            "[x * y for x in range(50) for y in range(50) if x % 2 == 0 and y % 3 == 0]",
            # Dictionary comprehension
            "{x: x * x for x in range(100) if x % 2 == 0}",
            # Set comprehension
            "{x * x for x in range(100) if x % 2 == 0}",
            # Complex filtering
            "[x for x in range(1000) if x % 2 == 0 and x % 3 == 0 and x % 5 == 0]",
            # Nested with conditions
            "[x + y for x in range(20) for y in range(20) if x > y and x % 2 == 0]",
            # Large range
            "[x * x for x in range(1000) if x % 2 == 0]",
            # Complex math
            "[x ** 2 + y ** 2 for x in range(30) for y in range(30) if x + y < 50]",
            # String operations
            "[str(x) + str(y) for x in range(20) for y in range(20) if x < y]",
            # Multiple conditions
            "[x for x in range(500) if x % 2 == 0 and x % 3 == 0 and x % 7 == 0]",
        ]

    async def stress_test_single_renders(
        self, session: aiohttp.ClientSession, num_requests: int = 100
    ):
        """Stress test with single renders"""
        print(f"🔥 Stress Testing Single Renders ({num_requests} requests)...")

        backends = ["rust", "ts", "go", "csharp", "sql", "julia"]
        test_codes = self.generate_test_codes()

        tasks = []
        for i in range(num_requests):
            backend = random.choice(backends)
            code = random.choice(test_codes)
            parallel = random.choice([True, False])

            task = self.single_render(session, backend, code, parallel)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions
        valid_results = [r for r in results if isinstance(r, dict)]

        print(f"✅ Single renders completed: {len(valid_results)}/{num_requests}")
        return valid_results

    async def stress_test_batch_renders(
        self, session: aiohttp.ClientSession, num_batches: int = 20
    ):
        """Stress test with batch renders"""
        print(f"🔥 Stress Testing Batch Renders ({num_batches} batches)...")

        backends = ["rust", "ts", "go", "csharp", "sql", "julia"]
        test_codes = self.generate_test_codes()

        tasks = []
        for i in range(num_batches):
            # Create batch with 2-5 tracks
            track_count = random.randint(2, 5)
            tracks = []

            for j in range(track_count):
                backend = random.choice(backends)
                code = random.choice(test_codes)
                parallel = random.choice([True, False])

                tracks.append({"target": backend, "code": code, "parallel": parallel})

            task = self.batch_render(session, tracks)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions
        valid_results = [r for r in results if isinstance(r, dict)]

        print(f"✅ Batch renders completed: {len(valid_results)}/{num_batches}")
        return valid_results

    async def stress_test_concurrent_renders(
        self, session: aiohttp.ClientSession, num_concurrent: int = 50
    ):
        """Stress test with concurrent renders"""
        print(f"🔥 Stress Testing Concurrent Renders ({num_concurrent} concurrent)...")

        backends = ["rust", "ts", "go", "csharp", "sql", "julia"]
        test_codes = self.generate_test_codes()

        # Create concurrent tasks
        tasks = []
        for i in range(num_concurrent):
            backend = random.choice(backends)
            code = random.choice(test_codes)
            parallel = random.choice([True, False])

            task = self.single_render(session, backend, code, parallel)
            tasks.append(task)

        # Run all tasks concurrently
        start_time = time.time()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        end_time = time.time()

        # Filter out exceptions
        valid_results = [r for r in results if isinstance(r, dict)]

        print(
            f"✅ Concurrent renders completed: {len(valid_results)}/{num_concurrent} in {end_time - start_time:.2f}s"
        )
        return valid_results

    async def stress_test_mixed_workload(
        self, session: aiohttp.ClientSession, duration_seconds: int = 60
    ):
        """Stress test with mixed workload for specified duration"""
        print(f"🔥 Stress Testing Mixed Workload ({duration_seconds}s)...")

        backends = ["rust", "ts", "go", "csharp", "sql", "julia"]
        test_codes = self.generate_test_codes()

        start_time = time.time()
        results = []

        while time.time() - start_time < duration_seconds:
            # Randomly choose between single and batch renders
            if random.random() < 0.7:  # 70% single renders
                backend = random.choice(backends)
                code = random.choice(test_codes)
                parallel = random.choice([True, False])

                result = await self.single_render(session, backend, code, parallel)
                results.append(result)
            else:  # 30% batch renders
                track_count = random.randint(2, 4)
                tracks = []

                for j in range(track_count):
                    backend = random.choice(backends)
                    code = random.choice(test_codes)
                    parallel = random.choice([True, False])

                    tracks.append(
                        {"target": backend, "code": code, "parallel": parallel}
                    )

                result = await self.batch_render(session, tracks)
                results.append(result)

            # Small delay to prevent overwhelming
            await asyncio.sleep(0.1)

        print(
            f"✅ Mixed workload completed: {len(results)} requests in {duration_seconds}s"
        )
        return results

    def analyze_results(self, results: List[Dict[str, Any]]):
        """Analyze stress test results"""
        if not results:
            print("❌ No results to analyze")
            return

        # Filter successful results
        successful = [r for r in results if r.get("success", False)]
        failed = [r for r in results if not r.get("success", False)]

        print("\n📊 Stress Test Results:")
        print(f"   Total requests: {len(results)}")
        print(f"   Successful: {len(successful)}")
        print(f"   Failed: {len(failed)}")
        print(f"   Success rate: {len(successful) / len(results) * 100:.1f}%")

        if successful:
            # Duration analysis
            durations = [r.get("duration", 0) for r in successful]
            print("\n⏱️  Duration Analysis:")
            print(f"   Min: {min(durations):.3f}s")
            print(f"   Max: {max(durations):.3f}s")
            print(f"   Mean: {statistics.mean(durations):.3f}s")
            print(f"   Median: {statistics.median(durations):.3f}s")
            print(f"   Std Dev: {statistics.stdev(durations):.3f}s")

            # Backend analysis
            backend_stats = {}
            for result in successful:
                backend = result.get("backend", "unknown")
                if backend not in backend_stats:
                    backend_stats[backend] = []
                backend_stats[backend].append(result.get("duration", 0))

            print("\n🎛️  Backend Performance:")
            for backend, durations in backend_stats.items():
                if durations:
                    print(
                        f"   {backend}: {statistics.mean(durations):.3f}s avg ({len(durations)} requests)"
                    )

            # Parallel vs Sequential
            parallel_results = [r for r in successful if r.get("parallel", False)]
            sequential_results = [r for r in successful if not r.get("parallel", False)]

            if parallel_results and sequential_results:
                parallel_avg = statistics.mean(
                    [r.get("duration", 0) for r in parallel_results]
                )
                sequential_avg = statistics.mean(
                    [r.get("duration", 0) for r in sequential_results]
                )
                speedup = sequential_avg / parallel_avg if parallel_avg > 0 else 0

                print("\n⚡ Parallel Performance:")
                print(
                    f"   Parallel: {parallel_avg:.3f}s avg ({len(parallel_results)} requests)"
                )
                print(
                    f"   Sequential: {sequential_avg:.3f}s avg ({len(sequential_results)} requests)"
                )
                print(f"   Speedup: {speedup:.2f}x")

        if failed:
            print("\n❌ Failed Requests:")
            error_counts = {}
            for result in failed:
                error = result.get("error", "Unknown error")
                error_counts[error] = error_counts.get(error, 0) + 1

            for error, count in error_counts.items():
                print(f"   {error}: {count} times")

    async def run_full_stress_test(self):
        """Run the complete stress test suite"""
        print("🎛️ Code Live Stress Test Suite")
        print("=" * 50)

        # Check if server is running
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/health") as response:
                    if response.status != 200:
                        print(f"❌ Server health check failed: {response.status}")
                        return
        except Exception as e:
            print(f"❌ Cannot connect to server: {e}")
            return

        print("✅ Server is healthy, starting stress tests...")

        async with aiohttp.ClientSession() as session:
            all_results = []

            # Test 1: Single renders
            single_results = await self.stress_test_single_renders(session, 50)
            all_results.extend(single_results)

            # Test 2: Batch renders
            batch_results = await self.stress_test_batch_renders(session, 10)
            all_results.extend(batch_results)

            # Test 3: Concurrent renders
            concurrent_results = await self.stress_test_concurrent_renders(session, 30)
            all_results.extend(concurrent_results)

            # Test 4: Mixed workload
            mixed_results = await self.stress_test_mixed_workload(session, 30)
            all_results.extend(mixed_results)

        # Analyze all results
        self.analyze_results(all_results)

        total_time = time.time() - self.start_time
        print(f"\n🎉 Stress test completed in {total_time:.2f}s")
        print(f"   Total requests: {len(all_results)}")
        print(f"   Requests/second: {len(all_results) / total_time:.2f}")


async def main():
    """Main function"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8787"

    stress_test = CodeLiveStressTest(base_url)
    await stress_test.run_full_stress_test()


if __name__ == "__main__":
    asyncio.run(main())
