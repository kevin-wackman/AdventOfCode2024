from filehandling import open_data_file_as_lines
from dataclasses import dataclass, field
from copy import deepcopy


DATA_FILE = "day17in.txt"

@dataclass
class Computer:
    register_A: int
    register_B: int
    register_C: int
    instruction_list: list[int]
    pointer: int = 0
    is_halted: bool = False
    print_buffer: list[int] = field(default_factory=list)

    def run_cycle(self):
        if self.pointer + 2 > len(self.instruction_list):
            self.is_halted = True
            return
        opcode = self.instruction_list[self.pointer]
        literal_operand = self.instruction_list[self.pointer + 1]
        # The pointer can be advanced now, since any jump will overwrite this
        self.pointer += 2

        if opcode == 0:
            # adv, division into A
            self.register_A = int(self.register_A / (2 ** self.get_combo_operand(literal_operand)))

        elif opcode == 1:
            # bxl, bitwise XOR of operand
            self.register_B = self.register_B ^ literal_operand

        elif opcode == 2:
            # bst, combo mod 8
            self.register_B = self.get_combo_operand(literal_operand) % 8

        elif opcode == 3:
            # jnz, jump if not zero
            if self.register_A != 0:
                self.pointer = literal_operand
        
        elif opcode == 4:
            # bxc, bitwise xor of registers
            self.register_B = self.register_B ^ self.register_C

        elif opcode == 5:
            # out, print mod 8
            self.print_buffer.append(self.get_combo_operand(literal_operand) % 8)

        elif opcode == 6:
            # bdv, division into B
            self.register_B = int(self.register_A / (2 ** self.get_combo_operand(literal_operand)))

        elif opcode == 7:
            # cdv, division into C
            self.register_C = int(self.register_A / (2 ** self.get_combo_operand(literal_operand)))

        else:
            raise ValueError("Invalid opcode {} encountered".format(opcode))

        return


    def get_combo_operand(self, literal_operand):
        if literal_operand <= 3:
            return literal_operand
        match literal_operand:
            case 4:
                return self.register_A
            case 5:
                return self.register_B
            case 6:
                return self.register_C
            case _:
                raise ValueError("Invalid operand {} found".format(literal_operand))

    def cycle_until_halt(self):
        while not self.is_halted:
            self.run_cycle()

    def get_printable_output(self):
        return ','.join(str(i) for i in self.print_buffer)
    
    def is_program_recursive(self):
        if self.is_halted:
            return self.instruction_list == self.print_buffer


def main():
    lines = open_data_file_as_lines(DATA_FILE)
    register_A = int(lines[0].split(':')[1].strip())
    register_B = int(lines[1].split(':')[1].strip())
    register_C = int(lines[2].split(':')[1].strip())
    program_string = lines[4].split(':')[1].strip()
    program = [int(n) for n in program_string.split(',')]
    comp = Computer(register_A, register_B, register_C, program)
    comp.cycle_until_halt()
    print(comp.get_printable_output())
    #register_A = 117440
    #register_B = 0
    #register_C = 0
    #program = [0,3,5,4,3,0]
    program_copy = deepcopy(program)
    working_sequences = []
    a = 0
    depth = 1
    expected_values = program_copy[-depth:]
    while a < (2 ** 10):
        comp = Computer(a, register_B, register_C, program)
        comp.cycle_until_halt()
        if comp.print_buffer[:depth] == expected_values:
            working_sequences.append(a)
        a += 1
    depth += 1
    while(depth <= len(program_copy)):
        expected_values = program_copy[-depth:]
        shift = 0
        new_working_sequences = []
        while shift < (2 ** 3):
            for old_a in working_sequences:
                a = (old_a << 3) + shift
                comp = Computer(a, register_B, register_C, program)
                comp.cycle_until_halt()
                if comp.print_buffer[:depth] == expected_values:
                    new_working_sequences.append(a)
            shift += 1
        working_sequences = new_working_sequences
        depth += 1
    print(min(working_sequences))
    n = Computer(190615597431823, register_B, register_C, program)
    n.cycle_until_halt()
    print(n.get_printable_output())


main()

