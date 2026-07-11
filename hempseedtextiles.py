#!/usr/bin/env python3
"""
Hemp seed bioplastic → faux leather → fortified strips
Simple composition model for:
- protein (hemp seed protein)
- oil (hemp seed oil)
- salt (NaCl or similar)
- water (for mobility / cohesion)

Outputs:
- fortification_score
- flexibility_score
- strength_score
- cohesion_score

All inputs are fractions of total solids (0.0–1.0) and should sum to ~1.0.
This is a conceptual model, not a lab protocol.
"""

from dataclasses import dataclass

@dataclass
class Composition:
    protein: float  # hemp seed protein fraction
    oil: float      # hemp seed oil fraction
    salt: float     # salt fraction
    water: float    # water fraction (effective, not free bulk water)


@dataclass
class Properties:
    fortification: float
    flexibility: float
    strength: float
    cohesion: float


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def evaluate_properties(comp: Composition) -> Properties:
    p = comp.protein
    o = comp.oil
    s = comp.salt
    w = comp.water

    # Normalize a bit if user overshoots
    total = p + o + s + w
    if total <= 0:
        raise ValueError("Total composition must be > 0")
    p /= total
    o /= total
    s /= total
    w /= total

    # Flexibility: driven by oil, moderated by protein, reduced by salt
    flex_base = 0.7 * o + 0.3 * (1.0 - p)
    flex_penalty_salt = 0.4 * s
    flexibility = clamp(flex_base - flex_penalty_salt)

    # Strength: driven by protein, slightly helped by moderate salt, reduced by excess oil
    strength_base = 0.8 * p + 0.2 * (0.3 - abs(s - 0.1))  # best around s ≈ 0.1
    strength_penalty_oil = 0.5 * o
    strength = clamp(strength_base - strength_penalty_oil)

    # Cohesion: needs protein network + some oil + a bit of water + moderate salt
    cohesion_base = (
        0.4 * p +
        0.3 * o +
        0.2 * w +
        0.1 * (0.3 - abs(s - 0.15))  # best around s ≈ 0.15
    )
    cohesion = clamp(cohesion_base)

    # Fortification: overall “composite quality” as a blend of the three
    fortification = clamp((flexibility + strength + cohesion) / 3.0)

    return Properties(
        fortification=fortification,
        flexibility=flexibility,
        strength=strength,
        cohesion=cohesion,
    )


def maxed_profile() -> Composition:
    """
    A reasonable 'max fortification / flex / strength / cohesion' compromise
    for your fortified faux-leather strips.
    Tuned qualitatively:
    - mid–high protein for network
    - mid oil for plasticization
    - moderate salt for ionic tightening
    - small water for mobility/cohesion
    """
    return Composition(
        protein=0.45,
        oil=0.35,
        salt=0.12,
        water=0.08,
    )


if __name__ == "__main__":
    comp = maxed_profile()
    props = evaluate_properties(comp)

    print("Hemp seed faux leather fortified strips – model")
    print(f"Composition: protein={comp.protein:.2f}, "
          f"oil={comp.oil:.2f}, salt={comp.salt:.2f}, water={comp.water:.2f}")
    print(f"Fortification score: {props.fortification:.3f}")
    print(f"Flexibility score:   {props.flexibility:.3f}")
    print(f"Strength score:      {props.strength:.3f}")
    print(f"Cohesion score:      {props.cohesion:.3f}")
