# Changelog

All notable changes to the Polyglot Code Sampler will be documented in this file.

## [Unreleased]

### Added
- **Central Renderer API**: Introduced `pcs.renderer_api` with automatic kwargs filtering
- **Type Safety**: Added `RendererFn` protocol for compile-time type checking
- **Pre-commit Hooks**: Added black, ruff, and mypy for code quality
- **CI/CD Matrix**: Added smoke tests across all backends
- **Golden Stability**: Added CI job to detect golden file changes

### Changed
- **Rust Exports**: Changed `fn` → `pub fn` for proper public function exports
- **TypeScript Exports**: Changed `function` → `export function` for proper module exports
- **CLI Integration**: Updated CLI to use central renderer API
- **Test Infrastructure**: All 52 tests now pass with zero signature mismatch errors

### Fixed
- **Signature Drift**: Eliminated `TypeError` exceptions from backend signature mismatches
- **Future-Proof**: Backend changes no longer break existing test infrastructure
- **Type Safety**: Added proper typing for all renderer functions

### Deprecated
- **Direct Backend Imports**: While still supported, recommend using `pcs.renderer_api.render()`

## [0.3.0] - 2025-09-26

### Added
- **Go Backend**: Complete implementation with parallel processing
- **Enterprise Platform**: Performance monitoring with policy-driven governance
- **Interactive Dashboard**: Real-time performance insights and trend analysis
- **Multi-Backend Benchmarks**: Comprehensive testing across 6 target languages
- **CI/CD Pipeline**: Automated regression detection and dashboard publishing

### Changed
- **Performance Monitoring**: Transformed from compiler demo to enterprise platform
- **Dashboard**: Enhanced with interactive charts and cross-backend comparisons
- **Testing**: Expanded test suite with golden file validation

## [0.2.0] - 2025-09-25

### Added
- **C# Backend**: LINQ implementation with PLINQ parallel support
- **Parallel Parity**: All 5 backends now support parallel processing
- **Showcase Charts**: Side-by-side Python → Rust → Go → TS → C# → SQL demos
- **Enterprise Angle**: Business logic comprehension examples

### Changed
- **Documentation**: Enhanced README with parallel processing examples
- **Performance**: Added comprehensive benchmarking across all backends

## [0.1.0] - 2025-09-24

### Added
- **Core IR**: Intermediate representation for Python comprehensions
- **Rust Backend**: Iterator chains with Rayon parallel support
- **TypeScript Backend**: Functional array methods with Web Workers
- **SQL Backend**: Query generation with dialect support
- **Go Backend**: Goroutines and channels for parallel processing
- **Julia Backend**: Loop and broadcast modes with thread safety
- **CLI Interface**: Command-line tool for all backends
- **Test Suite**: Comprehensive golden file testing
- **Performance Benchmarks**: Multi-backend performance monitoring

