#!/usr/bin/env python3
"""
🎼 Conductor Score DSL - Musical Score for Text Performance
=========================================================

A markup language for "scoring text" like a musical score:
- [Tremolo forte] TuneZilla [/]
- [Pizzicato piano] Rawtunez [/]
- [Violin Solo crescendo] Code Live [/]
- [Guitar Lead ff] Rawtunez [/]

Features:
- Dynamics (pp, p, mp, mf, f, ff, fff)
- Crescendo/Decrescendo (gradual build/decay)
- Ensemble sections (violins, violas, cellos, basses)
- Conducted score mode (act by act unfolding)
- Hybrid instruments (Neon Vibrato, Glitch Arpeggio)
"""

import re
import random
import math
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Import the FX runtime
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from runtime import apply_chain, FXConfig, OutputMode


class Dynamics(Enum):
    """Musical dynamics"""
    PPP = "ppp"  # pianississimo
    PP = "pp"    # pianissimo
    P = "p"      # piano
    MP = "mp"    # mezzo-piano
    MF = "mf"    # mezzo-forte
    F = "f"      # forte
    FF = "ff"    # fortissimo
    FFF = "fff"  # fortississimo


class EnsembleSection(Enum):
    """Orchestra sections"""
    VIOLINS = "violins"
    VIOLAS = "violas"
    CELLOS = "cellos"
    BASSES = "basses"
    STRINGS = "strings"  # all strings


@dataclass
class ScoreInstruction:
    """A single instruction in the conductor score"""
    technique: str
    dynamics: Dynamics
    section: Optional[EnsembleSection] = None
    crescendo: bool = False
    decrescendo: bool = False
    hybrid_fx: Optional[str] = None  # e.g., "neon", "glitch", "rainbow"


@dataclass
class ScoreText:
    """Text with score instructions"""
    text: str
    instructions: List[ScoreInstruction]


class ConductorScoreParser:
    """Parser for the Conductor Score DSL"""
    
    def __init__(self):
        self.pattern = re.compile(r'\[([^\]]+)\]([^[]+)\[/\]')
        self.dynamics_map = {
            'ppp': Dynamics.PPP, 'pp': Dynamics.PP, 'p': Dynamics.P,
            'mp': Dynamics.MP, 'mf': Dynamics.MF, 'f': Dynamics.F,
            'ff': Dynamics.FF, 'fff': Dynamics.FFF
        }
        self.techniques = [
            'tremolo', 'vibrato', 'glissando', 'arpeggio', 'harmonics',
            'palm_mute', 'double_stops', 'string_bends', 'trill',
            'pizzicato', 'feedback', 'violin_solo', 'guitar_lead',
            'string_orchestra', 'pizzicato_strings', 'arpeggio_harp',
            'feedback_sustain'
        ]
        self.sections = ['violins', 'violas', 'cellos', 'basses', 'strings']
        self.hybrid_fx = ['neon', 'glitch', 'rainbow', 'stutter', 'scramble']
    
    def parse(self, score_text: str) -> List[ScoreText]:
        """Parse conductor score DSL into ScoreText objects"""
        results = []
        
        for match in self.pattern.finditer(score_text):
            instruction_text = match.group(1).strip()
            text = match.group(2).strip()
            
            instruction = self._parse_instruction(instruction_text)
            results.append(ScoreText(text=text, instructions=[instruction]))
        
        return results
    
    def _parse_instruction(self, instruction_text: str) -> ScoreInstruction:
        """Parse a single instruction"""
        parts = instruction_text.split()
        
        # Extract technique
        technique = None
        for part in parts:
            if part.lower() in self.techniques:
                technique = part.lower()
                break
        
        if not technique:
            technique = 'vibrato'  # default
        
        # Extract dynamics
        dynamics = Dynamics.MF  # default mezzo-forte
        for part in parts:
            if part.lower() in self.dynamics_map:
                dynamics = self.dynamics_map[part.lower()]
                break
        
        # Extract section
        section = None
        for part in parts:
            if part.lower() in self.sections:
                section = EnsembleSection(part.lower())
                break
        
        # Check for crescendo/decrescendo
        crescendo = 'crescendo' in instruction_text.lower()
        decrescendo = 'decrescendo' in instruction_text.lower()
        
        # Extract hybrid FX
        hybrid_fx = None
        for part in parts:
            if part.lower() in self.hybrid_fx:
                hybrid_fx = part.lower()
                break
        
        return ScoreInstruction(
            technique=technique,
            dynamics=dynamics,
            section=section,
            crescendo=crescendo,
            decrescendo=decrescendo,
            hybrid_fx=hybrid_fx
        )


