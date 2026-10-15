from pathlib import Path

from environment import Environment
from virtmachine import VirtualMachine


folder = Path(__file__).resolve().parent

# Load the map.
with open(folder / "map.txt", encoding="utf-8") as file:
    rows, columns = map(int, file.readline().split())
    start = tuple(map(int, file.readline().split()))
    treasure_count = int(file.readline())

    treasures = [
        tuple(map(int, file.readline().split()))
        for _ in range(treasure_count)
    ]

environment = Environment(rows, columns, start, treasures)

# Load the VM's initial memory.
with open(folder / "program.txt", encoding="utf-8") as file:
    program = [int(value) for value in file.read().split()]

if len(program) != 64:
    raise ValueError("The program must contain exactly 64 numbers.")

if any(value < 0 or value > 255 for value in program):
    raise ValueError("Every memory value must be between 0 and 255.")

vm = VirtualMachine(environment)

print("Before execution:")
environment.display()

fitness = vm.run(program)

print("\nAfter execution:")
environment.display()

print("Output:", vm.output)
print("Treasures collected:", fitness)
print("Instructions executed:", vm.instructions_executed)