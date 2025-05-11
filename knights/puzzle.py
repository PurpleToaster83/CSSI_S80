from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(

    # A can either be a knight or knave but not both
    Biconditional(AKnight, Not(AKnave)),

    # if knight then saying knight/knave is true
    Implication(AKnight, And(AKnight, AKnave)),
    # if knave then saying knight/knave is false
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(

    # A can either be a knight or knave but not both
    Biconditional(AKnight, Not(AKnave)),

    # B can either be a knight or knave but not both
    Biconditional(BKnight, Not(BKnave)),

    # if A is knight then A/B are knaves
    Implication(AKnight, And(AKnave, BKnave)),
    # if A is knave then A/B are not knaves
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(

    # A can either be a knight or knave but not both
    Biconditional(AKnight, Not(AKnave)),

    # B can either be a knight or knave but not both
    Biconditional(BKnight, Not(BKnave)),

    # if A is knight then A and B are the same
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # if A is knave then A and B not same
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),

    # if B is knight then A and B are different
    Implication(BKnight, Or(And(AKnight, Not(BKnight)), And(AKnave, Not(BKnave)))),
    # if B is knave then A and B are same
    Implication(BKnave, Not(Or(And(AKnight, Not(BKnight)), And(AKnave, Not(BKnave)))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(

    # A can either be a knight or knave but not both
    Biconditional(AKnight, Not(AKnave)),

    # B can either be a knight or knave but not both
    Biconditional(BKnight, Not(BKnave)),

    # C can either be a knight or knave but not both
    Biconditional(CKnight, Not(CKnave)),

    # A may say "I am a knight" or "I am a knave"
    Or(

        # A says "I am a knight"
        And(
            # if A is knight then A is knight
            Implication(AKnight, AKnight),
            # if A is knave then A is not knight
            Implication(AKnave, Not(AKnight))
        ),

        # A says "I am a knave"
        And(
            # if A is knight then A is knight or knave
            Implication(AKnight, AKnave),
            # if A is knight then A is not knight or knave
            Implication(AKnave, Not(AKnave))
        )
    ),

    # if B is knight then A said "I am a knave"
    Implication(BKnight, And(Implication(AKnave, Not(AKnave)), Implication(AKnight, AKnave))),
    # if B is knave then A didn't say "I am a knave"
    Implication(BKnave, Not(And(Implication(AKnave, Not(AKnave)), Implication(AKnight, AKnave)))),

    # if B is knight then C is knave
    Implication(BKnight, CKnave),
    # if B is knave then is is not knave
    Implication(BKnave, Not(CKnave)),

    # if C is knight then A is knight
    Implication(CKnight, AKnight),
    # if C is knave then A is not Knight
    Implication(CKnave, Not(AKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