class ConductorScoreRenderer:
    """Renderer for conductor score DSL"""
    
    def __init__(self):
        self.parser = ConductorScoreParser()
        self.dynamics_intensity_map = {
            Dynamics.PPP: 0.1, Dynamics.PP: 0.2, Dynamics.P: 0.3,
            Dynamics.MP: 0.4, Dynamics.MF: 0.5, Dynamics.F: 0.7,
            Dynamics.FF: 0.8, Dynamics.FFF: 0.9
        }
        self.section_fx_map = {
            EnsembleSection.VIOLINS: ['vibrato', 'harmonics'],
            EnsembleSection.VIOLAS: ['vibrato', 'double_stops'],
            EnsembleSection.CELLOS: ['string_bends', 'harmonics'],
            EnsembleSection.BASSES: ['palm_mute', 'feedback']
        }
    
    def render(self, score_text: str, config: FXConfig = None) -> str:
        """Render conductor score DSL to transformed text"""
        if config is None:
            config = FXConfig()
        
        score_texts = self.parser.parse(score_text)
        results = []
        
        for score_text in score_texts:
            rendered_text = self._render_score_text(score_text, config)
            results.append(rendered_text)
        
        return ' '.join(results)
    
    def _render_score_text(self, score_text: ScoreText, config: FXConfig) -> str:
        """Render a single ScoreText object"""
        text = score_text.text
        instructions = score_text.instructions
        
        for instruction in instructions:
            # Build FX chain based on instruction
            chain = self._build_fx_chain(instruction, config)
            
            # Apply dynamics
            intensity = self.dynamics_intensity_map.get(instruction.dynamics, 0.5)
            if instruction.crescendo:
                intensity = self._apply_crescendo(intensity, len(text))
            elif instruction.decrescendo:
                intensity = self._apply_decrescendo(intensity, len(text))
            
            # Create FX config with dynamics
            fx_config = FXConfig(
                intensity=intensity,
                seed=config.seed,
                mode=config.mode,
                max_length=config.max_length,
                budget_ms=config.budget_ms
            )
            
            # Apply effects
            text = apply_chain(text, chain, fx_config)
        
        return text
    
    def _build_fx_chain(self, instruction: ScoreInstruction, config: FXConfig) -> List[Dict[str, Any]]:
        """Build FX chain based on instruction"""
        chain = []
        
        # Add technique
        if instruction.technique in ['violin_solo', 'guitar_lead', 'pizzicato_strings', 'arpeggio_harp', 'feedback_sustain', 'string_orchestra']:
            # Use preset - these are handled by the enhanced_string_fx.py
            # For now, use individual techniques
            if instruction.technique == 'violin_solo':
                chain.append({"name": "vibrato", "params": {"rate": 8.0, "depth": 0.8}})
                chain.append({"name": "glissando", "params": {"slide_speed": 1.2}})
                chain.append({"name": "harmonics", "params": {"harmonic_count": 1}})
            elif instruction.technique == 'guitar_lead':
                chain.append({"name": "string_bends", "params": {"bend_strength": 0.7}})
                chain.append({"name": "vibrato", "params": {"rate": 7.0, "depth": 0.5}})
                chain.append({"name": "feedback", "params": {"feedback_length": 3}})
            elif instruction.technique == 'pizzicato_strings':
                chain.append({"name": "pizzicato", "params": {"accent_chars": "!?."}})
                chain.append({"name": "palm_mute", "params": {"mute_chars": "·x—"}})
                chain.append({"name": "trill", "params": {"trill_chars": "AB", "trill_rate": 0.4}})
            elif instruction.technique == 'arpeggio_harp':
                chain.append({"name": "arpeggio", "params": {"spread": 3}})
                chain.append({"name": "harmonics", "params": {"harmonic_count": 3}})
                chain.append({"name": "glissando", "params": {"slide_speed": 0.8}})
            elif instruction.technique == 'feedback_sustain':
                chain.append({"name": "feedback", "params": {"feedback_length": 8}})
                chain.append({"name": "tremolo", "params": {"type": "amplitude", "rate": 4.0}})
                chain.append({"name": "harmonics", "params": {"harmonic_count": 2}})
            elif instruction.technique == 'string_orchestra':
                chain.append({"name": "vibrato", "params": {"rate": 6.0, "depth": 0.6}})
                chain.append({"name": "harmonics", "params": {"harmonic_count": 2}})
                chain.append({"name": "double_stops", "params": {"intensity": 0.5}})
        else:
            # Use individual technique
            chain.append({"name": instruction.technique, "params": {}})
        
        # Add section-specific effects
        if instruction.section and instruction.section in self.section_fx_map:
            for fx in self.section_fx_map[instruction.section]:
                chain.append({"name": fx, "params": {}})
        
        # Add hybrid FX
        if instruction.hybrid_fx:
            if instruction.hybrid_fx == "neon":
                chain.append({"name": "neon_fx", "params": {"glow": 1.5}})
            elif instruction.hybrid_fx == "glitch":
                chain.append({"name": "glitch_colors", "params": {"glitch_factor": 0.8}})
            elif instruction.hybrid_fx == "rainbow":
                chain.append({"name": "rainbow_gradient", "params": {}})
            elif instruction.hybrid_fx == "stutter":
                chain.append({"name": "stutter", "params": {"rate": 0.3}})
            elif instruction.hybrid_fx == "scramble":
                chain.append({"name": "scramble", "params": {"scramble_factor": 0.6}})
            else:
                chain.append({"name": instruction.hybrid_fx, "params": {}})
        
        return chain
    
    def _apply_crescendo(self, base_intensity: float, text_length: int) -> float:
        """Apply crescendo (gradual build)"""
        # Start soft, build to forte
        start_intensity = base_intensity * 0.3
        end_intensity = base_intensity * 1.5
        return start_intensity + (end_intensity - start_intensity) * 0.8
    
    def _apply_decrescendo(self, base_intensity: float, text_length: int) -> float:
        """Apply decrescendo (gradual decay)"""
        # Start forte, decay to soft
        start_intensity = base_intensity * 1.5
        end_intensity = base_intensity * 0.3
        return start_intensity + (end_intensity - start_intensity) * 0.8


