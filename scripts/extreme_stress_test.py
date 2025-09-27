#!/usr/bin/env python3
"""
Code Live Extreme Stress Test - Push the system to its absolute limits!
"""

import asyncio
import random
import statistics
import sys
import time
from typing import Any, Dict, List

import aiohttp


class ExtremeStressTest:
    def __init__(self, base_url: str = "http://localhost:8787"):
        self.base_url = base_url
        self.results = []
        self.start_time = time.time()

    async def extreme_single_render(
        self,
        session: aiohttp.ClientSession,
        target: str,
        code: str,
        parallel: bool = False,
    ) -> Dict[str, Any]:
        """Extreme single render request"""
        payload = {"target": target, "code": code, "parallel": parallel}

        start_time = time.time()
        try:
            async with session.post(
                f"{self.base_url}/render",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=5),
            ) as response:
                result = await response.json()
                duration = time.time() - start_time

                return {
                    "target": target,
                    "code": code,
                    "parallel": parallel,
                    "duration": duration,
                    "status": response.status,
                    "success": response.status == 200,
                    "code_length": len(result.get("code", "")),
                    "timing": result.get("timing", {}),
                }
        except Exception as e:
            return {
                "target": target,
                "code": code,
                "parallel": parallel,
                "duration": time.time() - start_time,
                "status": 500,
                "success": False,
                "error": str(e),
            }

    def generate_extreme_codes(self) -> List[str]:
        """Generate extreme test codes for maximum stress"""
        return [
            # Massive nested comprehension
            "[x * y * z for x in range(100) for y in range(100) for z in range(10) if x % 2 == 0 and y % 3 == 0]",
            # Complex dictionary with nested operations
            "{x: {y: x * y for y in range(50) if y % 2 == 0} for x in range(100) if x % 3 == 0}",
            # Deeply nested set comprehension
            "{x + y + z for x in range(50) for y in range(50) for z in range(20) if x > y and y > z}",
            # Complex filtering with multiple conditions
            "[x ** 2 + y ** 2 + z ** 2 for x in range(80) for y in range(80) for z in range(40) if x % 2 == 0 and y % 3 == 0 and z % 5 == 0 and x + y + z < 100]",
            # String operations with large ranges
            "[str(x) + str(y) + str(z) for x in range(30) for y in range(30) for z in range(30) if x < y < z]",
            # Mathematical operations
            "[x * y + z * w for x in range(40) for y in range(40) for z in range(40) for w in range(40) if x + y + z + w < 100]",
            # Complex conditional logic
            "[x if x % 2 == 0 else y * 2 for x in range(200) for y in range(200) if x + y < 150]",
            # Nested with multiple levels
            "[[x * y for y in range(20)] for x in range(50) if x % 2 == 0]",
            # Large range with complex math
            "[x ** 3 + y ** 2 + z for x in range(60) for y in range(60) for z in range(60) if x % 2 == 0 and y % 3 == 0]",
            # Multiple operations
            "[x * y + z * w + v for x in range(25) for y in range(25) for z in range(25) for w in range(25) for v in range(25) if x + y + z + w + v < 100]",
        ]

    async def extreme_concurrent_test(
        self, session: aiohttp.ClientSession, num_concurrent: int = 100
    ):
        """Extreme concurrent test"""
        print(f"🔥 EXTREME Concurrent Test ({num_concurrent} concurrent requests)...")

        targets = ["rust", "ts", "go", "csharp", "sql", "julia"]
        extreme_codes = self.generate_extreme_codes()

        tasks = []
        for i in range(num_concurrent):
            target = random.choice(targets)
            code = random.choice(extreme_codes)
            parallel = random.choice([True, False])

            task = self.extreme_single_render(session, target, code, parallel)
            tasks.append(task)

        start_time = time.time()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        end_time = time.time()

        valid_results = [r for r in results if isinstance(r, dict)]

        print(
            f"✅ Extreme concurrent test completed: {len(valid_results)}/{num_concurrent} in {end_time - start_time:.2f}s"
        )
        return valid_results

    async def extreme_sustained_test(
        self, session: aiohttp.ClientSession, duration_seconds: int = 60
    ):
        """Extreme sustained load test"""
        print(f"🔥 EXTREME Sustained Test ({duration_seconds}s of maximum load)...")

        targets = ["rust", "ts", "go", "csharp", "sql", "julia"]
        extreme_codes = self.generate_extreme_codes()

        start_time = time.time()
        results = []
        request_count = 0

        while time.time() - start_time < duration_seconds:
            # Create burst of concurrent requests
            burst_size = random.randint(10, 30)
            tasks = []

            for i in range(burst_size):
                target = random.choice(targets)
                code = random.choice(extreme_codes)
                parallel = random.choice([True, False])

                task = self.extreme_single_render(session, target, code, parallel)
                tasks.append(task)

            # Execute burst
            burst_results = await asyncio.gather(*tasks, return_exceptions=True)
            valid_results = [r for r in burst_results if isinstance(r, dict)]
            results.extend(valid_results)
            request_count += len(tasks)

            # Small delay between bursts
            await asyncio.sleep(0.05)

        print(
            f"✅ Extreme sustained test completed: {len(results)} successful requests in {duration_seconds}s"
        )
        print(f"   Total attempts: {request_count}")
        print(f"   Success rate: {len(results) / request_count * 100:.1f}%")
        return results

    async def extreme_mixed_workload(
        self, session: aiohttp.ClientSession, duration_seconds: int = 45
    ):
        """Extreme mixed workload with varying intensity"""
        print(
            f"🔥 EXTREME Mixed Workload ({duration_seconds}s with varying intensity)..."
        )

        targets = ["rust", "ts", "go", "csharp", "sql", "julia"]
        extreme_codes = self.generate_extreme_codes()

        start_time = time.time()
        results = []
        phase = 0

        while time.time() - start_time < duration_seconds:
            elapsed = time.time() - start_time

            # Vary intensity based on time
            if elapsed < 15:  # Ramp up
                intensity = 0.1 + (elapsed / 15) * 0.9
            elif elapsed < 30:  # Peak load
                intensity = 1.0
            else:  # Ramp down
                intensity = 1.0 - ((elapsed - 30) / 15) * 0.9

            # Determine burst size based on intensity
            burst_size = max(1, int(20 * intensity))

            tasks = []
            for i in range(burst_size):
                target = random.choice(targets)
                code = random.choice(extreme_codes)
                parallel = random.choice([True, False])

                task = self.extreme_single_render(session, target, code, parallel)
                tasks.append(task)

            # Execute burst
            burst_results = await asyncio.gather(*tasks, return_exceptions=True)
            valid_results = [r for r in burst_results if isinstance(r, dict)]
            results.extend(valid_results)

            # Vary delay based on intensity
            delay = max(0.01, 0.1 - (intensity * 0.08))
            await asyncio.sleep(delay)

        print(f"✅ Extreme mixed workload completed: {len(results)} requests")
        return results

    def analyze_extreme_results(self, results: List[Dict[str, Any]]):
        """Analyze extreme stress test results"""
        if not results:
            print("❌ No results to analyze")
            return

        successful = [r for r in results if r.get("success", False)]
        failed = [r for r in results if not r.get("success", False)]

        print("\n📊 EXTREME Stress Test Results:")
        print(f"   Total requests: {len(results)}")
        print(f"   Successful: {len(successful)}")
        print(f"   Failed: {len(failed)}")
        print(f"   Success rate: {len(successful) / len(results) * 100:.1f}%")

        if successful:
            # Duration analysis
            durations = [r.get("duration", 0) for r in successful]
            print("\n⏱️  Performance Analysis:")
            print(f"   Min: {min(durations):.3f}s")
            print(f"   Max: {max(durations):.3f}s")
            print(f"   Mean: {statistics.mean(durations):.3f}s")
            print(f"   Median: {statistics.median(durations):.3f}s")
            print(f"   Std Dev: {statistics.stdev(durations):.3f}s")
            print(f"   p95: {sorted(durations)[int(len(durations) * 0.95)]:.3f}s")
            print(f"   p99: {sorted(durations)[int(len(durations) * 0.99)]:.3f}s")

            # Backend performance
            target_stats = {}
            for result in successful:
                target = result.get("target", "unknown")
                if target not in target_stats:
                    target_stats[target] = []
                target_stats[target].append(result.get("duration", 0))

            print("\n🎛️  Backend Performance Under Extreme Load:")
            for target, durations in target_stats.items():
                if durations:
                    avg_duration = statistics.mean(durations)
                    max_duration = max(durations)
                    success_rate = (
                        len(durations)
                        / (
                            len(durations)
                            + len(
                                [
                                    r
                                    for r in results
                                    if r.get("target") == target
                                    and not r.get("success", False)
                                ]
                            )
                        )
                        * 100
                    )
                    print(
                        f"   {target}: {avg_duration:.3f}s avg, {max_duration:.3f}s max ({len(durations)} requests, {success_rate:.1f}% success)"
                    )

            # Parallel vs Sequential under extreme load
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

                print("\n⚡ Parallel Performance Under Extreme Load:")
                print(
                    f"   Parallel: {parallel_avg:.3f}s avg ({len(parallel_results)} requests)"
                )
                print(
                    f"   Sequential: {sequential_avg:.3f}s avg ({len(sequential_results)} requests)"
                )
                print(f"   Speedup: {speedup:.2f}x")

            # Timing breakdown
            timing_data = []
            for result in successful:
                timing = result.get("timing", {})
                if timing:
                    timing_data.append(timing)

            if timing_data:
                parse_times = [
                    t.get("parse_ms", 0) for t in timing_data if t.get("parse_ms")
                ]
                render_times = [
                    t.get("render_ms", 0) for t in timing_data if t.get("render_ms")
                ]

                if parse_times:
                    print("\n🔍 Timing Breakdown:")
                    print(
                        f"   Parse: {statistics.mean(parse_times):.2f}ms avg, {max(parse_times):.2f}ms max"
                    )
                if render_times:
                    print(
                        f"   Render: {statistics.mean(render_times):.2f}ms avg, {max(render_times):.2f}ms max"
                    )

        if failed:
            print("\n❌ Failure Analysis:")
            error_counts = {}
            for result in failed:
                error = result.get("error", "Unknown error")
                error_counts[error] = error_counts.get(error, 0) + 1

            for error, count in sorted(
                error_counts.items(), key=lambda x: x[1], reverse=True
            ):
                print(f"   {error}: {count} times")

    async def run_extreme_stress_test(self):
        """Run the complete extreme stress test suite"""
        print("🎛️ Code Live EXTREME Stress Test Suite")
        print("=" * 60)
        print("⚠️  WARNING: This will push the system to its absolute limits!")
        print("=" * 60)

        # Check server health
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/health") as response:
                    if response.status != 200:
                        print(f"❌ Server health check failed: {response.status}")
                        return
        except Exception as e:
            print(f"❌ Cannot connect to server: {e}")
            return

        print("✅ Server is healthy, starting EXTREME stress tests...")

        async with aiohttp.ClientSession() as session:
            all_results = []

            # Test 1: Extreme concurrent
            print("\n🔥 PHASE 1: Extreme Concurrent Load")
            concurrent_results = await self.extreme_concurrent_test(session, 100)
            all_results.extend(concurrent_results)

            # Test 2: Extreme sustained
            print("\n🔥 PHASE 2: Extreme Sustained Load")
            sustained_results = await self.extreme_sustained_test(session, 30)
            all_results.extend(sustained_results)

            # Test 3: Extreme mixed workload
            print("\n🔥 PHASE 3: Extreme Mixed Workload")
            mixed_results = await self.extreme_mixed_workload(session, 30)
            all_results.extend(mixed_results)

        # Analyze all results
        self.analyze_extreme_results(all_results)

        total_time = time.time() - self.start_time
        print(f"\n🎉 EXTREME stress test completed in {total_time:.2f}s")
        print(f"   Total requests: {len(all_results)}")
        print(f"   Requests/second: {len(all_results) / total_time:.2f}")
        print(
            f"   System resilience: {'EXCELLENT' if len([r for r in all_results if r.get('success', False)]) / len(all_results) > 0.8 else 'NEEDS IMPROVEMENT'}"
        )


async def main():
    """Main function"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8787"

    stress_test = ExtremeStressTest(base_url)
    await stress_test.run_extreme_stress_test()


if __name__ == "__main__":
    asyncio.run(main())
