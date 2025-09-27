#!/usr/bin/env python3
"""
Julia-focused stress test - Target the 9% success rate issue
"""

import asyncio
import random
import statistics
import sys
import time
from typing import Any

import aiohttp


class JuliaFocusedTest:
    def __init__(self, base_url: str = "http://localhost:8787"):
        self.base_url = base_url
        self.results = []
        self.start_time = time.time()

    async def julia_render(
        self,
        session: aiohttp.ClientSession,
        code: str,
        parallel: bool = False,
        unsafe: bool = False,
    ) -> dict[str, Any]:
        """Julia-specific render request"""
        payload = {
            "target": "julia",
            "code": code,
            "parallel": parallel,
            "unsafe": unsafe,
            "mode": "loops",  # Force loops mode for Julia
        }

        start_time = time.time()
        try:
            async with session.post(
                f"{self.base_url}/render",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                result = await response.json()
                duration = time.time() - start_time

                return {
                    "code": code,
                    "parallel": parallel,
                    "unsafe": unsafe,
                    "duration": duration,
                    "status": response.status,
                    "success": response.status == 200,
                    "code_length": len(result.get("code", "")),
                    "degraded": result.get("degraded", False),
                    "notes": result.get("notes", []),
                    "timing": result.get("metrics", {}),
                }
        except Exception as e:
            return {
                "code": code,
                "parallel": parallel,
                "unsafe": unsafe,
                "duration": time.time() - start_time,
                "status": 500,
                "success": False,
                "error": str(e),
            }

    def generate_julia_test_codes(self) -> list[str]:
        """Generate Julia-specific test codes"""
        return [
            # Simple list comprehension
            "[x * x for x in range(10)]",
            # Simple nested comprehension
            "[x * y for x in range(5) for y in range(5)]",
            # Simple filtering
            "[x for x in range(20) if x % 2 == 0]",
            # Simple dictionary comprehension
            "{x: x * x for x in range(10)}",
            # Simple set comprehension
            "{x * x for x in range(10)}",
            # Simple conditional
            "[x if x % 2 == 0 else x * 2 for x in range(10)]",
            # Simple nested with condition
            "[x + y for x in range(5) for y in range(5) if x > y]",
            # Simple math operations
            "[x ** 2 for x in range(10)]",
            # Simple string operations
            "[str(x) for x in range(5)]",
            # Simple range operations
            "[x for x in range(1, 11)]",
        ]

    async def julia_soak_test(
        self, session: aiohttp.ClientSession, duration_seconds: int = 600
    ):
        """Julia-focused soak test"""
        print(f"🔥 Julia Soak Test ({duration_seconds}s)...")

        test_codes = self.generate_julia_test_codes()

        start_time = time.time()
        results = []
        request_count = 0

        while time.time() - start_time < duration_seconds:
            # Create burst of Julia requests
            burst_size = random.randint(1, 5)
            tasks = []

            for i in range(burst_size):
                code = random.choice(test_codes)
                parallel = random.choice([True, False])
                unsafe = random.choice([True, False])

                task = self.julia_render(session, code, parallel, unsafe)
                tasks.append(task)

            # Execute burst
            burst_results = await asyncio.gather(*tasks, return_exceptions=True)
            valid_results = [r for r in burst_results if isinstance(r, dict)]
            results.extend(valid_results)
            request_count += len(tasks)

            # Small delay between bursts
            await asyncio.sleep(0.1)

        print(
            f"✅ Julia soak test completed: {len(results)} requests in {duration_seconds}s"
        )
        print(f"   Total attempts: {request_count}")
        print(f"   Success rate: {len(results) / request_count * 100:.1f}%")
        return results

    async def julia_concurrent_test(
        self, session: aiohttp.ClientSession, num_concurrent: int = 50
    ):
        """Julia concurrent test"""
        print(f"🔥 Julia Concurrent Test ({num_concurrent} concurrent requests)...")

        test_codes = self.generate_julia_test_codes()

        tasks = []
        for i in range(num_concurrent):
            code = random.choice(test_codes)
            parallel = random.choice([True, False])
            unsafe = random.choice([True, False])

            task = self.julia_render(session, code, parallel, unsafe)
            tasks.append(task)

        start_time = time.time()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        end_time = time.time()

        valid_results = [r for r in results if isinstance(r, dict)]

        print(
            f"✅ Julia concurrent test completed: {len(valid_results)}/{num_concurrent} in {end_time - start_time:.2f}s"
        )
        return valid_results

    async def julia_fallback_test(
        self, session: aiohttp.ClientSession, num_requests: int = 100
    ):
        """Test Julia fallback behavior"""
        print(f"🔥 Julia Fallback Test ({num_requests} requests)...")

        # Use complex codes that might trigger fallbacks
        complex_codes = [
            "[x * y for x in range(50) for y in range(50) if x % 2 == 0]",
            "[x ** 2 + y ** 2 for x in range(30) for y in range(30) if x + y < 50]",
            "[x if x % 2 == 0 else y * 2 for x in range(20) for y in range(20) if x > y]",
            "{x: x * y for x in range(20) for y in range(20) if x % 2 == 0}",
            "[x * y + z for x in range(15) for y in range(15) for z in range(15) if x + y + z < 30]",
        ]

        tasks = []
        for i in range(num_requests):
            code = random.choice(complex_codes)
            parallel = random.choice([True, False])
            unsafe = random.choice([True, False])

            task = self.julia_render(session, code, parallel, unsafe)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)
        valid_results = [r for r in results if isinstance(r, dict)]

        print(f"✅ Julia fallback test completed: {len(valid_results)}/{num_requests}")
        return valid_results

    def analyze_julia_results(self, results: list[dict[str, Any]]):
        """Analyze Julia-specific results"""
        if not results:
            print("❌ No results to analyze")
            return

        successful = [r for r in results if r.get("success", False)]
        failed = [r for r in results if not r.get("success", False)]
        degraded = [r for r in successful if r.get("degraded", False)]

        print("\n📊 Julia Test Results:")
        print(f"   Total requests: {len(results)}")
        print(f"   Successful: {len(successful)}")
        print(f"   Failed: {len(failed)}")
        print(f"   Degraded (fallback): {len(degraded)}")
        print(f"   Success rate: {len(successful) / len(results) * 100:.1f}%")
        print(f"   Degraded rate: {len(degraded) / len(successful) * 100:.1f}%")

        if successful:
            # Duration analysis
            durations = [r.get("duration", 0) for r in successful]
            print("\n⏱️  Performance Analysis:")
            print(f"   Min: {min(durations):.3f}s")
            print(f"   Max: {max(durations):.3f}s")
            print(f"   Mean: {statistics.mean(durations):.3f}s")
            print(f"   Median: {statistics.median(durations):.3f}s")
            print(f"   Std Dev: {statistics.stdev(durations):.3f}s")

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

            # Unsafe vs Safe
            unsafe_results = [r for r in successful if r.get("unsafe", False)]
            safe_results = [r for r in successful if not r.get("unsafe", False)]

            if unsafe_results and safe_results:
                unsafe_avg = statistics.mean(
                    [r.get("duration", 0) for r in unsafe_results]
                )
                safe_avg = statistics.mean([r.get("duration", 0) for r in safe_results])

                print("\n🔧 Unsafe vs Safe:")
                print(
                    f"   Unsafe: {unsafe_avg:.3f}s avg ({len(unsafe_results)} requests)"
                )
                print(f"   Safe: {safe_avg:.3f}s avg ({len(safe_results)} requests)")

            # Fallback analysis
            if degraded:
                print("\n🔄 Fallback Analysis:")
                fallback_reasons = {}
                for result in degraded:
                    notes = result.get("notes", [])
                    for note in notes:
                        if "fallback" in note.lower():
                            fallback_reasons[note] = fallback_reasons.get(note, 0) + 1

                for reason, count in fallback_reasons.items():
                    print(f"   {reason}: {count} times")

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

    async def run_julia_focused_test(self):
        """Run the complete Julia-focused test suite"""
        print("🎛️ Julia-Focused Stress Test Suite")
        print("=" * 50)
        print("🎯 Target: Improve Julia's 9% success rate to ≥99.5%")
        print("=" * 50)

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

        print("✅ Server is healthy, starting Julia-focused tests...")

        async with aiohttp.ClientSession() as session:
            all_results = []

            # Test 1: Julia concurrent
            print("\n🔥 PHASE 1: Julia Concurrent Load")
            concurrent_results = await self.julia_concurrent_test(session, 50)
            all_results.extend(concurrent_results)

            # Test 2: Julia fallback
            print("\n🔥 PHASE 2: Julia Fallback Behavior")
            fallback_results = await self.julia_fallback_test(session, 50)
            all_results.extend(fallback_results)

            # Test 3: Julia soak (shorter for demo)
            print("\n🔥 PHASE 3: Julia Soak Test")
            soak_results = await self.julia_soak_test(session, 60)
            all_results.extend(soak_results)

        # Analyze all results
        self.analyze_julia_results(all_results)

        total_time = time.time() - self.start_time
        print(f"\n🎉 Julia-focused test completed in {total_time:.2f}s")
        print(f"   Total requests: {len(all_results)}")
        print(f"   Requests/second: {len(all_results) / total_time:.2f}")

        success_rate = (
            len([r for r in all_results if r.get("success", False)])
            / len(all_results)
            * 100
        )
        print(f"   Julia success rate: {success_rate:.1f}%")

        if success_rate >= 99.5:
            print("🎉 EXCELLENT: Julia success rate ≥99.5%!")
        elif success_rate >= 95:
            print("✅ GOOD: Julia success rate ≥95%")
        elif success_rate >= 90:
            print("⚠️  FAIR: Julia success rate ≥90%")
        else:
            print("❌ POOR: Julia success rate <90% - needs optimization")


async def main():
    """Main function"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8787"

    test = JuliaFocusedTest(base_url)
    await test.run_julia_focused_test()


if __name__ == "__main__":
    asyncio.run(main())
