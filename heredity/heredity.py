import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    # create a variable to represent the joint probability
    probability = 1

    # for every person in family dataset
    for person in people:
        mother = people[person]['mother']
        father = people[person]['father']

        # index "gene" depending on person's genotype
        if person in two_genes:
            gene_copies = 2
        elif person in one_gene:
            gene_copies = 1
        else:
            gene_copies = 0

        # index "trait" depending on the person's phenotype
        trait_show = person in have_trait

        # multiply phenotype and genotype probabilities by running joint probability
        if not mother or not father:
            probability *= PROBS["gene"][gene_copies] * PROBS['trait'][gene_copies][trait_show]

        else:
            parents = set({mother, father})
            parent_pass = {}

            # calculate the probability of receiving the gene from each parent
            for parent in parents:
                if parent in two_genes:
                    parent_pass[parent] = 1 - PROBS["mutation"]
                elif parent in one_gene:
                    parent_pass[parent] = 0.5
                else:
                    parent_pass[parent] = PROBS["mutation"]

            # calculate the probability of a child's phenotype
            if person in two_genes:
                child_p = parent_pass[father] * parent_pass[mother]
            elif person in one_gene:
                child_p = (parent_pass[mother] * (1 - parent_pass[father])
                           + parent_pass[father] * (1 - parent_pass[mother]))
            else:
                child_p = (1 - parent_pass[father]) * (1 - parent_pass[mother])

            # multiply child node phenotype and genotype probabilities to get joint probability
            probability *= child_p * PROBS['trait'][gene_copies][trait_show]

    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    # update for every person
    for person in probabilities:

        # determine how many copies of the gene they have
        if person in two_genes:
            gene_copies = 2
        elif person in one_gene:
            gene_copies = 1
        else:
            gene_copies = 0

        # update the probability of the person having the genotype
        probabilities[person]["gene"][gene_copies] += p

        # update the probability based on if they display the trait or not
        trait_show = person in have_trait
        probabilities[person]["trait"][trait_show] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    # for each person in probability
    for person in probabilities:

        genes = probabilities[person]["gene"]
        traits = probabilities[person]["trait"]

        # normalizing coefficient are 1 divided by the sum of the dict values
        gene_coef = 1/sum(genes.values())
        trait_coef = 1/sum(traits.values())

        # multiply each value by it's normalizing coefficient
        for gene_num in genes:
            genes[gene_num] *= gene_coef

        for trait_bool in traits:
            traits[trait_bool] *= trait_coef


if __name__ == "__main__":
    main()
