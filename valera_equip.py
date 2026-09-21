"""Экипировка. Старая версия, тестовый сервер.

Автор: Валера. Поддержка: никто.

Файл нужен только затем, чтобы воспроизвести дюп. Чинить его не надо —
новую систему ты пишешь в equipment.py с нуля.
"""

SLOTS = ("head", "body", "right_hand", "left_hand", "ring_1", "ring_2")
HANDS = ("right_hand", "left_hand")


class Item:

    def __init__(self, name, slot, power=0, durability=100, level_req=1,
                 two_handed=False):
        self.name = name
        self.slot = slot
        self.power = power
        self.durability = durability
        self.level_req = level_req
        self.two_handed = two_handed

    def __bool__(self):
        return self.durability > 0

    def __repr__(self):
        return f"<{self.name} {self.slot} dur={self.durability}>"


class Player:
    def __init__(self, name, level=1, inventory=None, capacity=20):
        self.name = name
        self.level = level
        self.inventory = list(inventory) if inventory else []
        self.capacity = capacity
        self.slots = {slot: None for slot in SLOTS}

    def __repr__(self):
        return f"<{self.name} lvl={self.level} inv={len(self.inventory)}>"


def equip(player, item):
    if item not in player.inventory:
        return False
    if item.slot not in SLOTS and item.slot != "hand":
        return False
    if player.level < item.level_req:
        return False

    initial_count = len(player.inventory) + len(set(id(x) for x in player.slots.values() if x is not None))

    target_slots = []
    if item.slot == "hand":
        if item.two_handed:
            target_slots = list(HANDS)
        else:
            target_slots = ["right_hand"] if player.slots["right_hand"] is None else ["left_hand"] if player.slots["left_hand"] is None else ["right_hand"]
    else:
        target_slots = [item.slot]

    items_to_unequip = []
    for s in target_slots:
        current_item = player.slots[s]
        if current_item is not None and current_item not in items_to_unequip:
            items_to_unequip.append(current_item)
            
    for s in HANDS:
        current_item = player.slots[s]
        if current_item is not None and current_item.two_handed and current_item not in items_to_unequip:
            items_to_unequip.append(current_item)

    predicted_inv_len = len(player.inventory) - 1 + len(items_to_unequip)
    if predicted_inv_len > player.capacity:
        return False

    player.inventory.remove(item)
    
    for s in player.slots:
        if player.slots[s] in items_to_unequip:
            player.slots[s] = None
            
    for old_item in items_to_unequip:
        player.inventory.append(old_item)

    for s in target_slots:
        player.slots[s] = item

    final_count = len(player.inventory) + len(set(id(x) for x in player.slots.values() if x is not None))
    assert initial_count == final_count
    
    return True


def unequip(player, slot):
    item = player.slots[slot]
    if item is None:
        return False

    if len(player.inventory) >= player.capacity:
        return False

    initial_count = len(player.inventory) + len(set(id(x) for x in player.slots.values() if x is not None))

    if item.two_handed:
        player.slots["right_hand"] = None
        player.slots["left_hand"] = None
    else:
        player.slots[slot] = None

    player.inventory.append(item)

    final_count = len(player.inventory) + len(set(id(x) for x in player.slots.values() if x is not None))
    assert initial_count == final_count
    
    return True


def total_power(player):
    power = 0
    counted_items_ids = set()
    
    for slot, item in player.slots.items():
        if item is not None and id(item) not in counted_items_ids:
            counted_items_ids.add(id(item))
            if item:  
                power += item.power
    return power
