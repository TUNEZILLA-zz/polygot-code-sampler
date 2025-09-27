#!/usr/bin/env python3
"""
🎛️ Code Live - Vintage Profiles Engine
=====================================

Like SP-1200 / MPC60 for compilers/runtimes - time machine for code generation.
Applies vintage constraints to create "period-correct" code patterns.
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


class VintageEra(Enum):
    """Vintage computing eras"""

    MODERN = "modern"
    MPC60 = "mpc60"  # 1990s vibe
    SP1200 = "sp1200"  # Crunchy 80s
    MPC2000XL = "mpc2000xl"  # Early 2000s
    Y2K_WEB = "y2k_web"  # IE6 era
    POSTGRES_92 = "postgres_92"  # Pre-window SQL
    GO_PRE_MODULES = "go_pre_modules"  # Go 1.10
    JULIA_PRE_BROADCAST = "julia_pre_broadcast"  # Julia 0.6


@dataclass
class VintageConstraints:
    """Constraints for a specific language in a vintage profile"""

    toolchain: Optional[str] = None
    edition: Optional[str] = None
    target: Optional[str] = None
    version: Optional[str] = None
    dialect: Optional[str] = None
    features_off: List[str] = None
    opts: List[str] = None
    idioms: List[str] = None
    degraders: List[str] = None
    polyfills: List[str] = None
    transpile: bool = False

    def __post_init__(self):
        if self.features_off is None:
            self.features_off = []
        if self.opts is None:
            self.opts = []
        if self.idioms is None:
            self.idioms = []
        if self.degraders is None:
            self.degraders = []
        if self.polyfills is None:
            self.polyfills = []


@dataclass
class GlobalDegraders:
    """Global performance degraders for vintage feel"""

    bit_depth: int = 32
    sample_rate: int = 44100
    buffer_size: int = 4096
    noise_floor: float = 0.0


@dataclass
class VintageProfile:
    """Complete vintage profile configuration"""

    label: str
    description: str
    global_degraders: GlobalDegraders
    rust: VintageConstraints
    typescript: VintageConstraints
    go: VintageConstraints
    julia: VintageConstraints
    sql: VintageConstraints

    def get_constraints_for_language(self, language: str) -> VintageConstraints:
        """Get constraints for a specific language"""
        constraints_map = {
            "rust": self.rust,
            "typescript": self.typescript,
            "go": self.go,
            "julia": self.julia,
            "sql": self.sql,
        }
        return constraints_map.get(language, VintageConstraints())


class VintageProfileEngine:
    """Engine for applying vintage profiles to code generation"""

    def __init__(self, config_path: str = "bench/vintage.yml"):
        self.config_path = Path(config_path)
        self.profiles: Dict[str, VintageProfile] = {}
        self.capabilities: Dict[str, Dict[str, List[str]]] = {}
        self.load_config()

    def load_config(self):
        """Load vintage profiles configuration"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Vintage config not found: {self.config_path}")

        with open(self.config_path) as f:
            config = yaml.safe_load(f)

        # Load profiles
        for profile_name, profile_data in config.get("profiles", {}).items():
            self.profiles[profile_name] = self._parse_profile(
                profile_name, profile_data
            )

        # Load capabilities matrix
        self.capabilities = config.get("capabilities", {})

    def _parse_profile(self, name: str, data: Dict[str, Any]) -> VintageProfile:
        """Parse a profile from configuration data"""

        # Parse global degraders
        global_degraders_data = data.get("global_degraders", {})
        global_degraders = GlobalDegraders(
            bit_depth=global_degraders_data.get("bit_depth", 32),
            sample_rate=global_degraders_data.get("sample_rate", 44100),
            buffer_size=global_degraders_data.get("buffer_size", 4096),
            noise_floor=global_degraders_data.get("noise_floor", 0.0),
        )

        # Parse language-specific constraints
        rust = self._parse_constraints(data.get("rust", {}))
        typescript = self._parse_constraints(data.get("typescript", {}))
        go = self._parse_constraints(data.get("go", {}))
        julia = self._parse_constraints(data.get("julia", {}))
        sql = self._parse_constraints(data.get("sql", {}))

        return VintageProfile(
            label=data.get("label", name),
            description=data.get("description", ""),
            global_degraders=global_degraders,
            rust=rust,
            typescript=typescript,
            go=go,
            julia=julia,
            sql=sql,
        )

    def _parse_constraints(self, data: Dict[str, Any]) -> VintageConstraints:
        """Parse constraints for a specific language"""
        return VintageConstraints(
            toolchain=data.get("toolchain"),
            edition=data.get("edition"),
            target=data.get("target"),
            version=data.get("version"),
            dialect=data.get("dialect"),
            features_off=data.get("features_off", []),
            opts=data.get("opts", []),
            idioms=data.get("idioms", []),
            degraders=data.get("degraders", []),
            polyfills=data.get("polyfills", []),
            transpile=data.get("transpile", False),
        )

    def get_profile(self, profile_name: str) -> Optional[VintageProfile]:
        """Get a vintage profile by name"""
        return self.profiles.get(profile_name)

    def list_profiles(self) -> List[str]:
        """List all available vintage profiles"""
        return list(self.profiles.keys())

    def apply_vintage_constraints(
        self, code: str, language: str, profile_name: str
    ) -> str:
        """Apply vintage constraints to generated code"""
        profile = self.get_profile(profile_name)
        if not profile:
            return code

        constraints = profile.get_constraints_for_language(language)
        if not constraints:
            return code

        # Apply language-specific transformations
        if language == "typescript":
            return self._apply_typescript_vintage(code, constraints)
        elif language == "rust":
            return self._apply_rust_vintage(code, constraints)
        elif language == "go":
            return self._apply_go_vintage(code, constraints)
        elif language == "julia":
            return self._apply_julia_vintage(code, constraints)
        elif language == "sql":
            return self._apply_sql_vintage(code, constraints)

        return code

    def _apply_typescript_vintage(
        self, code: str, constraints: VintageConstraints
    ) -> str:
        """Apply TypeScript vintage constraints"""
        vintage_code = code

        # Remove async/await if forbidden
        if "async_await" in constraints.features_off:
            vintage_code = self._remove_async_await(vintage_code)

        # Remove arrow functions if forbidden
        if "arrow_functions" in constraints.features_off:
            vintage_code = self._remove_arrow_functions(vintage_code)

        # Remove const/let if forbidden
        if "const_let" in constraints.features_off:
            vintage_code = self._replace_const_let_with_var(vintage_code)

        # Remove template literals if forbidden
        if "template_literals" in constraints.features_off:
            vintage_code = self._remove_template_literals(vintage_code)

        # Remove classes if forbidden
        if "no_classes" in constraints.idioms:
            vintage_code = self._remove_classes(vintage_code)

        # Apply manual loops if required
        if "manual_loops" in constraints.idioms:
            vintage_code = self._convert_to_manual_loops(vintage_code)

        return vintage_code

    def _apply_rust_vintage(self, code: str, constraints: VintageConstraints) -> str:
        """Apply Rust vintage constraints"""
        vintage_code = code

        # Remove iterators if forbidden
        if "no_iterators" in constraints.idioms:
            vintage_code = self._remove_rust_iterators(vintage_code)

        # Convert to manual loops if required
        if "for_loops_only" in constraints.idioms:
            vintage_code = self._convert_rust_to_manual_loops(vintage_code)

        # Remove SIMD if forbidden
        if "no_simd" in constraints.degraders:
            vintage_code = self._remove_rust_simd(vintage_code)

        return vintage_code

    def _apply_go_vintage(self, code: str, constraints: VintageConstraints) -> str:
        """Apply Go vintage constraints"""
        vintage_code = code

        # Remove goroutines if forbidden
        if "no_goroutines" in constraints.degraders:
            vintage_code = self._remove_go_goroutines(vintage_code)

        # Convert to manual slices if required
        if "manual_slices" in constraints.idioms:
            vintage_code = self._convert_go_to_manual_slices(vintage_code)

        return vintage_code

    def _apply_julia_vintage(self, code: str, constraints: VintageConstraints) -> str:
        """Apply Julia vintage constraints"""
        vintage_code = code

        # Remove broadcast if forbidden
        if "broadcast" in constraints.features_off:
            vintage_code = self._remove_julia_broadcast(vintage_code)

        # Remove dot syntax if forbidden
        if "no_dot_syntax" in constraints.idioms:
            vintage_code = self._remove_julia_dot_syntax(vintage_code)

        # Convert to manual loops if required
        if "for_loops" in constraints.idioms:
            vintage_code = self._convert_julia_to_manual_loops(vintage_code)

        return vintage_code

    def _apply_sql_vintage(self, code: str, constraints: VintageConstraints) -> str:
        """Apply SQL vintage constraints"""
        vintage_code = code

        # Remove window functions if forbidden
        if "window_functions" in constraints.features_off:
            vintage_code = self._remove_sql_window_functions(vintage_code)

        # Remove CTEs if forbidden
        if "cte" in constraints.features_off:
            vintage_code = self._remove_sql_cte(vintage_code)

        # Convert to manual joins if required
        if "manual_joins" in constraints.idioms:
            vintage_code = self._convert_sql_to_manual_joins(vintage_code)

        return vintage_code

    # TypeScript vintage transformations
    def _remove_async_await(self, code: str) -> str:
        """Remove async/await and convert to Promise chains"""
        # This is a simplified example - in practice, you'd use AST transformation
        code = code.replace("async ", "")
        code = code.replace("await ", "")
        return code

    def _remove_arrow_functions(self, code: str) -> str:
        """Remove arrow functions and convert to function expressions"""
        # Simplified example - would need proper AST parsing
        return code

    def _replace_const_let_with_var(self, code: str) -> str:
        """Replace const/let with var"""
        code = code.replace("const ", "var ")
        code = code.replace("let ", "var ")
        return code

    def _remove_template_literals(self, code: str) -> str:
        """Remove template literals and convert to string concatenation"""
        # Simplified example
        return code

    def _remove_classes(self, code: str) -> str:
        """Remove ES6 classes"""
        # Simplified example
        return code

    def _convert_to_manual_loops(self, code: str) -> str:
        """Convert array methods to manual loops"""
        # Simplified example
        return code

    # Rust vintage transformations
    def _remove_rust_iterators(self, code: str) -> str:
        """Remove Rust iterators"""
        return code

    def _convert_rust_to_manual_loops(self, code: str) -> str:
        """Convert Rust iterators to manual loops"""
        return code

    def _remove_rust_simd(self, code: str) -> str:
        """Remove Rust SIMD"""
        return code

    # Go vintage transformations
    def _remove_go_goroutines(self, code: str) -> str:
        """Remove Go goroutines"""
        return code

    def _convert_go_to_manual_slices(self, code: str) -> str:
        """Convert Go slices to manual arrays"""
        return code

    # Julia vintage transformations
    def _remove_julia_broadcast(self, code: str) -> str:
        """Remove Julia broadcast"""
        return code

    def _remove_julia_dot_syntax(self, code: str) -> str:
        """Remove Julia dot syntax"""
        return code

    def _convert_julia_to_manual_loops(self, code: str) -> str:
        """Convert Julia to manual loops"""
        return code

    # SQL vintage transformations
    def _remove_sql_window_functions(self, code: str) -> str:
        """Remove SQL window functions"""
        return code

    def _remove_sql_cte(self, code: str) -> str:
        """Remove SQL CTEs"""
        return code

    def _convert_sql_to_manual_joins(self, code: str) -> str:
        """Convert SQL to manual joins"""
        return code

    def get_vintage_compiler_flags(self, language: str, profile_name: str) -> List[str]:
        """Get compiler flags for vintage profile"""
        profile = self.get_profile(profile_name)
        if not profile:
            return []

        constraints = profile.get_constraints_for_language(language)
        if not constraints:
            return []

        return constraints.opts

    def get_vintage_toolchain(self, language: str, profile_name: str) -> Optional[str]:
        """Get toolchain version for vintage profile"""
        profile = self.get_profile(profile_name)
        if not profile:
            return None

        constraints = profile.get_constraints_for_language(language)
        if not constraints:
            return None

        return constraints.toolchain or constraints.version

    def get_vintage_degraders(self, profile_name: str) -> GlobalDegraders:
        """Get global degraders for vintage profile"""
        profile = self.get_profile(profile_name)
        if not profile:
            return GlobalDegraders()

        return profile.global_degraders

    def validate_vintage_compatibility(
        self, code: str, language: str, profile_name: str
    ) -> Tuple[bool, List[str]]:
        """Validate if code is compatible with vintage profile"""
        profile = self.get_profile(profile_name)
        if not profile:
            return True, []

        constraints = profile.get_constraints_for_language(language)
        if not constraints:
            return True, []

        issues = []

        # Check for forbidden features
        for feature in constraints.features_off:
            if self._code_contains_feature(code, language, feature):
                issues.append(f"Forbidden feature detected: {feature}")

        # Check for required idioms
        for idiom in constraints.idioms:
            if not self._code_follows_idiom(code, language, idiom):
                issues.append(f"Required idiom not followed: {idiom}")

        return len(issues) == 0, issues

    def _code_contains_feature(self, code: str, language: str, feature: str) -> bool:
        """Check if code contains a specific feature"""
        # Simplified feature detection - would need proper AST parsing
        feature_patterns = {
            "async_await": ["async ", "await "],
            "arrow_functions": ["=>"],
            "const_let": ["const ", "let "],
            "template_literals": ["`"],
            "classes": ["class "],
            "window_functions": ["OVER (", "PARTITION BY"],
            "cte": ["WITH "],
            "broadcast": ["."],
            "dot_syntax": ["."],
            "iterators": [".iter()", ".map(", ".filter("],
            "goroutines": ["go "],
            "simd": ["simd", "SIMD"],
        }

        patterns = feature_patterns.get(feature, [])
        return any(pattern in code for pattern in patterns)

    def _code_follows_idiom(self, code: str, language: str, idiom: str) -> bool:
        """Check if code follows a specific idiom"""
        # Simplified idiom checking - would need proper AST parsing
        idiom_patterns = {
            "manual_loops": ["for (", "while (", "for i in"],
            "for_loops_only": ["for (", "while (", "for i in"],
            "var_declarations": ["var "],
            "function_expressions": ["function "],
            "no_classes": ["class "],
            "manual_joins": ["JOIN ", "INNER JOIN", "LEFT JOIN"],
            "for_loops": ["for ", "while "],
            "manual_arrays": ["Array(", "new Array"],
        }

        patterns = idiom_patterns.get(idiom, [])
        return any(pattern in code for pattern in patterns)


