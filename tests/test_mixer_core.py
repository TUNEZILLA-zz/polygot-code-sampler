# tests/test_mixer_core.py - Unit tests for mixer core functionality

import pytest
from mixer_core import *


class TestInterpolation:
    def test_lerp(self):
        assert lerp(0, 10, 0.5) == 5
        assert lerp(0, 10, 0.0) == 0
        assert lerp(0, 10, 1.0) == 10
        assert lerp(5, 15, 0.2) == 7

    def test_ease_in_out(self):
        assert easeInOut(0.0) == 0.0
        assert easeInOut(1.0) == 1.0
        assert easeInOut(0.5) == 0.5
        # Should be smooth curve
        assert 0 < easeInOut(0.25) < 0.5
        assert 0.5 < easeInOut(0.75) < 1.0

    def test_ramps(self):
        assert ramps.linear(0.5) == 0.5
        assert ramps.exp(0.5) < 0.5  # Should be steeper
        assert ramps.s(0.5) == 0.5  # Should be smooth

    def test_interp_state(self):
        keyframe_a = Keyframe(
            t=0,
            state=MixerState(
                faders={"rust": 0.2, "julia": 0.3},
                macros={"performance": 0.4},
                flags={"parallel": False},
            ),
        )
        keyframe_b = Keyframe(
            t=100,
            state=MixerState(
                faders={"rust": 0.8, "julia": 0.7},
                macros={"performance": 0.9},
                flags={"parallel": True},
            ),
        )

        # Test interpolation at midpoint
        result = interpState(keyframe_a, keyframe_b, 50)
        assert 0.2 < result.faders["rust"] < 0.8
        assert 0.3 < result.faders["julia"] < 0.7
        assert 0.4 < result.macros["performance"] < 0.9
        # Flags should switch at 0.5
        assert result.flags["parallel"] == True


class TestQuantization:
    def test_quantize_time(self):
        assert quantize(150, 100) == 100
        assert quantize(250, 100) == 200
        assert quantize(75, 100) == 100

    def test_quantize_to_grid(self):
        assert quantizeToGrid(0.23, 0.25) == 0.25
        assert quantizeToGrid(0.12, 0.25) == 0.0
        assert quantizeToGrid(0.37, 0.25) == 0.25
        assert quantizeToGrid(0.62, 0.25) == 0.75


class TestSoloLogic:
    def test_no_solo(self):
        tracks = {"rust": 0.5, "julia": 0.3, "sql": 0.7}
        soloed = {"rust": False, "julia": False, "sql": False}

        result = applySoloLogic(tracks, soloed)
        assert result["rust"] == True
        assert result["julia"] == True
        assert result["sql"] == True

    def test_solo_active(self):
        tracks = {"rust": 0.5, "julia": 0.3, "sql": 0.7}
        soloed = {"rust": False, "julia": True, "sql": False}

        result = applySoloLogic(tracks, soloed)
        assert result["rust"] == False
        assert result["julia"] == True
        assert result["sql"] == False

    def test_multiple_solo(self):
        tracks = {"rust": 0.5, "julia": 0.3, "sql": 0.7}
        soloed = {"rust": True, "julia": True, "sql": False}

        result = applySoloLogic(tracks, soloed)
        assert result["rust"] == True
        assert result["julia"] == True
        assert result["sql"] == False


