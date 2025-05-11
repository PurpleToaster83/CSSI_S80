import sys
import copy

from collections import deque
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """

        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        # iterate over each variable in the crossword puzzle
        for node in self.crossword.variables:
            word_length = node.length
            node_copy = copy.deepcopy(self.domains[node])

            # select a word from the variable domain
            for word_selection in node_copy:

                # remove the word from the variable domain if not the word length
                if len(word_selection) != word_length:
                    self.domains[node].remove(word_selection)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        revised = False

        domain_copy = copy.deepcopy(self.domains[x])

        # create variables for the overlap coordinates of the variables
        overlap = self.crossword.overlaps[x, y]

        if overlap:

            x_overlap, y_overlap = overlap

            # loop over all elements in x's domain
            for x_word in domain_copy:
                overlap = False

                # loop over all elements in y's domain
                for y_word in self.domains[y]:

                    # if the the same letter at the intersection return true
                    if x_word[x_overlap] == y_word[y_overlap]:
                        overlap = True
                        break

                # if the words do not overlap remove the word from x domain
                if not overlap:
                    self.domains[x].remove(x_word)
                    revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # if arcs is None, create a list of all arcs in the crossword
        if arcs is None:
            arcs = deque()
            for node in self.crossword.variables:
                for neighbor in self.crossword.neighbors(node):
                    arcs.append((node, neighbor))
        else:
            arcs = deque(arcs)

        # while arcs is not empty
        while arcs:

            # dequeue an arc from the arcs set
            (x, y) = arcs.popleft()

            # call revised function
            if self.revise(x, y):

                # arc consistency is not enforced if the x has no domain
                if len(self.domains[x]) == 0:
                    return False

                # create new arc to replace old one to check if all arcs with x are still consistent
                for neighbor in (self.crossword.neighbors(x)):
                    if neighbor != y:
                        arcs.append((neighbor, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        # check if any of the variables are not assigned
        for variable in self.domains:
            if variable not in assignment:
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # check if each variable is unique
        unique = set()
        for variable, value in assignment.items():
            if value not in unique:
                unique.add(value)
            else:
                return False

        # check if each variable is the correct length
        for variable in assignment:
            if len(assignment[variable]) != variable.length:
                return False

            # enumerate over every variable's neighbors
            for neighbor in self.crossword.neighbors(variable):

                # check if the variable and neighbor overlap
                if self.crossword.overlaps[(variable, neighbor)] and neighbor in assignment:

                    # (i, j) is the coordinates of the intersection of variable and neighbor
                    (i, j) = self.crossword.overlaps[(variable, neighbor)]

                    # check if the ith letter of varible is not the jth letter of neighbor
                    if assignment[variable][i] != assignment[neighbor][j]:
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        ruled_out_list = {}

        # loop over each domain value for the variable
        for var_domain in self.domains[var]:
            ruled_out_list[var_domain] = 0

            # loop over each of the variable's neighbors
            for neighbor in self.crossword.neighbors(var):

                if neighbor not in assignment:

                    # get the coordinates of the neighbor and varable's overlap
                    (i, j) = self.crossword.overlaps[var, neighbor]

                    # loop over the neighbor's domain values
                    for neighbor_domain in self.domains[neighbor]:

                        # if the intersection doesn't match, increase the ruled_out_list
                        if var_domain[i] != neighbor_domain[j]:
                            ruled_out_list[var_domain] += 1

        return sorted(ruled_out_list, key=ruled_out_list.get)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        best_var = None

        for variable in self.domains:
            if variable not in assignment:

                # set best_var equal to variable according to minimum remaining value heuristic
                if best_var is None or len(self.domains[variable]) < len(self.domains[best_var]):
                    best_var = variable

                # set best_var equal to variable according to degree heuristic
                elif len(self.domains[variable]) == len(self.domains[best_var]) \
                    and len(self.crossword.neighbors(variable)) > len(self.crossword.neighbors(best_var)):
                    best_var = variable

        return best_var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # if the assignment is complete the crossword has been solved
        if self.assignment_complete(assignment):
            return assignment

        # select an unassigned variable
        var = self.select_unassigned_variable(assignment)

        # loop over the variable's domain values
        for value in self.order_domain_values(var, assignment):

            assignment_copy = assignment.copy()

            # add value with key of variable to the assignment dict
            assignment_copy.update({var: value})

            # check that the assignment is consistent
            if self.consistent(assignment_copy):

                # create a new list of arcs by iterating over neighboring variables
                arc = []
                for variable in self.crossword.variables:
                    if variable not in assignment:
                        for n in self.crossword.neighbors(variable):
                            arc.append((variable, n))

                # use arc list to check inferance consistency
                self.ac3(arc)

                # recursivley call backtrack and return resulting assignment
                result = self.backtrack(assignment_copy)
                if result is not None:
                    return result

        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