def main():
    """Test the vintage profiles engine"""
    engine = VintageProfileEngine()

    print("🎛️ Code Live - Vintage Profiles Engine")
    print("=" * 50)

    print("\n📋 Available Profiles:")
    for profile_name in engine.list_profiles():
        profile = engine.get_profile(profile_name)
        print(f"  {profile_name}: {profile.label}")
        print(f"    {profile.description}")

    print("\n🧪 Testing Vintage Constraints:")

    # Test TypeScript ES5 conversion
    modern_ts = """
    export async function sumEvens(n: number): Promise<number> {
      const xs = Array.from({length: n}, (_, i) => i);
      return xs.filter(x => x % 2 === 0).reduce((a,b) => a+b*b, 0);
    }
    """

    vintage_ts = engine.apply_vintage_constraints(modern_ts, "typescript", "mpc60")
    print("\nTypeScript MPC60 conversion:")
    print(f"Original: {modern_ts.strip()}")
    print(f"Vintage:  {vintage_ts.strip()}")

    # Test Rust 2015 conversion
    modern_rust = """
    pub fn sum_evens(n: usize) -> i64 {
        (0..n).into_par_iter().filter(|x| x % 2 == 0).map(|x| (x*x) as i64).sum()
    }
    """

    vintage_rust = engine.apply_vintage_constraints(modern_rust, "rust", "sp1200")
    print("\nRust SP1200 conversion:")
    print(f"Original: {modern_rust.strip()}")
    print(f"Vintage:  {vintage_rust.strip()}")

    print("\n🎉 Vintage Profiles Engine Ready!")


if __name__ == "__main__":
    main()
