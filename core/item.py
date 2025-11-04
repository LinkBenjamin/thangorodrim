"""
Item composition system for Thangorodrim.

This module implements a component-based Item model used by the game.
Instead of a deep inheritance tree, items are composed of small, focused
components (Equippable, Consumable, Stackable, Weapon, etc.) that describe
capabilities and data. Items are instantiated from JSON-like templates via
the item_from_template factory.

Template example:
{
  "id": "potion_healing_small",
  "name": "Small Healing Potion",
  "description": "Restores a small amount of HP.",
  "weight": 0.5,
  "consumable": { "effect": {"heal": 20}, "charges": 1 },
  "stackable": { "quantity": 3 }
}

Notes:
- Components are plain dataclasses and contain no heavy game logic.
- Effect application (e.g. applying heal) should live in game logic, not here.
- This approach simplifies serialization and mix-and-match behavior.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

@dataclass
class Component:
    """Marker base class for item components. Extend to add behavior/state."""
    pass

@dataclass
class Equippable(Component):
    """Data for items that can be equipped.

    Attributes:
        slot: Equipment slot name (e.g. 'weapon', 'head', 'body').
        attack_bonus: Flat attack bonus when equipped.
        defense_bonus: Flat defense bonus when equipped.
    """
    slot: str # 'weapon', 'head', 'body', etc
    attack_bonus: int = 0
    defense_bonus: int = 0

@dataclass
class Consumable(Component):
    """Data for consumable items.

    Attributes:
        effect: A data structure describing the effect (interpreted by game logic).
        charges: Number of uses remaining.
    """
    effect: Dict[str, Any] # description of effect
    charges: int = 1

    def use(self, user):
        """Consume one charge and return the effect payload.

        Returns False if there are no charges left, otherwise returns the
        effect dict (the caller applies it).
        """
        # apply effect to user
        if self.charges <= 0:
            return False
        self.charges -= 1
        return self.effect # caller interprets and applies

@dataclass
class Stackable(Component):
    """Component representing stackable items.

    Attributes:
        max_stack: Maximum items per stack.
        quantity: Current quantity in this stack.
    """
    max_stack: int = 99
    quantity: int = 1

@dataclass
class Weapon(Component):
    """Weapon-specific data component.

    Attributes:
        damage_die: Damage expression (e.g. '1d8').
        range: Attack range (tiles/meters depending on game).
        ammo_type: Optional ammo type for ranged weapons.
    """
    damage_die: str # e.g. '1d8'
    range: int = 1
    ammo_type: Optional[str] = None

@dataclass
class Item:
    """Represents an instantiated item with a set of components.

    Attributes:
        id: Unique template identifier.
        name: Display name.
        description: Human-readable description.
        weight: Item weight used for carry calculations.
        components: Mapping of component name to component instance.
    """
    id: str
    name: str
    description: str = ""
    weight: float = 0.0
    components: Dict[str, Component] = field(default_factory=dict)

    def has(self, comp_name: str) -> bool:
        """Return True if the item contains a component named comp_name."""
        return comp_name in self.components
    
    def get(self, comp_name: str):
        """Return the component instance for comp_name or None if missing."""
        return self.components.get(comp_name)

def item_from_template(template: Dict[str, Any]) -> Item:
    """Factory that creates an Item from a JSON-like template dictionary.

    The template may include keys like 'equippable', 'consumable', 'stackable',
    and 'weapon' to populate component instances. Unknown keys are ignored.

    Raises KeyError if required fields such as 'id' or 'name' are missing.
    """
    comp_map = {}
    if "equippable" in template:
        eq = template['equippable']
        comp_map['equippable'] = Equippable(slot=eq["slot"],
                                           attack_bonus=eq.get("attack_bonus", 0),
                                           defense_bonus=eq.get("defense_bonus", 0))
    if "consumable" in template:
        c = template["consumable"]
        comp_map["consumable"] = Consumable(effect=c["effect"], charges=c.get("charges", 1))
    if "stackable" in template:
        s = template["stackable"]
        comp_map["stackable"] = Stackable(max_stack=s.get("max_stack", 99), quantity=s.get("quantity", 1))
    if "weapon" in template:
        w = template["weapon"]
        comp_map["weapon"] = Weapon(damage_die=w["damage_die"], range=w.get("range", 1), ammo_type=w.get("ammo_type"))

    return Item(id=template["id"],
                name=template["name"],
                description=template.get("description", ""),
                weight=template.get("weight", 0.0),
                components=comp_map)