class VirtualMachine:
    def __init__(self, environment):
        self.environment = environment
        self.memory = [0] * 64
        self.instruction_pointer = 0
        self.instructions_executed = 0
        self.output = []

    def load_program(self, program):
        self.memory = program.copy()
        self.instruction_pointer = 0
        self.instructions_executed = 0
        self.output = []
        self.environment.reset()

    def step(self):
        instruction = self.memory[self.instruction_pointer]

        operation = instruction >> 6
        address = instruction & 63 # here I use AND with 63 to get only 6 bits

        
        if operation == 0:
            self.memory[address] = (self.memory[address] + 1) % 256
        elif operation == 1:
            self.memory[address] = (self.memory[address] - 1) % 256
        elif operation == 2:
            self.instruction_pointer = address
        elif operation == 3:
            directions = ["H", "D", "P", "L"]
            direction = directions[self.memory[address] % 4]
            self.output.append(direction)

            if not self.environment.move(direction):
                self.instructions_executed += 1
                return False

        if operation != 2: # since if it is 2 then jump has already set a new instruction
            self.instruction_pointer = (self.instruction_pointer + 1) % 64

        self.instructions_executed += 1
        return True

    def run(self, program):
        self.load_program(program)

        while self.instructions_executed < 500:
            if self.environment.all_collected():
                break

            if not self.step():
                break

        return self.environment.treasures_found


