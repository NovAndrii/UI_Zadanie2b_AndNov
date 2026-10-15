class Environment:
    def __init__(self, rows, columns, start, treasures):
        self.rows = rows
        self.columns = columns

        self.start = start
        self.position = start

        self.initial_treasures = set(treasures)
        self.remaining_treasures = set(treasures)

        self.treasures_found = 0
        self.moves_count = 0


    def reset(self):
        self.position = self.start
        self.remaining_treasures = self.initial_treasures.copy()
        self.treasures_found = 0
        self.moves_count = 0    


    def move(self, direction):
        row, column = self.position

        if(direction == "H"):
            if(row - 1 >= 0):
                row -= 1
                self.moves_count += 1
                

            else:
                print("Out of Grid")
                return False
        elif(direction == "D"):
            if(row + 1 <= self.rows):
                row += 1
                self.moves_count += 1
                

            else:
                print("Out of Grid")
                return False
        elif(direction == "L"):
            if(column - 1 >= 0):
                column -= 1
                self.moves_count += 1

            else:
                print("Out of Grid")
                return False
        elif(direction == "P"):
            if(column + 1 <= self.columns):
                column += 1
                self.moves_count += 1

            else:
                print("Out of Grid")
                return False 
        else:   
            print("There is no such an operation")

        self.position = (row, column)


        if self.position in self.remaining_treasures:
            self.treasures_found += 1
            self.remaining_treasures.remove(self.position)
            
        return True
        


    def all_collected(self):
        return len(self.remaining_treasures) == 0



    def display(self):
        for row in range(self.rows):
            cells = []

            for column in range(self.columns):
                position = (row, column)

                if position == self.position:
                    cells.append("A")
                elif position in self.remaining_treasures:
                    cells.append("T")
                elif position == self.start:
                    cells.append("S")
                else:
                    cells.append(".")

            print(" ".join(cells))

        print(f"Position: {self.position}")
        print(f"Treasures found: {self.treasures_found}")
        print(f"Moves: {self.moves_count}")      

        



environment = Environment(
    rows=5,
    columns=5,
    start=(0, 0),
    treasures=[(0, 2), (2, 3), (4, 1)]
)

environment.display()

environment.move('R')
environment.display()
environment.move('R')
environment.display()
environment.move('D')
environment.display()



        