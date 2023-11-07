from abc import ABC
from enum import Enum
from typing import List, Union

from puzzle_base import PuzzleBase


class Signal:
    wire_key: str = None
    _value: int = None

    def __init__(self, key_or_const: Union[str, int]):
        if key_or_const.isnumeric():
            self.value = int(key_or_const)
        else:
            self.wire_key = key_or_const

    @property
    def has_value(self) -> bool:
        return self.value is not None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: int):
        self._value = value & 0xFFFF

    def __str__(self):
        if self.has_value:
            value_str = f'[{self.value}; {bin(self.value)}]'

            if self.wire_key is not None:
                return f'{self.wire_key}{value_str}'
            else:
                return value_str
        else:
            return self.wire_key


class InstructionType(Enum):
    STORE = 0,
    NOT = 1,
    AND = 2,
    OR = 3,
    LSHIFT = 4,
    RSHIFT = 5


class Instruction:
    out_wire: str
    in_signals: list[Signal]

    shift_num = 0

    instruction_type: InstructionType

    def __init__(self, out_wire: str, in_signals: list[Signal], instruction_type: InstructionType, shift_num = 0):
        self.out_wire = out_wire
        self.in_signals = in_signals

        self.shift_num = shift_num

        self.instruction_type = instruction_type

    def __str__(self):
        if self.instruction_type == InstructionType.STORE:
            return f'{self.in_signals[0]} -> {self.out_wire}'
        elif self.instruction_type == InstructionType.NOT:
            return f'NOT {self.in_signals[0]} -> {self.out_wire}'
        elif self.instruction_type == InstructionType.AND:
            return f'{self.in_signals[0]} AND {self.in_signals[1]} -> {self.out_wire}'
        elif self.instruction_type == InstructionType.OR:
            return f'{self.in_signals[0]} OR {self.in_signals[1]} -> {self.out_wire}'
        elif self.instruction_type == InstructionType.LSHIFT:
            return f'{self.in_signals[0]} LSHIFT {self.shift_num} -> {self.out_wire}'
        elif self.instruction_type == InstructionType.RSHIFT:
            return f'{self.in_signals[0]} RSHIFT {self.shift_num} -> {self.out_wire}'


# def instructions_to_str():
#     return '\n'.join([f'{wire}: {wire_instructions[wire]}' for wire in sorted(wire_instructions.keys())])


class Puzzle(PuzzleBase):
    year = 2015
    day = 7

    instructions: list[Instruction]
    signals: dict[str, Signal]

    def reset(self):
        self.instructions = []
        self.signals = {}

    def prepare_data(self, input_data: List[str], current_part: int):
        for i in range(len(input_data)):
            if input_data[i] == '':
                continue

            opcodes = input_data[i].split(' ')

            shift_num = 0

            if len(opcodes) == 3:
                to_wire = opcodes[2]
                from_wires = [opcodes[0]]
                instruction_type = InstructionType.STORE
            elif opcodes[0] == 'NOT':
                to_wire = opcodes[3]
                from_wires = [opcodes[1]]
                instruction_type = InstructionType.NOT
            elif opcodes[1] == 'AND':
                to_wire = opcodes[4]
                from_wires = [opcodes[0], opcodes[2]]
                instruction_type = InstructionType.AND
            elif opcodes[1] == 'OR':
                to_wire = opcodes[4]
                from_wires = [opcodes[0], opcodes[2]]
                instruction_type = InstructionType.OR
            elif opcodes[1] == 'LSHIFT':
                to_wire = opcodes[4]
                from_wires = [opcodes[0]]
                instruction_type = InstructionType.LSHIFT
                shift_num = int(opcodes[2])
            else:
                to_wire = opcodes[4]
                from_wires = [opcodes[0]]
                instruction_type = InstructionType.RSHIFT
                shift_num = int(opcodes[2])

            for wire in from_wires:
                if wire not in self.signals:
                    self.signals[wire] = Signal(wire)

            instruction = Instruction(to_wire, [self.signals[w] for w in from_wires], instruction_type, shift_num)
            self.instructions.append(instruction)

    def get_value_on_wire(self, wire: str) -> int:
        wire_instruction = [i for i in self.instructions if i.out_wire == wire][0]

        print(f'[Start] {wire_instruction}')

        for signal in wire_instruction.in_signals:
            if not signal.has_value:
                signal.value = self.get_value_on_wire(signal.wire_key)

        value = -1
        if wire_instruction.instruction_type == InstructionType.STORE:
            value = wire_instruction.in_signals[0].value
        elif wire_instruction.instruction_type == InstructionType.NOT:
            value = ~wire_instruction.in_signals[0].value
        elif wire_instruction.instruction_type == InstructionType.AND:
            value = wire_instruction.in_signals[0].value & wire_instruction.in_signals[1].value
        elif wire_instruction.instruction_type == InstructionType.OR:
            value = wire_instruction.in_signals[0].value | wire_instruction.in_signals[1].value
        elif wire_instruction.instruction_type == InstructionType.LSHIFT:
            value = wire_instruction.in_signals[0].value << wire_instruction.shift_num
        else:
            value = wire_instruction.in_signals[0].value >> wire_instruction.shift_num

        value &= 0xFFFF

        print(f'[End]   {wire_instruction} ({value}; {bin(value)})')

        return value

    def get_day_1_answer(self, use_sample=False) -> str:
        return str(self.get_value_on_wire('a'))

    def get_day_2_answer(self, use_sample=False) -> str:
        a_value = self.get_value_on_wire('a')

        print('\n=====\nResetting mid-part 2.\n=====\n')

        self.reset()
        self.prepare_data(self.sample_data.input_data_2 if use_sample else self.input_data, 2)

        self.signals['b'].value = a_value

        return str(self.get_value_on_wire('a'))


if __name__ == "__main__":
    puzzle = Puzzle()
    print(puzzle.test_and_run())