class TestSidechainRules:
    def test_apply_rule_gt(self):
        rule = Rule(
            when=Metric(path="rust.gen_ms", op=">", value=25),
            then=Action(target="julia.level", delta=-0.15),
        )
        metrics = {"rust": {"gen_ms": 30}}
        state = MixerState(faders={"julia": 0.8}, macros={}, flags={})

        result = applyRule(rule, metrics, state)
        assert result.faders["julia"] == 0.65  # 0.8 - 0.15

    def test_apply_rule_lt(self):
        rule = Rule(
            when=Metric(path="sql.rows", op="<", value=100),
            then=Action(target="rust.level", delta=0.2),
        )
        metrics = {"sql": {"rows": 50}}
        state = MixerState(faders={"rust": 0.3}, macros={}, flags={})

        result = applyRule(rule, metrics, state)
        assert result.faders["rust"] == 0.5  # 0.3 + 0.2

    def test_apply_rule_condition_not_met(self):
        rule = Rule(
            when=Metric(path="rust.gen_ms", op=">", value=25),
            then=Action(target="julia.level", delta=-0.15),
        )
        metrics = {"rust": {"gen_ms": 20}}
        state = MixerState(faders={"julia": 0.8}, macros={}, flags={})

        result = applyRule(rule, metrics, state)
        assert result.faders["julia"] == 0.8  # No change

    def test_apply_rules_multiple(self):
        rules = [
            Rule(
                when=Metric(path="rust.gen_ms", op=">", value=25),
                then=Action(target="julia.level", delta=-0.15),
            ),
            Rule(
                when=Metric(path="sql.rows", op="<", value=100),
                then=Action(target="rust.level", delta=0.2),
            ),
        ]
        metrics = {"rust": {"gen_ms": 30}, "sql": {"rows": 50}}
        state = MixerState(faders={"julia": 0.8, "rust": 0.3}, macros={}, flags={})

        result = applyRules(rules, metrics, state)
        assert result.faders["julia"] == 0.65  # 0.8 - 0.15
        assert result.faders["rust"] == 0.5  # 0.3 + 0.2


class TestMidiMapping:
    def test_apply_midi_macro(self):
        midi_map = [MidiMap(cc=1, target="macros.performance")]
        cc = 1
        value = 64  # 50% of 127

        state = MixerState(faders={}, macros={"performance": 0.0}, flags={})

        result = applyMidiMap(midi_map, cc, value, state)
        assert result.macros["performance"] == 0.5  # 64/127 ≈ 0.5

    def test_apply_midi_fader(self):
        midi_map = [MidiMap(cc=2, target="rust.level")]
        cc = 2
        value = 127  # 100%

        state = MixerState(faders={"rust": 0.0}, macros={}, flags={})

        result = applyMidiMap(midi_map, cc, value, state)
        assert result.faders["rust"] == 1.0  # 127/127 = 1.0

    def test_apply_midi_no_match(self):
        midi_map = [MidiMap(cc=1, target="macros.performance")]
        cc = 2  # Different CC
        value = 64

        state = MixerState(faders={}, macros={"performance": 0.0}, flags={})

        result = applyMidiMap(midi_map, cc, value, state)
        assert result.macros["performance"] == 0.0  # No change


class TestPresetManagement:
    def test_export_preset(self):
        state = MixerState(
            faders={"rust": 0.8, "julia": 0.6},
            macros={"performance": 0.9},
            flags={"parallel": True},
        )

        preset = exportPreset("Test Preset", state, "Test notes")
        assert preset.name == "Test Preset"
        assert preset.state == state
        assert preset.notes == "Test notes"
        assert preset.version == "1.0"

    def test_import_preset(self):
        state = MixerState(
            faders={"rust": 0.8, "julia": 0.6},
            macros={"performance": 0.9},
            flags={"parallel": True},
        )

        preset = Preset(
            version="1.0", name="Test Preset", state=state, notes="Test notes"
        )

        imported_state = importPreset(preset)
        assert imported_state == state

    def test_import_preset_wrong_version(self):
        preset = Preset(version="2.0", name="Test Preset", state={}, notes="Test notes")

        with pytest.raises(ValueError, match="Unsupported preset version"):
            importPreset(preset)


