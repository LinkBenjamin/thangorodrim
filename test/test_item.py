"""
Tests for the core.item class.

These unit tests verify:
- item_from_template behavior for minimal and full templates
- handling of unknown keys and missing required fields
- Consumable use semantics (charges and return values)
- Stackable defaults and constraints
- Direct instantiation of Equippable and Weapon components
"""

import pytest

from core.item import (
    Item,
    item_from_template,
    Consumable,
    Stackable,
    Equippable,
    Weapon,
)


def test_item_from_template_minimal():
    """Create an Item from a minimal template and assert defaults.

    Verifies that required top-level fields are set, optional fields
    (weight, components) default correctly, and missing components
    return None / report as absent.
    """
    tmpl = {"id": "test_paper", "name": "Paper", "description": "A sheet"}
    item = item_from_template(tmpl)
    assert isinstance(item, Item)
    assert item.id == "test_paper"
    assert item.name == "Paper"
    assert item.description == "A sheet"
    assert item.weight == pytest.approx(0.0)
    assert item.components == {}
    assert not item.has("consumable")
    assert item.get("consumable") is None


def test_item_from_template_all_components():
    """Build an Item with all supported components and validate them.

    Ensures component factories produce the expected component types
    and that their fields are populated from the template.
    """
    tmpl = {
        "id": "potion_healing_small",
        "name": "Small Healing Potion",
        "description": "Restores a small amount of HP.",
        "weight": 0.5,
        "consumable": {"effect": {"heal": 20}, "charges": 3},
        "stackable": {"quantity": 3, "max_stack": 20},
        "equippable": {"slot": "hand", "attack_bonus": 1, "defense_bonus": 0},
        "weapon": {"damage_die": "1d6", "range": 1},
    }
    item = item_from_template(tmpl)

    # top-level fields
    assert item.id == tmpl["id"]
    assert item.name == tmpl["name"]
    assert item.weight == pytest.approx(0.5)

    # components present
    assert item.has("consumable")
    assert item.has("stackable")
    assert item.has("equippable")
    assert item.has("weapon")

    cons = item.get("consumable")
    assert isinstance(cons, Consumable)
    assert cons.effect == {"heal": 20}
    assert cons.charges == 3

    stk = item.get("stackable")
    assert isinstance(stk, Stackable)
    assert stk.quantity == 3
    assert stk.max_stack == 20

    eq = item.get("equippable")
    assert isinstance(eq, Equippable)
    assert eq.slot == "hand"
    assert eq.attack_bonus == 1

    wp = item.get("weapon")
    assert isinstance(wp, Weapon)
    assert wp.damage_die == "1d6"
    assert wp.range == 1


def test_item_from_template_ignores_unknown_keys():
    """Unknown top-level keys in a template should be ignored."""
    tmpl = {"id": "mystery", "name": "Strange", "foo": {"bar": 1}}
    item = item_from_template(tmpl)
    # unknown 'foo' should be ignored
    assert item.components == {}
    assert not item.has("foo")


def test_item_from_template_missing_required_raises():
    """Missing required top-level fields should raise KeyError."""
    with pytest.raises(KeyError):
        item_from_template({"name": "no id"})
    with pytest.raises(KeyError):
        item_from_template({"id": "no_name"})


def test_consumable_use_behaviour():
    """Consumable.use should return effect while charges remain and decrement."""
    c = Consumable(effect={"heal": 10}, charges=2)
    # first use returns effect and decrements
    res1 = c.use(user=None)
    assert res1 == {"heal": 10}
    assert c.charges == 1
    # second use returns effect and decrements to 0
    res2 = c.use(user=None)
    assert res2 == {"heal": 10}
    assert c.charges == 0
    # third use returns False when no charges remain
    res3 = c.use(user=None)
    assert res3 is False
    assert c.charges == 0


def test_consumable_with_zero_charges_returns_false():
    """A Consumable initialized with zero charges should immediately be unusable."""
    c = Consumable(effect={"buff": 1}, charges=0)
    assert c.use(user=None) is False
    assert c.charges == 0


def test_stackable_defaults_and_values():
    """Stackable should provide sensible defaults and enforce quantity <= max_stack."""
    s = Stackable()
    # defaults
    assert s.max_stack == 99
    assert s.quantity == 1

    # explicit values preserved
    s2 = Stackable(max_stack=10, quantity=5)
    assert s2.max_stack == 10
    assert s2.quantity == 5
    assert s2.quantity <= s2.max_stack


def test_equippable_and_weapon_direct_instantiation():
    """Directly instantiate Equippable and Weapon and validate fields."""
    e = Equippable(slot="head", attack_bonus=0, defense_bonus=2)
    assert e.slot == "head"
    assert e.defense_bonus == 2

    w = Weapon(damage_die="2d4", range=3, ammo_type="arrow")
    assert w.damage_die == "2d4"
    assert w.range == 3
    assert w.ammo_type == "arrow"