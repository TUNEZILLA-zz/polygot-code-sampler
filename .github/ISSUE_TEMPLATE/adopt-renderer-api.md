---
name: Adopt Central Renderer API
about: Track migration from direct backend imports to central renderer API
title: "[MIGRATION] Adopt renderer_api.render(...) in examples/tests"
labels: ["migration", "enhancement", "good first issue"]
assignees: []
---

## 🎯 **Migration Goal**

Migrate from direct backend imports to the central `renderer_api.render()` function for better maintainability and signature drift protection.

## 📋 **Current State**

- ✅ Central renderer API implemented (`pcs.renderer_api`)
- ✅ CLI updated to use central API
- ✅ Legacy re-exports working for backward compatibility
- ✅ All 59 tests passing

## 🔄 **Migration Tasks**

### **High Priority**
- [ ] Update all examples in `docs/` to use `renderer_api.render()`
- [ ] Update test files that import directly from `pcs.renderers.*`
- [ ] Update README code snippets to show central API usage

### **Medium Priority**
- [ ] Update any remaining direct imports in `pcs_step3_ts.py`
- [ ] Update benchmark scripts to use central API
- [ ] Update documentation in `docs/RENDERER_API.md`

### **Low Priority**
- [ ] Add deprecation warnings to direct imports (future)
- [ ] Remove legacy re-exports (future major version)

## 🧪 **Testing**

After migration, verify:
- [ ] All tests still pass
- [ ] Examples work correctly
- [ ] No signature mismatch errors
- [ ] Performance benchmarks unaffected

## 📚 **Reference**

See `docs/RENDERER_API.md` for:
- Usage examples
- Migration guide
- Backend-specific parameters
- Error handling

## 🎉 **Benefits**

- **Zero Signature Drift**: Automatic kwargs filtering
- **Future-Proof**: New backend flags won't break code
- **Type Safety**: Compile-time type checking
- **Consistent Interface**: Same API for all backends
