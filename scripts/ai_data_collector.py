#!/usr/bin/env python3
"""
AI Data Collector for Code Live
Collects training data for AI plugins from stress tests, benchmarks, and user interactions
"""

import asyncio
import json
import logging
import random
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CodePattern:
    """Represents a code pattern for AI training"""

    code: str
    target: str
    parallel: bool
    complexity: int
    nested_level: int
    functional_style: bool
    mathematical_ops: bool
    data_processing: bool
    scientific: bool
    web_development: bool
    concurrent: bool
    enterprise: bool


@dataclass
class PerformanceMetrics:
    """Represents performance metrics for AI training"""

    latency_ms: float
    throughput_rps: float
    memory_usage_mb: float
    cache_hit_rate: float
    success_rate: float
    error_rate: float
    fallback_rate: float
    degradation_rate: float


@dataclass
class OptimizationResult:
    """Represents optimization results for AI training"""

    original_code: str
    optimized_code: str
    optimization_type: str
    performance_improvement: float
    memory_improvement: float
    cache_improvement: float
    parallel_speedup: float
    unsafe_benefit: float


@dataclass
class UserInteraction:
    """Represents user interaction data for AI training"""

    timestamp: datetime
    user_action: str
    parameters: dict[str, Any]
    result_satisfaction: float
    performance_feedback: float
    creativity_rating: float
    learning_preference: str


@dataclass
class AITrainingData:
    """Complete AI training dataset"""

    code_patterns: list[CodePattern]
    performance_metrics: list[PerformanceMetrics]
    optimization_results: list[OptimizationResult]
    user_interactions: list[UserInteraction]
    preset_recommendations: list[dict[str, Any]]
    adaptive_tuning_data: list[dict[str, Any]]
    patch_generation_data: list[dict[str, Any]]
    pattern_detection_data: list[dict[str, Any]]
    chaos_enhancement_data: list[dict[str, Any]]
    prediction_data: list[dict[str, Any]]
    style_transfer_data: list[dict[str, Any]]


