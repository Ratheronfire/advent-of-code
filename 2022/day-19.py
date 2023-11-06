import re
from copy import deepcopy
from enum import Enum
from typing import List

from puzzle_base import PuzzleBase


class Resources(Enum):
    NONE = 0
    ORE = 1,
    CLAY = 2,
    OBSIDIAN = 3,
    GEODE = 4


class RobotCost:
    resource_type: Resources
    amount: int

    def __init__(self, resource_type, amount):
        self.resource_type = resource_type
        self.amount = amount


class ResourceMine:
    resource_type: Resources
    robot_costs: list[RobotCost]

    def __init__(self, resource_type, robot_costs):
        self.resource_type = resource_type
        self.robot_costs = robot_costs


class Blueprint:
    id: int

    ore_mine: ResourceMine
    clay_mine: ResourceMine
    obsidian_mine: ResourceMine
    geode_mine: ResourceMine

    def __init__(self, id, ore_cost, clay_cost, obsidian_ore_cost, obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost):
        self.id = id

        self.ore_mine = ResourceMine(Resources.ORE, [RobotCost(Resources.ORE, ore_cost)])

        self.clay_mine = ResourceMine(Resources.CLAY, [RobotCost(Resources.ORE, clay_cost)])

        self.obsidian_mine = ResourceMine(Resources.OBSIDIAN, [
            RobotCost(Resources.ORE, obsidian_ore_cost),
            RobotCost(Resources.CLAY, obsidian_clay_cost)
        ])

        self.geode_mine = ResourceMine(Resources.GEODE, [
            RobotCost(Resources.ORE, geode_ore_cost),
            RobotCost(Resources.OBSIDIAN, geode_obsidian_cost)
        ])

    @property
    def mines(self) -> list[ResourceMine]:
        return [self.ore_mine, self.clay_mine, self.obsidian_mine, self.geode_mine]

    def __getitem__(self, item):
        if item == Resources.ORE:
            return self.ore_mine
        elif item == Resources.CLAY:
            return self.clay_mine
        elif item == Resources.OBSIDIAN:
            return self.obsidian_mine
        elif item == Resources.GEODE:
            return self.geode_mine


def get_affordable_robots(blueprint: Blueprint, ore_count, clay_count, obsidian_count, geode_count):
    affordable_robots = {}

    for mine in blueprint.mines:
        amount_per_resource = {}
        for cost in mine.robot_costs:
            amount = 0

            if cost.resource_type == Resources.ORE:
                amount = ore_count // cost.amount
            elif cost.resource_type == Resources.CLAY:
                amount = clay_count // cost.amount
            elif cost.resource_type == Resources.OBSIDIAN:
                amount = obsidian_count // cost.amount
            elif cost.resource_type == Resources.GEODE:
                amount = geode_count // cost.amount

            amount_per_resource[cost.resource_type] = amount

        affordable_costs = [amount for amount in amount_per_resource.values() if amount > 0]
        affordable_robots[mine.resource_type] = min(affordable_costs) if len(affordable_costs) else 0

    return affordable_robots


def can_afford_robot(robot_costs, ore_count, clay_count, obsidian_count, geode_count):
    for cost in robot_costs:
        if (cost.resource_type == Resources.ORE and ore_count < cost.amount) or \
                (cost.resource_type == Resources.CLAY and clay_count < cost.amount) or \
                (cost.resource_type == Resources.OBSIDIAN and obsidian_count < cost.amount) or \
                (cost.resource_type == Resources.GEODE and geode_count < cost.amount):
            return False

    return True


class Puzzle(PuzzleBase):
    year = 2022
    day = 19

    blueprints: list[Blueprint]

    decision_cache = {}

    def reset(self):
        self.blueprints = []

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            line = input_data[i]

            match = re.match(r'Blueprint (\d+): '
                             r'Each ore robot costs (\d+) ore. '
                             r'Each clay robot costs (\d+) ore. '
                             r'Each obsidian robot costs (\d+) ore and (\d+) clay. '
                             r'Each geode robot costs (\d+) ore and (\d+) obsidian.', line)
            if match:
                blueprint = Blueprint(
                    int(match[1]),
                    int(match[2]),
                    int(match[3]),
                    int(match[4]),
                    int(match[5]),
                    int(match[6]),
                    int(match[7])
                )

                self.blueprints.append(blueprint)

    def get_ideal_decision(self, blueprint: Blueprint,
                           ore_robots=1, clay_robots=0, obsidian_robots=0, geode_robots=0,
                           ore_count=0, clay_count=0, obsidian_count=0, geode_count=0,
                           minute=0,
                           robot_to_build: Resources = Resources.NONE,
                           pending_robot: Resources = Resources.NONE):
        if minute >= 24:
            return geode_count

        if pending_robot == Resources.ORE:
            ore_robots += 1
        elif pending_robot == Resources.CLAY:
            clay_robots += 1
        elif pending_robot == Resources.OBSIDIAN:
            obsidian_robots += 1
        elif pending_robot == Resources.GEODE:
            geode_robots += 1
        pending_robot = Resources.NONE

        if robot_to_build != Resources.NONE:
            for cost in blueprint[robot_to_build].robot_costs:
                if cost.resource_type == Resources.ORE:
                    ore_count -= cost.amount
                elif cost.resource_type == Resources.CLAY:
                    clay_count -= cost.amount
                elif cost.resource_type == Resources.OBSIDIAN:
                    obsidian_count -= cost.amount
                elif cost.resource_type == Resources.GEODE:
                    geode_count -= cost.amount

            pending_robot = robot_to_build

        ore_count += ore_robots
        clay_count += clay_robots
        obsidian_count += obsidian_robots
        geode_count += geode_robots

        if (ore_count, clay_count, obsidian_count, geode_count,
            ore_robots, clay_robots, obsidian_robots, geode_robots) \
                in self.decision_cache:
            return self.decision_cache[(ore_count, clay_count, obsidian_count, geode_count,
                                        ore_robots, clay_robots, obsidian_robots, geode_robots)]

        decisions = []

        for mine in blueprint.mines:
            can_afford = can_afford_robot(mine.robot_costs, ore_count, clay_count, obsidian_count, geode_count)

            if can_afford:
                decisions.append(mine.resource_type)

        decisions.append(Resources.NONE)

        geode_totals = []
        for decision in decisions:
            geode_totals.append(
                self.get_ideal_decision(
                    blueprint,
                    ore_robots, clay_robots, obsidian_robots, geode_robots,
                    ore_count, clay_count, obsidian_count, geode_count,
                    minute + 1, decision, pending_robot)
            )

        max_geodes = max(geode_totals)
        self.decision_cache[(ore_count, clay_count, obsidian_count, geode_count,
                             ore_robots, clay_robots, obsidian_robots, geode_robots)] = max_geodes
        return max_geodes

    def get_day_1_answer(self, use_sample=False) -> str:
        scores = []
        for blueprint in self.blueprints:
            self.decision_cache = {}
            scores.append(self.get_ideal_decision(blueprint))

        print(scores)
        return str(sum([(i + 1) * scores[i] for i in range(len(scores))]))

    def get_day_2_answer(self, use_sample=False) -> str:
        return ''


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
