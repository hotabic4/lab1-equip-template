
from equipment import Player, Item, equip, unequip, total_power


def get_items_total_count(player):
    unique_items = set(id(x) for x in player.slots.values() if x is not None)
    return len(player.inventory) + len(unique_items)


def test_basic_equip_and_invariant():
    p = Player("Warrior", level=5, capacity=5)
    sword = Item("Меч", "right_hand", power=10, level_req=1)
    p.inventory.append(sword)

    assert get_items_total_count(p) == 1

    assert equip(p, sword) is True
    assert p.slots["right_hand"] is sword
    assert sword not in p.inventory
    assert get_items_total_count(p) == 1

    assert unequip(p, "right_hand") is True
    assert p.slots["right_hand"] is None
    assert sword in p.inventory
    assert get_items_total_count(p) == 1


def test_two_handed_weapon_logic():
    p = Player("Knight", level=10, capacity=5)
    shield = Item("Щит", "left_hand", power=5)
    one_hand_sword = Item("Нож", "right_hand", power=3)
    two_handed_sword = Item("Двуруч", "hand", power=25, two_handed=True)

    p.inventory.extend([shield, one_hand_sword, two_handed_sword])
    
    equip(p, shield)
    equip(p, one_hand_sword)
    assert get_items_total_count(p) == 3

    assert equip(p, two_handed_sword) is True
    assert p.slots["right_hand"] is two_handed_sword
    assert p.slots["left_hand"] is two_handed_sword
    assert shield in p.inventory
    assert one_hand_sword in p.inventory
    assert get_items_total_count(p) == 3


def test_broken_item_durability_zero():
    p = Player("Paladin", level=1)
    broken_armor = Item("Сломанная кираса", "body", power=50, durability=0)
    
    p.inventory.append(broken_armor)
    equip(p, broken_armor)
    
    assert total_power(p) == 0
    
    assert unequip(p, "body") is True
    assert broken_armor in p.inventory


def test_inventory_overflow_deny():
    p = Player("Thief", level=1, capacity=1)
    shield = Item("Щит", "left_hand", power=5)
    axe = Item("Топор", "right_hand", power=5)
    
    p.slots["left_hand"] = shield
    p.inventory.append(axe)
    
    assert equip(p, axe) is False
    assert p.slots["left_hand"] is shield
    assert axe in p.inventory
