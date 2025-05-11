import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        # if the number of cells is the same as the count then all are definitivly mines
        if len(self.cells) == self.count and self.count != 0:
            return self.cells

        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        # if the count is equal to zero then all of the cells are safe
        if self.count == 0:
            return self.cells

        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        # check if the mine is in the cell set. If so, remove from set
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        # check if the safe cell is in the cell set. If so, remove from set
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # add the cell to the moves_made set
        self.moves_made.add(cell)

        # add cell to safe set and update sentences with cell
        self.mark_safe(cell)

        neighbors = set()
        row = cell[0]
        column = cell[1]

        # find all valid neighbors for a cell
        for neighbors_r in range(-1, 2):
            for neighbors_c in range(-1, 2):
                if (neighbors_r != 0 or neighbors_c != 0):
                    if 0 <= neighbors_r + row < self.height and 0 <= neighbors_c + column < self.width:
                        neighbors.add((neighbors_r + row, neighbors_c + column))

        # take intersection so you can decrease the count by the amount of known neighbor mines
        count_neighbor_mines = len(neighbors.intersection(self.mines))

        # remove known cells from the set
        unknown_moves = neighbors.difference(self.safes)
        unknown_moves = unknown_moves.difference(self.mines)

        # add new neighbor info
        if len(unknown_moves) > 0:
            self.knowledge.append(Sentence(unknown_moves, count - count_neighbor_mines))

        # update knowledge based on new sentence and try to infer new knowledge
        self.update_knowledge()
        self.infer_knowledge()

    def update_knowledge(self):
        """Recursively updates the knowledge based on the new sentence"""

        # make a deep copy so the knowledge base in't messed up
        knowledge_copy = copy.deepcopy(self.knowledge)

        # loop over sentences in knowledge
        for sentence in knowledge_copy:

            # check if the length of the sentence is 0 as break case
            if len(sentence.cells) == 0 and sentence in self.knowledge:
                self.knowledge.remove(sentence)

            else:

                mine_cells = sentence.known_mines()
                safe_cells = sentence.known_safes()

                # mark known mines and recursivly call update knowledge
                if mine_cells:
                    for mine in mine_cells:
                        self.mark_mine(mine)
                        self.update_knowledge()

                # mark known safes and recursivly call update knowledge
                if safe_cells:
                    for safe in safe_cells:
                        self.mark_safe(safe)
                        self.update_knowledge()

    def infer_knowledge(self):
        knowledge_copy = copy.deepcopy(self.knowledge)

        # check if there are sentences that are subsets of other sentences
        for sentence1 in knowledge_copy:
            if len(sentence1.cells) > 0:
                for sentence2 in knowledge_copy:
                    if len(sentence2.cells) > 0 and sentence1.cells.issubset(sentence2.cells) and sentence1.cells != sentence2.cells:

                        # create a new sentence that is the differance between sentences 1 and 2
                        infered_sentence = Sentence(
                            sentence2.cells - sentence1.cells, sentence2.count - sentence1.count)

                        # check if the new sentence is already in knowledge. If not, add it
                        if len(infered_sentence.cells) > 0 and infered_sentence not in self.knowledge:
                            self.knowledge.append(infered_sentence)

                            mine_cells = copy.deepcopy(infered_sentence.known_mines())
                            safe_cells = copy.deepcopy(infered_sentence.known_safes())

                            # mark known mines
                            if mine_cells:
                                for mine in mine_cells:
                                    self.mark_mine(mine)

                            # mark known safes
                            if safe_cells:
                                for safe in safe_cells:
                                    self.mark_safe(safe)

                            # check if sentence empty. If so, remove to reduce computation
                            if len(sentence2.cells) == 0 and sentence2 in self.knowledge:
                                self.knowledge.remove(sentence2)

                            # recursively call infer_knowledge to check knowledge with infered sentence
                            self.infer_knowledge()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        available_safe = self.safes - self.moves_made

        # if the safe set is empty return None
        if len(available_safe) == 0:
            return None

        # return the first move from the available_safe set
        return available_safe.pop()

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        other_moves = set()

        # put all moves into other moves set
        for i in range(self.height):
            for j in range(self.width):
                other_moves.add((i, j))

        # remove the moves that are mines or that have been made
        other_moves = other_moves - self.mines - self.moves_made

        # if other_moves is empty return None
        if len(other_moves) == 0:
            return None

        # select random move from other_moves
        return random.choice(list(other_moves))