class ConductorScoreComposer:
    """Composer for creating conductor scores"""
    
    def __init__(self):
        self.renderer = ConductorScoreRenderer()
    
    def create_score(self, text: str, technique: str, dynamics: str = "mf", 
                    section: str = None, crescendo: bool = False, 
                    decrescendo: bool = False, hybrid_fx: str = None) -> str:
        """Create a conductor score for text"""
        instruction_parts = [technique, dynamics]
        
        if section:
            instruction_parts.append(section)
        
        if crescendo:
            instruction_parts.append("crescendo")
        elif decrescendo:
            instruction_parts.append("decrescendo")
        
        if hybrid_fx:
            instruction_parts.append(hybrid_fx)
        
        instruction = " ".join(instruction_parts)
        return f"[{instruction}] {text} [/]"
    
    def create_ensemble_score(self, text: str) -> str:
        """Create a full ensemble score"""
        words = text.split()
        if len(words) < 4:
            return self.create_score(text, "string_orchestra", "mf")
        
        # Divide into sections
        violins = words[:len(words)//4]
        violas = words[len(words)//4:len(words)//2]
        cellos = words[len(words)//2:3*len(words)//4]
        basses = words[3*len(words)//4:]
        
        score_parts = []
        
        if violins:
            score_parts.append(self.create_score(" ".join(violins), "vibrato", "f", "violins"))
        if violas:
            score_parts.append(self.create_score(" ".join(violas), "double_stops", "mf", "violas"))
        if cellos:
            score_parts.append(self.create_score(" ".join(cellos), "string_bends", "mf", "cellos"))
        if basses:
            score_parts.append(self.create_score(" ".join(basses), "palm_mute", "p", "basses"))
        
        return " ".join(score_parts)
    
    def create_crescendo_score(self, text: str) -> str:
        """Create a crescendo score"""
        words = text.split()
        if len(words) < 3:
            return self.create_score(text, "tremolo", "p", crescendo=True)
        
        # Build crescendo across words
        score_parts = []
        for i, word in enumerate(words):
            dynamics = ["p", "mp", "mf", "f", "ff"][min(i, 4)]
            score_parts.append(self.create_score(word, "tremolo", dynamics, crescendo=True))
        
        return " ".join(score_parts)
    
    def create_hybrid_score(self, text: str, technique: str, hybrid_fx: str) -> str:
        """Create a hybrid score with technique + FX"""
        return self.create_score(text, technique, "mf", hybrid_fx=hybrid_fx)


def main():
    """Test the conductor score DSL"""
    composer = ConductorScoreComposer()
    renderer = ConductorScoreRenderer()
    
    # Test basic score
    score = "[Tremolo forte] TuneZilla [/]"
    print(f"Score: {score}")
    result = renderer.render(score)
    print(f"Result: {result}")
    print()
    
    # Test crescendo
    score = "[Violin Solo crescendo] Code Live [/]"
    print(f"Score: {score}")
    result = renderer.render(score)
    print(f"Result: {result}")
    print()
    
    # Test hybrid
    score = "[Guitar Lead ff neon] Rawtunez [/]"
    print(f"Score: {score}")
    result = renderer.render(score)
    print(f"Result: {result}")
    print()
    
    # Test ensemble
    score = composer.create_ensemble_score("Code Live TuneZilla Rawtunez")
    print(f"Ensemble Score: {score}")
    result = renderer.render(score)
    print(f"Ensemble Result: {result}")


if __name__ == "__main__":
    main()
