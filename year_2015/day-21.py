import math
import sys
from enum import Enum
from typing import List, Union

from puzzle_base import PuzzleBase


class GearType(Enum):
    WEAPON = 0
    ARMOR = 1
    RING = 2


class Gear:
    gear_type: GearType
    name: str

    cost: int
    damage: int
    armor: int

    def __init__(self, gear_type, name, cost, damage, armor):
        self.gear_type = gear_type
        self.name = name

        self.cost = cost
        self.damage = damage
        self.armor = armor

    def __str__(self):
        return self.name


class Fighter:
    health: int

    _damage: int
    _armor: int

    def __init__(self, health, damage, armor):
        self.health = health

        self._damage = damage
        self._armor = armor

    @property
    def damage(self):
        return self._damage

    @property
    def armor(self):
        return self._armor


class Player(Fighter):
    weapon: Gear
    armor_gear: Union[Gear, None]
    ring_l: Union[Gear, None]
    ring_r: Union[Gear, None]

    def __init__(self, health, damage, armor):
        super().__init__(health, damage, armor)

    def __str__(self):
        return f'Player: Health = {self.health}; Damage = {self.damage}; Armor = {self.armor} | ' \
               f'[{self.weapon}, {self.armor_gear}, {self.ring_l}, {self.ring_r}]'

    @property
    def damage(self):
        damage = self.weapon.damage

        if self.ring_l:
            damage += self.ring_l.damage
        if self.ring_r:
            damage += self.ring_r.damage

        return damage

    @property
    def armor(self):
        armor = 0

        if self.armor_gear:
            armor += self.armor_gear.armor
        if self.ring_l:
            armor += self.ring_l.armor
        if self.ring_r:
            armor += self.ring_r.armor

        return armor


class Puzzle(PuzzleBase):
    year = 2015
    day = 21

    sample_data = 0

    shop_weapons: list[Gear]
    shop_armor: list[Gear]
    shop_rings: list[Gear]

    boss: Fighter
    player: Player

    def reset(self):
        self.shop_weapons = [
            Gear(GearType.WEAPON, 'Dagger',     8,  4, 0),
            Gear(GearType.WEAPON, 'Shortsword', 10, 5, 0),
            Gear(GearType.WEAPON, 'Warhammer',  25, 6, 0),
            Gear(GearType.WEAPON, 'Longsword',  40, 7, 0),
            Gear(GearType.WEAPON, 'Greataxe',   74, 8, 0),
        ]

        self.shop_armor = [
            Gear(GearType.ARMOR, 'Leather',    13,  0, 1),
            Gear(GearType.ARMOR, 'Chainmail',  31,  0, 2),
            Gear(GearType.ARMOR, 'Splintmail', 53,  0, 3),
            Gear(GearType.ARMOR, 'Bandedmail', 75,  0, 4),
            Gear(GearType.ARMOR, 'Platemail',  102, 0, 5),
        ]

        self.shop_rings = [
            Gear(GearType.RING, 'Damage +1',  25,  1, 0),
            Gear(GearType.RING, 'Damage +2',  50,  2, 0),
            Gear(GearType.RING, 'Damage +3',  100, 3, 0),
            Gear(GearType.RING, 'Defense +1', 20,  0, 1),
            Gear(GearType.RING, 'Defense +2', 40,  0, 2),
            Gear(GearType.RING, 'Defense +3', 80,  0, 3),
        ]

        self.player = Player(100, 0, 0)

    def prepare_data(self, input_data: List[str], current_part: int):
        health = int(input_data[0].split(' ')[-1])
        damage = int(input_data[1].split(' ')[-1])
        armor  = int(input_data[2].split(' ')[-1])

        self.boss = Fighter(health, damage, armor)

    def simulate_battle(self) -> bool:
        player_damage_dealt = max(self.player.damage - self.boss.armor, 1)
        boss_damage_dealt = max(self.boss.damage - self.player.armor, 1)

        player_turns_alive = math.ceil(self.player.health / boss_damage_dealt)
        boss_turns_alive = math.ceil(self.boss.health / player_damage_dealt)

        return player_turns_alive >= boss_turns_alive

    def get_loadout_permutations(self):
        weapon_permutations = self.shop_weapons.copy()

        armor_permutations: list[Union[Gear, None]] = self.shop_armor.copy()
        armor_permutations.append(None)

        ring_permutations = []
        for ring_l in self.shop_rings:
            for ring_r in self.shop_rings:
                if ring_l != ring_r:
                    ring_permutations.append([ring_l, ring_r])

            ring_permutations.append([ring_l])

        ring_permutations.append([])

        return weapon_permutations, armor_permutations, ring_permutations

    def get_part_1_answer(self, use_sample=False) -> str:
        weapon_permutations, armor_permutations, ring_permutations = self.get_loadout_permutations()
        cheapest_loadout = sys.maxsize

        for weapon_selection in weapon_permutations:
            for armor_selection in armor_permutations:
                for ring_selection in ring_permutations:
                    self.player.weapon = weapon_selection
                    self.player.armor_gear = armor_selection

                    self.player.ring_l = ring_selection[0] if len(ring_selection) > 0 else None
                    self.player.ring_r = ring_selection[1] if len(ring_selection) > 1 else None

                    loadout_cost = weapon_selection.cost

                    if armor_selection:
                        loadout_cost += armor_selection.cost

                    loadout_cost += sum([r.cost for r in ring_selection])

                    if self.simulate_battle() and loadout_cost < cheapest_loadout:
                        cheapest_loadout = loadout_cost
                        print(f'New best - {loadout_cost} Gold\n{self.player}\n')

        return str(cheapest_loadout)

    def get_part_2_answer(self, use_sample=False) -> str:
        weapon_permutations, armor_permutations, ring_permutations = self.get_loadout_permutations()
        highest_loadout = 0

        for weapon_selection in weapon_permutations:
            for armor_selection in armor_permutations:
                for ring_selection in ring_permutations:
                    self.player.weapon = weapon_selection
                    self.player.armor_gear = armor_selection

                    self.player.ring_l = ring_selection[0] if len(ring_selection) > 0 else None
                    self.player.ring_r = ring_selection[1] if len(ring_selection) > 1 else None

                    loadout_cost = weapon_selection.cost

                    if armor_selection:
                        loadout_cost += armor_selection.cost

                    loadout_cost += sum([r.cost for r in ring_selection])

                    if not self.simulate_battle() and loadout_cost > highest_loadout:
                        highest_loadout = loadout_cost
                        print(f'New worst - {loadout_cost} Gold\n{self.player}\n')

        return str(highest_loadout)


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