class AIDataCollector:
    """Collects training data for AI plugins"""

    def __init__(self, base_url: str = "http://localhost:8787"):
        self.base_url = base_url
        self.training_data = AITrainingData(
            code_patterns=[],
            performance_metrics=[],
            optimization_results=[],
            user_interactions=[],
            preset_recommendations=[],
            adaptive_tuning_data=[],
            patch_generation_data=[],
            pattern_detection_data=[],
            chaos_enhancement_data=[],
            prediction_data=[],
            style_transfer_data=[],
        )

    def analyze_code_pattern(
        self, code: str, target: str, parallel: bool
    ) -> CodePattern:
        """Analyze code pattern for AI training"""
        return CodePattern(
            code=code,
            target=target,
            parallel=parallel,
            complexity=len(code.split("\n")),
            nested_level=code.count("[") + code.count("{"),
            functional_style="lambda" in code or "map" in code,
            mathematical_ops="**" in code or "pow" in code,
            data_processing="range" in code and "for" in code,
            scientific="numpy" in code or "scipy" in code,
            web_development="json" in code or "api" in code,
            concurrent="thread" in code or "async" in code,
            enterprise="class" in code or "interface" in code,
        )

    def collect_performance_metrics(
        self,
        latency: float,
        throughput: float,
        memory: float,
        cache_hit: float,
        success: float,
        error: float,
        fallback: float,
        degradation: float,
    ) -> PerformanceMetrics:
        """Collect performance metrics for AI training"""
        return PerformanceMetrics(
            latency_ms=latency,
            throughput_rps=throughput,
            memory_usage_mb=memory,
            cache_hit_rate=cache_hit,
            success_rate=success,
            error_rate=error,
            fallback_rate=fallback,
            degradation_rate=degradation,
        )

    def collect_optimization_result(
        self,
        original: str,
        optimized: str,
        opt_type: str,
        perf_improvement: float,
        memory_improvement: float,
        cache_improvement: float,
        parallel_speedup: float,
        unsafe_benefit: float,
    ) -> OptimizationResult:
        """Collect optimization result for AI training"""
        return OptimizationResult(
            original_code=original,
            optimized_code=optimized,
            optimization_type=opt_type,
            performance_improvement=perf_improvement,
            memory_improvement=memory_improvement,
            cache_improvement=cache_improvement,
            parallel_speedup=parallel_speedup,
            unsafe_benefit=unsafe_benefit,
        )

    def collect_user_interaction(
        self,
        action: str,
        parameters: dict[str, Any],
        satisfaction: float,
        performance_feedback: float,
        creativity_rating: float,
        learning_preference: str,
    ) -> UserInteraction:
        """Collect user interaction data for AI training"""
        return UserInteraction(
            timestamp=datetime.now(),
            user_action=action,
            parameters=parameters,
            result_satisfaction=satisfaction,
            performance_feedback=performance_feedback,
            creativity_rating=creativity_rating,
            learning_preference=learning_preference,
        )

    async def collect_stress_test_data(self, duration_minutes: int = 5) -> None:
        """Collect data from stress tests"""
        logger.info(f"Collecting stress test data for {duration_minutes} minutes...")

        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)

        while time.time() < end_time:
            try:
                # Generate random code patterns
                code_patterns = [
                    "[x ** 2 for x in range(100)]",
                    "[x * y for x in range(50) for y in range(50)]",
                    "[x for x in range(1000) if x % 2 == 0]",
                    "[str(x) + str(y) for x in range(100) for y in range(100)]",
                    "[x if x % 2 == 0 else y * 2 for x in range(200) for y in range(200)]",
                ]

                targets = ["rust", "ts", "go", "csharp", "sql", "julia"]

                for code in code_patterns:
                    for target in targets:
                        # Analyze code pattern
                        pattern = self.analyze_code_pattern(
                            code, target, random.choice([True, False])
                        )
                        self.training_data.code_patterns.append(pattern)

                        # Simulate performance metrics
                        metrics = self.collect_performance_metrics(
                            latency=random.uniform(5, 50),
                            throughput=random.uniform(10, 100),
                            memory=random.uniform(10, 100),
                            cache_hit=random.uniform(0.3, 0.9),
                            success=random.uniform(0.8, 1.0),
                            error=random.uniform(0.0, 0.2),
                            fallback=random.uniform(0.0, 0.3),
                            degradation=random.uniform(0.0, 0.1),
                        )
                        self.training_data.performance_metrics.append(metrics)

                        # Simulate optimization results
                        optimization = self.collect_optimization_result(
                            original=code,
                            optimized=code + " # optimized",
                            opt_type=random.choice(
                                ["parallel", "vectorization", "caching", "unsafe"]
                            ),
                            perf_improvement=random.uniform(0.1, 2.0),
                            memory_improvement=random.uniform(0.0, 0.5),
                            cache_improvement=random.uniform(0.0, 0.3),
                            parallel_speedup=random.uniform(1.0, 4.0),
                            unsafe_benefit=random.uniform(0.0, 0.4),
                        )
                        self.training_data.optimization_results.append(optimization)

                await asyncio.sleep(1)  # Collect data every second

            except Exception as e:
                logger.error(f"Error collecting stress test data: {e}")
                await asyncio.sleep(1)

        logger.info(
            f"Collected {len(self.training_data.code_patterns)} code patterns from stress test"
        )

    async def collect_benchmark_data(self, num_benchmarks: int = 100) -> None:
        """Collect data from benchmark runs"""
        logger.info(f"Collecting benchmark data for {num_benchmarks} benchmarks...")

        for i in range(num_benchmarks):
            try:
                # Generate benchmark scenarios
                scenarios = [
                    {
                        "name": "data_processing",
                        "code": "[x ** 2 for x in range(1000)]",
                        "target": "sql",
                    },
                    {
                        "name": "mathematical",
                        "code": "[x * y for x in range(100) for y in range(100)]",
                        "target": "rust",
                    },
                    {
                        "name": "scientific",
                        "code": "[x ** 3 + y ** 2 for x in range(50) for y in range(50)]",
                        "target": "julia",
                    },
                    {
                        "name": "web_development",
                        "code": "[str(x) for x in range(500)]",
                        "target": "ts",
                    },
                    {
                        "name": "concurrent",
                        "code": "[x + y for x in range(200) for y in range(200)]",
                        "target": "go",
                    },
                    {
                        "name": "enterprise",
                        "code": "[x * y * z for x in range(100) for y in range(100) for z in range(100)]",
                        "target": "csharp",
                    },
                ]

                scenario = random.choice(scenarios)

                # Collect preset recommendation data
                preset_rec = {
                    "scenario": scenario["name"],
                    "code": scenario["code"],
                    "target": scenario["target"],
                    "recommended_preset": random.choice(
                        [
                            "SQL Club Mix",
                            "Rust FM Synth",
                            "Julia Granular Synth",
                            "TypeScript Digital Synth",
                            "Go Analog Synth",
                            "C# PLINQ Synth",
                        ]
                    ),
                    "confidence": random.uniform(0.6, 0.95),
                    "reasoning": f"Detected {scenario['name']} pattern",
                }
                self.training_data.preset_recommendations.append(preset_rec)

                # Collect adaptive tuning data
                tuning_data = {
                    "scenario": scenario["name"],
                    "auto_tune_level": random.uniform(0.3, 0.9),
                    "learning_speed": random.uniform(0.4, 0.8),
                    "optimization_score": random.uniform(60, 95),
                    "suggestions": random.choice(
                        [
                            ["Consider parallel processing", "Enable vectorization"],
                            ["Add caching", "Optimize memory access"],
                            ["Enable unsafe optimizations", "Add bounds checking"],
                        ]
                    ),
                }
                self.training_data.adaptive_tuning_data.append(tuning_data)

                # Collect patch generation data
                patch_data = {
                    "scenario": scenario["name"],
                    "creativity": random.uniform(0.5, 0.9),
                    "chaos": random.uniform(0.2, 0.7),
                    "generated_patches": random.randint(1, 5),
                    "patch_types": random.choice(
                        [
                            ["Parallel Vectorization", "Chaos Optimization"],
                            ["Creative Transformation", "Performance Boost"],
                            ["Memory Optimization", "Cache Enhancement"],
                        ]
                    ),
                }
                self.training_data.patch_generation_data.append(patch_data)

                # Collect pattern detection data
                pattern_data = {
                    "scenario": scenario["name"],
                    "sensitivity": random.uniform(0.4, 0.9),
                    "alert_level": random.uniform(0.3, 0.8),
                    "detected_issues": random.randint(0, 3),
                    "suggested_fixes": random.choice(
                        [
                            ["Try constant folding", "Add predicate pushdown"],
                            ["Enable parallel processing", "Optimize data structures"],
                            ["Add caching layers", "Enable vectorization"],
                        ]
                    ),
                }
                self.training_data.pattern_detection_data.append(pattern_data)

                # Collect chaos enhancement data
                chaos_data = {
                    "scenario": scenario["name"],
                    "chaos_level": random.uniform(0.1, 0.8),
                    "glitch_mode": random.uniform(0.0, 0.5),
                    "enhancements": random.choice(
                        [
                            ["Add random noise", "Enable glitch effects"],
                            ["Generate chaotic transformations", "Add stress testing"],
                            ["Enable performance art mode", "Add creative chaos"],
                        ]
                    ),
                }
                self.training_data.chaos_enhancement_data.append(chaos_data)

                # Collect prediction data
                prediction_data = {
                    "scenario": scenario["name"],
                    "prediction_window": random.uniform(0.6, 0.95),
                    "accuracy": random.uniform(0.7, 0.95),
                    "predictions": random.choice(
                        [
                            [
                                "30ms latency spike if parallelism ramped",
                                "Memory usage will increase by 15%",
                            ],
                            [
                                "Cache hit rate will improve by 25%",
                                "Throughput will increase by 40%",
                            ],
                            [
                                "Performance will degrade by 20%",
                                "Optimization will improve by 35%",
                            ],
                        ]
                    ),
                }
                self.training_data.prediction_data.append(prediction_data)

                # Collect style transfer data
                style_data = {
                    "scenario": scenario["name"],
                    "source_target": scenario["target"],
                    "target_style": random.choice(
                        [
                            "SQL Club Mix",
                            "Rust FM Synth",
                            "Julia Granular Synth",
                            "TypeScript Digital Synth",
                            "Go Analog Synth",
                            "C# PLINQ Synth",
                        ]
                    ),
                    "style_strength": random.uniform(0.4, 0.9),
                    "creativity": random.uniform(0.5, 0.8),
                    "transformations": random.choice(
                        [
                            ["Optimize data structures", "Add type safety"],
                            [
                                "Enable parallel processing",
                                "Add performance optimizations",
                            ],
                            [
                                "Apply style-specific optimizations",
                                "Add backend-specific features",
                            ],
                        ]
                    ),
                }
                self.training_data.style_transfer_data.append(style_data)

                await asyncio.sleep(0.1)  # Small delay between benchmarks

            except Exception as e:
                logger.error(f"Error collecting benchmark data: {e}")
                await asyncio.sleep(0.1)

        logger.info(
            f"Collected {len(self.training_data.preset_recommendations)} benchmark scenarios"
        )

    async def collect_user_interaction_data(self, num_interactions: int = 50) -> None:
        """Collect user interaction data"""
        logger.info(
            f"Collecting user interaction data for {num_interactions} interactions..."
        )

        for i in range(num_interactions):
            try:
                # Simulate user interactions
                actions = [
                    "preset_selection",
                    "parameter_adjustment",
                    "optimization_toggle",
                    "chaos_enhancement",
                    "style_transfer",
                    "performance_prediction",
                    "pattern_detection",
                    "patch_generation",
                ]

                action = random.choice(actions)
                parameters = {
                    "target": random.choice(
                        ["rust", "ts", "go", "csharp", "sql", "julia"]
                    ),
                    "parallel": random.choice([True, False]),
                    "optimization_level": random.uniform(0.1, 0.9),
                    "creativity": random.uniform(0.3, 0.8),
                    "chaos": random.uniform(0.1, 0.6),
                }

                interaction = self.collect_user_interaction(
                    action=action,
                    parameters=parameters,
                    satisfaction=random.uniform(0.6, 1.0),
                    performance_feedback=random.uniform(0.5, 1.0),
                    creativity_rating=random.uniform(0.4, 0.9),
                    learning_preference=random.choice(
                        ["conservative", "aggressive", "creative", "balanced"]
                    ),
                )
                self.training_data.user_interactions.append(interaction)

                await asyncio.sleep(0.05)  # Small delay between interactions

            except Exception as e:
                logger.error(f"Error collecting user interaction data: {e}")
                await asyncio.sleep(0.05)

        logger.info(
            f"Collected {len(self.training_data.user_interactions)} user interactions"
        )

    def save_training_data(self, filename: str = "ai_training_data.json") -> None:
        """Save collected training data to file"""
        logger.info(f"Saving training data to {filename}...")

        # Convert dataclasses to dictionaries
        data_dict = {
            "code_patterns": [
                asdict(pattern) for pattern in self.training_data.code_patterns
            ],
            "performance_metrics": [
                asdict(metrics) for metrics in self.training_data.performance_metrics
            ],
            "optimization_results": [
                asdict(result) for result in self.training_data.optimization_results
            ],
            "user_interactions": [
                asdict(interaction)
                for interaction in self.training_data.user_interactions
            ],
            "preset_recommendations": self.training_data.preset_recommendations,
            "adaptive_tuning_data": self.training_data.adaptive_tuning_data,
            "patch_generation_data": self.training_data.patch_generation_data,
            "pattern_detection_data": self.training_data.pattern_detection_data,
            "chaos_enhancement_data": self.training_data.chaos_enhancement_data,
            "prediction_data": self.training_data.prediction_data,
            "style_transfer_data": self.training_data.style_transfer_data,
            "collection_timestamp": datetime.now().isoformat(),
            "total_records": len(self.training_data.code_patterns)
            + len(self.training_data.performance_metrics)
            + len(self.training_data.optimization_results)
            + len(self.training_data.user_interactions),
        }

        with open(filename, "w") as f:
            json.dump(data_dict, f, indent=2)

        logger.info(
            f"Saved {data_dict['total_records']} training records to {filename}"
        )

    async def run_data_collection(
        self,
        stress_duration: int = 5,
        num_benchmarks: int = 100,
        num_interactions: int = 50,
    ) -> None:
        """Run complete data collection process"""
        logger.info("Starting AI data collection process...")

        start_time = time.time()

        # Collect data from different sources
        await self.collect_stress_test_data(stress_duration)
        await self.collect_benchmark_data(num_benchmarks)
        await self.collect_user_interaction_data(num_interactions)

        # Save collected data
        self.save_training_data()

        end_time = time.time()
        duration = end_time - start_time

        logger.info(f"Data collection completed in {duration:.2f} seconds")
        logger.info(
            f"Total records collected: {len(self.training_data.code_patterns) + len(self.training_data.performance_metrics) + len(self.training_data.optimization_results) + len(self.training_data.user_interactions)}"
        )


async def main():
    """Main function to run data collection"""
    collector = AIDataCollector()

    # Run data collection
    await collector.run_data_collection(
        stress_duration=5,  # 5 minutes of stress test data
        num_benchmarks=100,  # 100 benchmark scenarios
        num_interactions=50,  # 50 user interactions
    )


if __name__ == "__main__":
    asyncio.run(main())