class TestGlitchMode:
    def test_apply_glitch(self):
        state = MixerState(
            faders={"rust": 0.5, "julia": 0.3},
            macros={"performance": 0.7},
            flags={"parallel": True},
        )

        # Use seed for deterministic testing
        glitched = applyGlitch(state, intensity=0.2, seed=12345)

        # Values should be different but within bounds
        assert 0 <= glitched.faders["rust"] <= 1
        assert 0 <= glitched.faders["julia"] <= 1
        assert 0 <= glitched.macros["performance"] <= 1
        assert glitched.flags == state.flags  # Flags shouldn't change

    def test_apply_glitch_same_seed(self):
        state = MixerState(faders={"rust": 0.5}, macros={}, flags={})

        glitched1 = applyGlitch(state, intensity=0.2, seed=12345)
        glitched2 = applyGlitch(state, intensity=0.2, seed=12345)

        # Same seed should produce same result
        assert glitched1.faders["rust"] == glitched2.faders["rust"]


class TestABCompare:
    def test_create_ab_compare(self):
        state = MixerState(faders={"rust": 0.5}, macros={}, flags={})

        ab = createABCompare(state)
        assert ab.a == state
        assert ab.b == state
        assert ab.active == "a"

    def test_toggle_ab(self):
        state = MixerState(faders={"rust": 0.5}, macros={}, flags={})

        ab = createABCompare(state)
        assert ab.active == "a"

        toggled = toggleAB(ab)
        assert toggled.active == "b"

        toggled_again = toggleAB(toggled)
        assert toggled_again.active == "a"

    def test_get_active_state(self):
        state_a = MixerState(faders={"rust": 0.5}, macros={}, flags={})
        state_b = MixerState(faders={"rust": 0.8}, macros={}, flags={})

        ab = ABCompare(a=state_a, b=state_b, active="a")
        assert getActiveState(ab) == state_a

        ab.active = "b"
        assert getActiveState(ab) == state_b


class TestUtilities:
    def test_clamp(self):
        assert clamp(0.5) == 0.5
        assert clamp(1.5) == 1.0
        assert clamp(-0.5) == 0.0
        assert clamp(0.5, 0, 2) == 0.5
        assert clamp(1.5, 0, 2) == 1.5
        assert clamp(2.5, 0, 2) == 2.0

    def test_round_to_precision(self):
        assert roundToPrecision(0.123456, 2) == 0.12
        assert roundToPrecision(0.123456, 3) == 0.123
        assert roundToPrecision(0.123456, 0) == 0.0

    def test_debounce(self):
        call_count = 0

        def test_func():
            nonlocal call_count
            call_count += 1

        debounced = debounce(test_func, 100)

        # Call multiple times quickly
        debounced()
        debounced()
        debounced()

        # Should only call once after delay
        import time

        time.sleep(0.15)
        assert call_count == 1


class TestProjectManagement:
    def test_create_project(self):
        project = createProject("print('hello')")
        assert project.python_source == "print('hello')"
        assert project.project_version == "1.0"
        assert project.clips == []
        assert project.keyframes == []
        assert project.rules == []
        assert project.midi_map == []
        assert project.history == []

    def test_add_to_history(self):
        project = createProject("print('hello')")
        state = MixerState(faders={"rust": 0.5}, macros={}, flags={})

        updated = addToHistory(project, state)
        assert len(updated.history) == 1
        assert updated.history[0] == state

    def test_undo(self):
        project = createProject("print('hello')")
        state1 = MixerState(faders={"rust": 0.5}, macros={}, flags={})
        state2 = MixerState(faders={"rust": 0.8}, macros={}, flags={})

        project = addToHistory(project, state1)
        project = addToHistory(project, state2)
        assert len(project.history) == 2

        undone = undo(project)
        assert undone is not None
        assert len(undone.history) == 1
        assert undone.history[0] == state1

    def test_undo_empty_history(self):
        project = createProject("print('hello')")
        assert undo(project) is None

    def test_history_limit(self):
        project = createProject("print('hello')")

        # Add 12 states (more than limit of 10)
        for i in range(12):
            state = MixerState(faders={"rust": i / 10}, macros={}, flags={})
            project = addToHistory(project, state)

        assert len(project.history) == 10  # Should be limited
        assert project.history[0].faders["rust"] == 0.2  # First 2 should be dropped
        assert project.history[-1].faders["rust"] == 1.1  # Last should be newest


if __name__ == "__main__":
    pytest.main([__file__])
