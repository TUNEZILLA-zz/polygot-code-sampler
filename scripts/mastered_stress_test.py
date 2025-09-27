#!/usr/bin/env python3
"""
Code Live Mastered Stress Test - Self-tuning live performance demonstration
"""

import asyncio
import random
import statistics
import sys
import time
from typing import Any

import aiohttp


class MasteredStressTest:
    def __init__(self, base_url: str = "http://localhost:8787"):
        self.base_url = base_url
        self.results = []
        self.start_time = time.time()

    async def mastered_render(
        self,
        session: aiohttp.ClientSession,
        target: str,
        code: str,
        parallel: bool = False,
    ) -> dict[str, Any]:
        """Mastered render request with circuit breaker and rate limiting"""
        payload = {"target": target, "code": code, "parallel": parallel}

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
                    "target": target,
                    "code": code,
                    "parallel": parallel,
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
                "target": target,
                "code": code,
                "parallel": parallel,
                "duration": time.time() - start_time,
                "status": 500,
                "success": False,
                "error": str(e),
            }

    def generate_mastered_codes(self) -> list[str]:
        """Generate test codes for mastered performance testing"""
        return [
            # Simple cases (should work perfectly)
            "[x * x for x in range(10)]",
            "[x for x in range(20) if x % 2 == 0]",
            "{x: x * x for x in range(10)}",
            # Medium complexity (should work with fallbacks)
            "[x * y for x in range(20) for y in range(20) if x % 2 == 0]",
            "[x ** 2 + y ** 2 for x in range(15) for y in range(15) if x + y < 20]",
            "{x: {y: x * y for y in range(10) if y % 2 == 0} for x in range(10)}",
            # Complex cases (should trigger circuit breakers)
            "[x * y * z for x in range(30) for y in range(30) for z in range(30) if x + y + z < 50]",
            "[x ** 3 + y ** 2 + z for x in range(25) for y in range(25) for z in range(25) if x % 2 == 0]",
            "[[x * y for y in range(15)] for x in range(20) if x % 2 == 0]",
            # Edge cases (should test limits)
            "[x for x in range(1000) if x % 2 == 0 and x % 3 == 0 and x % 5 == 0]",
            "[x * y + z * w for x in range(20) for y in range(20) for z in range(20) for w in range(20) if x + y + z + w < 40]",
        ]

    async def circuit_breaker_test(
        self, session: aiohttp.ClientSession, target: str, num_requests: int = 50
    ):
        """Test circuit breaker behavior"""
        print(f"🔥 Circuit Breaker Test for {target} ({num_requests} requests)...")

        # Use complex codes that might trigger circuit breaker
        complex_codes = [
            "[x * y * z for x in range(50) for y in range(50) for z in range(50) if x + y + z < 100]",
            "[x ** 3 + y ** 2 + z for x in range(40) for y in range(40) for z in range(40) if x % 2 == 0]",
            "[[x * y for y in range(25)] for x in range(30) if x % 2 == 0]",
        ]

        tasks = []
        for i in range(num_requests):
            code = random.choice(complex_codes)
            parallel = random.choice([True, False])

            task = self.mastered_render(session, target, code, parallel)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)
        valid_results = [r for r in results if isinstance(r, dict)]

        print(f"✅ Circuit breaker test completed: {len(valid_results)}/{num_requests}")
        return valid_results

    async def adaptive_rate_limit_test(
        self, session: aiohttp.ClientSession, target: str, duration_seconds: int = 30
    ):
        """Test adaptive rate limiting"""
        print(f"🔥 Adaptive Rate Limit Test for {target} ({duration_seconds}s)...")

        test_codes = self.generate_mastered_codes()

        start_time = time.time()
        results = []
        request_count = 0

        while time.time() - start_time < duration_seconds:
            # Create burst of requests
            burst_size = random.randint(5, 15)
            tasks = []

            for i in range(burst_size):
                code = random.choice(test_codes)
                parallel = random.choice([True, False])

                task = self.mastered_render(session, target, code, parallel)
                tasks.append(task)

            # Execute burst
            burst_results = await asyncio.gather(*tasks, return_exceptions=True)
            valid_results = [r for r in burst_results if isinstance(r, dict)]
            results.extend(valid_results)
            request_count += len(tasks)

            # Small delay between bursts
            await asyncio.sleep(0.1)

        print(
            f"✅ Adaptive rate limit test completed: {len(results)} requests in {duration_seconds}s"
        )
        print(f"   Total attempts: {request_count}")
        print(f"   Success rate: {len(results) / request_count * 100:.1f}%")
        return results

    async def self_tuning_test(
        self, session: aiohttp.ClientSession, duration_seconds: int = 60
    ):
        """Test self-tuning performance"""
        print(f"🔥 Self-Tuning Test ({duration_seconds}s of adaptive performance)...")

        targets = ["rust", "ts", "go", "csharp", "sql", "julia"]
        test_codes = self.generate_mastered_codes()

        start_time = time.time()
        results = []
        phase = 0

        while time.time() - start_time < duration_seconds:
            elapsed = time.time() - start_time

            # Vary load intensity to test self-tuning
            if elapsed < 20:  # Ramp up
                intensity = 0.2 + (elapsed / 20) * 0.8
            elif elapsed < 40:  # Peak load
                intensity = 1.0
            else:  # Ramp down
                intensity = 1.0 - ((elapsed - 40) / 20) * 0.8

            # Determine burst size based on intensity
            burst_size = max(1, int(10 * intensity))

            tasks = []
            for i in range(burst_size):
                target = random.choice(targets)
                code = random.choice(test_codes)
                parallel = random.choice([True, False])

                task = self.mastered_render(session, target, code, parallel)
                tasks.append(task)

            # Execute burst
            burst_results = await asyncio.gather(*tasks, return_exceptions=True)
            valid_results = [r for r in burst_results if isinstance(r, dict)]
            results.extend(valid_results)

            # Vary delay based on intensity
            delay = max(0.01, 0.1 - (intensity * 0.08))
            await asyncio.sleep(delay)

        print(f"✅ Self-tuning test completed: {len(results)} requests")
        return results

    async def creative_workflow_test(
        self, session: aiohttp.ClientSession, duration_seconds: int = 45
    ):
        """Test creative workflow with MIDI-like activity"""
        print(
            f"🔥 Creative Workflow Test ({duration_seconds}s of creative activity)..."
        )

        targets = ["rust", "ts", "go", "csharp", "sql", "julia"]
        test_codes = self.generate_mastered_codes()

        start_time = time.time()
        results = []

        while time.time() - start_time < duration_seconds:
            # Simulate creative workflow patterns
            if random.random() < 0.7:  # 70% single renders (like playing notes)
                target = random.choice(targets)
                code = random.choice(test_codes)
                parallel = random.choice([True, False])

                result = await self.mastered_render(session, target, code, parallel)
                results.append(result)
            elif random.random() < 0.9:  # 20% batch renders (like recording)
                # Simulate batch render
                batch_size = random.randint(2, 5)
                tasks = []

                for i in range(batch_size):
                    target = random.choice(targets)
                    code = random.choice(test_codes)
                    parallel = random.choice([True, False])

                    task = self.mastered_render(session, target, code, parallel)
                    tasks.append(task)

                batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                valid_results = [r for r in batch_results if isinstance(r, dict)]
                results.extend(valid_results)
            else:  # 10% glitch effects (like creative experimentation)
                # Simulate glitch activation
                if random.random() < 0.1:  # 10% chance of glitch
                    try:
                        async with session.post(
                            f"{self.base_url}/glitch",
                            json={"intensity": random.random()},
                        ) as response:
                            if response.status == 200:
                                print("🎵 Glitch effect activated!")
                    except:
                        pass

            # Creative timing (like human performance)
            await asyncio.sleep(random.uniform(0.05, 0.2))

        print(f"✅ Creative workflow test completed: {len(results)} requests")
        return results

    def analyze_mastered_results(self, results: list[dict[str, Any]]):
        """Analyze mastered stress test results"""
        if not results:
            print("❌ No results to analyze")
            return

        successful = [r for r in results if r.get("success", False)]
        failed = [r for r in results if not r.get("success", False)]
        degraded = [r for r in successful if r.get("degraded", False)]

        print("\n📊 Mastered Performance Results:")
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
            print(f"   p95: {sorted(durations)[int(len(durations) * 0.95)]:.3f}s")
            print(f"   p99: {sorted(durations)[int(len(durations) * 0.99)]:.3f}s")

            # Backend performance
            target_stats = {}
            for result in successful:
                target = result.get("target", "unknown")
                if target not in target_stats:
                    target_stats[target] = []
                target_stats[target].append(result.get("duration", 0))

            print("\n🎛️  Backend Performance (Mastered):")
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

            # Circuit breaker analysis
            circuit_breaker_failures = [
                r
                for r in failed
                if "circuit breaker" in str(r.get("error", "")).lower()
            ]
            rate_limit_failures = [
                r for r in failed if "rate limit" in str(r.get("error", "")).lower()
            ]

            if circuit_breaker_failures:
                print("\n🔌 Circuit Breaker Analysis:")
                print(f"   Circuit breaker failures: {len(circuit_breaker_failures)}")
                print(
                    f"   Circuit breaker rate: {len(circuit_breaker_failures) / len(failed) * 100:.1f}%"
                )

            if rate_limit_failures:
                print("\n🚦 Rate Limiting Analysis:")
                print(f"   Rate limit failures: {len(rate_limit_failures)}")
                print(
                    f"   Rate limit rate: {len(rate_limit_failures) / len(failed) * 100:.1f}%"
                )

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

    async def run_mastered_stress_test(self):
        """Run the complete mastered stress test suite"""
        print("🎛️ Code Live Mastered Stress Test Suite")
        print("=" * 60)
        print("🎯 Target: Self-tuning live performance with circuit breakers")
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

        print("✅ Server is healthy, starting mastered stress tests...")

        async with aiohttp.ClientSession() as session:
            all_results = []

            # Test 1: Circuit breaker test
            print("\n🔥 PHASE 1: Circuit Breaker Test")
            circuit_results = await self.circuit_breaker_test(session, "julia", 30)
            all_results.extend(circuit_results)

            # Test 2: Adaptive rate limiting
            print("\n🔥 PHASE 2: Adaptive Rate Limiting")
            rate_limit_results = await self.adaptive_rate_limit_test(
                session, "rust", 20
            )
            all_results.extend(rate_limit_results)

            # Test 3: Self-tuning performance
            print("\n🔥 PHASE 3: Self-Tuning Performance")
            self_tuning_results = await self.self_tuning_test(session, 30)
            all_results.extend(self_tuning_results)

            # Test 4: Creative workflow
            print("\n🔥 PHASE 4: Creative Workflow")
            creative_results = await self.creative_workflow_test(session, 30)
            all_results.extend(creative_results)

        # Analyze all results
        self.analyze_mastered_results(all_results)

        total_time = time.time() - self.start_time
        print(f"\n🎉 Mastered stress test completed in {total_time:.2f}s")
        print(f"   Total requests: {len(all_results)}")
        print(f"   Requests/second: {len(all_results) / total_time:.2f}")

        success_rate = (
            len([r for r in all_results if r.get("success", False)])
            / len(all_results)
            * 100
        )
        print(f"   Overall success rate: {success_rate:.1f}%")

        if success_rate >= 95:
            print("🎉 EXCELLENT: Mastered performance ≥95%!")
        elif success_rate >= 90:
            print("✅ GOOD: Mastered performance ≥90%")
        elif success_rate >= 85:
            print("⚠️  FAIR: Mastered performance ≥85%")
        else:
            print("❌ POOR: Mastered performance <85% - needs optimization")


async def main():
    """Main function"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8787"

    test = MasteredStressTest(base_url)
    await test.run_mastered_stress_test()


if __name__ == "__main__":
    asyncio.run(main())
