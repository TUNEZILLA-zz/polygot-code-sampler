# 🎛️ Code Live - Pull Request Template

## What
<!-- Brief description of what this PR changes -->

## Why
<!-- Why is this change needed? What problem does it solve? -->

## Screens/Metrics
<!-- Include relevant screenshots, performance metrics, or test results -->
- [ ] Screenshots of UI changes (if applicable)
- [ ] Performance metrics before/after
- [ ] Test results and coverage
- [ ] Golden test results (if applicable)

## Rollback Plan
<!-- How to rollback if this causes issues -->
- [ ] Database migrations are reversible
- [ ] Feature flags can disable new functionality
- [ ] Clear rollback steps documented

## Risk Assessment
<!-- Check the appropriate risk level -->
- [ ] **Low Risk** - No breaking changes, backwards compatible
- [ ] **Medium Risk** - Some breaking changes with migration path
- [ ] **High Risk** - Major breaking changes, requires coordination

## Mitigations
<!-- What we're doing to reduce risk -->
- [ ] Feature flags for gradual rollout
- [ ] Comprehensive testing
- [ ] Monitoring and alerting
- [ ] Documentation updates

## Testing
<!-- Checklist of testing completed -->
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Golden tests pass
- [ ] Manual testing completed
- [ ] Performance testing (if applicable)
- [ ] Security testing (if applicable)

## Experiment Branch Specific
<!-- For experiment branches (fx-*) -->
- [ ] **Experiment Type**: [synth-modulation/lolcat-visuals/audio-reactive/etc.]
- [ ] **Demo Presets**: [List demo presets created]
- [ ] **Performance Impact**: [Any performance implications]
- [ ] **Accessibility**: [Accessibility considerations]
- [ ] **Browser Support**: [Browser compatibility tested]

## Documentation
<!-- Documentation updates needed -->
- [ ] README updated (if applicable)
- [ ] API documentation updated (if applicable)
- [ ] Code comments added
- [ ] Architecture decisions documented

## Dependencies
<!-- Any new dependencies or version changes -->
- [ ] New dependencies added
- [ ] Dependency versions updated
- [ ] Security audit completed for new dependencies

## Performance Impact
<!-- Performance considerations -->
- [ ] No performance regression
- [ ] Performance improvements documented
- [ ] Memory usage analyzed
- [ ] CPU usage analyzed

## Security
<!-- Security considerations -->
- [ ] No security vulnerabilities introduced
- [ ] Input validation added (if applicable)
- [ ] Authentication/authorization updated (if applicable)
- [ ] Secrets management reviewed (if applicable)

## Monitoring
<!-- Monitoring and observability -->
- [ ] New metrics added (if applicable)
- [ ] Alerts configured (if applicable)
- [ ] Logging added (if applicable)
- [ ] Dashboard updated (if applicable)

## Checklist for Reviewers
<!-- For reviewers to check -->
- [ ] Code follows project conventions
- [ ] Tests are comprehensive
- [ ] Documentation is clear
- [ ] Performance impact is acceptable
- [ ] Security considerations addressed
- [ ] Accessibility requirements met

---

**Labels**:
- `type:feature` / `type:bugfix` / `type:experiment` / `type:docs`
- `area:fx` / `area:backend` / `area:frontend` / `area:ops`
- `risk:low` / `risk:medium` / `risk:high`
- `ready-for-merge` (when ready)
