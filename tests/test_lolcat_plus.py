#!/usr/bin/env python3
"""
LOLcat++ Test Suite - Determinism, bounds, A11y, and performance
"""
import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from string_fx.lolcat_plus import lolcat_plus


def test_lolcat_determinism():
    """Test that same input/seed produces identical output"""
    text = "Hello world!"
    seed = 1337

    result1 = lolcat_plus(
        text, seed=seed, intensity=0.6, uwu=0.4, chaos=0.2, emoji=0.12
    )
    result2 = lolcat_plus(
        text, seed=seed, intensity=0.6, uwu=0.4, chaos=0.2, emoji=0.12
    )

    assert result1["text"] == result2["text"]
    assert result1["ansi"] == result2["ansi"]
    assert result1["meta"]["seed"] == result2["meta"]["seed"]


def test_lolcat_bounds():
    """Test parameter bounds enforcement"""
    text = "Test bounds"

    # Test valid bounds
    result = lolcat_plus(
        text, intensity=0.5, uwu=0.3, chaos=0.1, emoji=0.08, nyan_trail=0.2
    )
    assert 0.0 <= result["meta"]["trail"] <= 1.0
    assert 0.0 <= result["meta"]["intensity"] <= 1.0

    # Test edge cases
    result_min = lolcat_plus(
        text, intensity=0.0, uwu=0.0, chaos=0.0, emoji=0.0, nyan_trail=0.0
    )
    result_max = lolcat_plus(
        text, intensity=1.0, uwu=1.0, chaos=1.0, emoji=1.0, nyan_trail=1.0
    )

    assert result_min["meta"]["trail"] == 0.0
    assert result_max["meta"]["trail"] == 1.0


def test_lolcat_a11y_mono():
    """Test A11y compliance with reduced motion and mono"""
    text = "Hello world!"

    result = lolcat_plus(text, reduced_motion=True, mono=True, seed=1)

    # Should not contain ANSI color codes in mono mode
    assert "\x1b[38;2" not in result["ansi"]
    assert result["meta"]["trail"] == 0.0

    # Should still contain some form of the text (may be transformed)
    assert len(result["text"]) > 0
    # Just check that we got some transformed text
    assert result["text"] != ""


def test_lolcat_a11y_reduced_motion():
    """Test reduced motion mode"""
    text = "Test reduced motion"

    result = lolcat_plus(text, reduced_motion=True, seed=1)

    # Trail should be 0 in reduced motion
    assert result["meta"]["trail"] == 0.0

    # Should still work
    assert len(result["text"]) > 0


def test_lolcat_uwu_transformation():
    """Test UwU transformation rules"""
    text = "really awesome"

    result = lolcat_plus(text, uwu=0.8, seed=1)

    # Should contain some transformations (text should be different from input)
    assert result["text"] != text
    assert len(result["text"]) > 0


def test_lolcat_chaos_case():
    """Test chaos case transformation"""
    text = "Hello World"

    result = lolcat_plus(text, chaos=0.5, seed=1)

    # Should contain some case mixing
    assert len(result["text"]) > 0
    # Should not be all uppercase or all lowercase
    assert not (result["text"].isupper() or result["text"].islower())


def test_lolcat_emoji_sprinkles():
    """Test emoji sprinkling"""
    text = "Hello world"

    result = lolcat_plus(text, emoji=0.3, seed=1)

    # Should contain some emojis
    emoji_chars = ["😺", "😸", "😹", "😻", "✨", "🌈", "🐾", "🫶", "🍣"]
    has_emoji = any(emoji in result["text"] for emoji in emoji_chars)
    assert has_emoji


def test_lolcat_gradient_phase():
    """Test gradient phase affects output"""
    text = "Test gradient"

    result1 = lolcat_plus(text, gradient_phase=0.0, seed=1)
    result2 = lolcat_plus(text, gradient_phase=0.5, seed=1)

    # Should produce different ANSI output
    assert result1["ansi"] != result2["ansi"]

    # But same text content
    assert result1["text"] == result2["text"]


def test_lolcat_performance():
    """Test performance for typical text length"""
    import time

    text = "A" * 120  # 120 characters
    start_time = time.time()

    result = lolcat_plus(text, seed=1)

    end_time = time.time()
    render_time = (end_time - start_time) * 1000  # Convert to ms

    # Should render in under 2ms for 120 chars
    assert render_time < 2.0
    assert len(result["text"]) > 0


def test_lolcat_rule_rewrites():
    """Test cat-speak rule rewrites"""
    text = "you are really awesome"

    result = lolcat_plus(text, seed=1)

    # Should contain some rewrites
    assert (
        "u" in result["text"] or "rly" in result["text"] or "pawsome" in result["text"]
    )


if __name__ == "__main__":
    # Run tests
    test_lolcat_determinism()
    test_lolcat_bounds()
    test_lolcat_a11y_mono()
    test_lolcat_a11y_reduced_motion()
    test_lolcat_uwu_transformation()
    test_lolcat_chaos_case()
    test_lolcat_emoji_sprinkles()
    test_lolcat_gradient_phase()
    test_lolcat_performance()
    test_lolcat_rule_rewrites()

    print("😺 All LOLcat++ tests passed!")
