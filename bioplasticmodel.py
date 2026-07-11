#!/usr/bin/env python3
"""
Hemp seed bioplastic model:
- Start from hemp seed components
- Form a bioplastic / faux-leather sheet
- Fortify it
- Cut it into strips and evaluate properties

Conceptual only: no real-world chemistry steps.
"""

from dataclasses import dataclass
from math import fabs

@dataclass
class Composition:
    protein: float      # hemp seed protein
    oil: float          # hemp seed oil (triglycerides)
    cellulose: float    # seed coat cellulose fragments
    salt: float         # ionic species
    water: float        # effective water

@dataclass
class MolecularKnobs:
    denaturation_level: float   # 0–1
    oleogel_structuring: float  # 0–1
    ionic_crosslinking: float   # 0–1

@dataclass
class Properties:
    fortification: float
    flexibility: float
    strength: float
    cohesion: float

def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))

def normalize(comp: Composition) -> Composition:
    total = comp.protein + comp.oil + comp.cellulose + comp.salt + comp.water
    if total <= 0:
        raise ValueError("Total composition must be > 0")
    f = 1.0 / total
    comp.protein *= f
    comp.oil *= f
    comp.cellulose *= f
    comp.salt *= f
    comp.water *= f
    return comp

def evaluate_bioplastic(comp: Composition, knobs: MolecularKnobs) -> Properties:
    comp = normalize(comp)

    p, o, c, s, w = comp.protein, comp.oil, comp.cellulose, comp.salt, comp.water
    d = clamp(knobs.denaturation_level)
    g = clamp(knobs.oleogel_structuring)
    x = clamp(knobs.ionic_crosslinking)

    # Flexibility: oil + oleogel + water, penalized by stiff networks
    flex = clamp(0.6*o + 0.3*g + 0.1*w - (0.3*d + 0.3*x))

    # Strength: protein network + cellulose, penalized by excess oil
    strength = clamp(0.5*p*d + 0.2*c + 0.2*(0.4 - fabs(x - 0.5)) - 0.4*o)

    # Cohesion: protein + oleogel + ions + water
    cohesion = clamp(
        0.3*p*d +
        0.3*o*g +
        0.2*w +
        0.2*(0.4 - fabs(s - 0.2))
    )

    fortification = clamp((flex + strength + cohesion) / 3.0)

    return Properties(fortification, flex, strength, cohesion)

def base_hemp_seed_composition() -> Composition:
    # Conceptual split of hemp seed mass into functional fractions
    return Composition(
        protein=0.40,
        oil=0.35,
        cellulose=0.08,
        salt=0.10,
        water=0.07
    )

def tuned_knobs() -> MolecularKnobs:
    # A balanced profile for faux-leather-like behavior
    return MolecularKnobs(
        denaturation_level=0.85,
        oleogel_structuring=0.80,
        ionic_crosslinking=0.55
    )

def cut_strips(props: Properties, width_mm: float = 0.1) -> Properties:
    # Cutting into strips slightly reduces effective properties
    return Properties(
        fortification=props.fortification * 0.95,
        flexibility=props.flexibility * 0.90,
        strength=props.strength * 0.88,
        cohesion=props.cohesion * 0.92
    )

if __name__ == "__main__":
    comp = base_hemp_seed_composition()
    knobs = tuned_knobs()
    sheet_props = evaluate_bioplastic(comp, knobs)
    strip_props = cut_strips(sheet_props, width_mm=0.1)

    print("Hemp seed bioplastic – faux leather model")
    print(f"Sheet properties: {sheet_props}")
    print(f"0.1 mm strip properties: {strip_props}")
