"""Agent Skills standard implementation for 12FZ协作AI.

Provides filesystem-based skill packaging with progressive disclosure.
"""

from fzxiezuoai.skills.loader import activate_skill, discover_skills
from fzxiezuoai.skills.models import Skill, SkillFrontmatter
from fzxiezuoai.skills.parser import SkillParseError


__all__ = [
    "Skill",
    "SkillFrontmatter",
    "SkillParseError",
    "activate_skill",
    "discover_skills",
]
