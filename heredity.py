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

    # calculate the probability that everyone in set 'one gene' has one copy of the gene
    one_gene_probabilities = []
    for person in one_gene:
        # check who the parents of the person are
        person_mother = people[person]['mother']
        person_father = people[person]['father']

        # if person has no parents, use the probability distribution PROBS['genes']
        if person_father and person_mother == None:
            one_gene_probabilities.append(PROBS['genes'][1])

        # either person gets the gene from his mother and not his father
        # or he gets it from his father and not his mother
        if person_father in one_gene:
            father_passing_probability = 0.49 # 0.5 - 0.01 (the probability of mutation to not the specified gene)
        if person_father in two_genes:
            father_passing_probability = 0.99 # 1 - 0.01 (the probability of mutation to not the specified gene)
        else:
            father_passing_probability = 0.01 # (the probability of not the specified gene mutating into the specified gene)


        if person_mother in one_gene:
            mother_passing_probability = 0.49 # 0.5 - 0.01 (the probability of mutation to not the specified gene)
        if person_father in two_genes:
            mother_passing_probability = 0.99 # 1 - 0.01 (the probability of mutation to not the specified gene)
        else:
            mother_passing_probability = 0.01 # (the probability of not the specified gene mutating into the specified gene)
        
        # probability = gets gene ONLY from mother OR gets gene ONLY from father
        probability = mother_passing_probability * (1 - father_passing_probability) + (1 - mother_passing_probability) * father_passing_probability
        # add the probability of person having one gene to the list of probabilities
        one_gene_probabilities.append(probability)

    two_genes_probabilities = []
    for person in two_genes_probabilities:
        # check who the parents of the person are
        person_mother = people[person]['mother']
        person_father = people[person]['father']

        # if person has no parents, use the probability distribution PROBS['genes']
        if person_father and person_mother == None:
            two_genes_probabilities.append(PROBS['genes'][2])

        # check probability of passing the gene by persons parents
        if person_father in one_gene:
            father_passing_probability = 0.49 # 0.5 - 0.01 (the probability of mutation to not the specified gene)
        if person_father in two_genes:
            father_passing_probability = 0.99 # 1 - 0.01 (the probability of mutation to not the specified gene)
        else:
            father_passing_probability = 0.01 # (the probability of not the specified gene mutating into the specified gene)


        if person_mother in one_gene:
            mother_passing_probability = 0.49 # 0.5 - 0.01 (the probability of mutation to not the specified gene)
        if person_father in two_genes:
            mother_passing_probability = 0.99 # 1 - 0.01 (the probability of mutation to not the specified gene)
        else:
            mother_passing_probability = 0.01 # (the probability of not the specified gene mutating into the specified gene)

        # probability = mother passed the gene AND father passed the gene
        two_genes_probability = mother_passing_probability * father_passing_probability
        # add the probability of person having the gene to list of probabilities
        two_genes_probabilities.append(two_genes_probability)

    no_gene_probabilities = []
    # get a list of all people not in one_gene or two_gene
    no_gene_people = []
    for person in people:
        if person not in one_gene and person not in two_genes:
            no_gene_people.append(person)
    
    for person in no_gene_people:
        # check who the parents of the person are
        person_mother = people[person]['mother']
        person_father = people[person]['father']

        # if person has no parents, use the probability distribution PROBS['genes']
        if person_father and person_mother == None:
            two_genes_probabilities.append(PROBS['genes'][0])
        
        # check probability of passing the gene by persons parents
        if person_father in one_gene:
            father_passing_probability = 0.49 # 0.5 - 0.01 (the probability of mutation to not the specified gene)
        if person_father in two_genes:
            father_passing_probability = 0.99 # 1 - 0.01 (the probability of mutation to not the specified gene)
        else:
            father_passing_probability = 0.01 # (the probability of not the specified gene mutating into the specified gene)


        if person_mother in one_gene:
            mother_passing_probability = 0.49 # 0.5 - 0.01 (the probability of mutation to not the specified gene)
        if person_father in two_genes:
            mother_passing_probability = 0.99 # 1 - 0.01 (the probability of mutation to not the specified gene)
        else:
            mother_passing_probability = 0.01 # (the probability of not the specified gene mutating into the specified gene)

        # probability = father NOT passing gene AND mother NOT passing gene
        probability = (1 - mother_passing_probability)  * (1 - father_passing_probability)

        no_gene_probabilities.append(probability)

    # calculate probabilities for persons to have trait
    have_trait_probabilities = []
    for person in have_trait:
        # calculate probability of trait, given 0 genes
        if person not in one_gene and person not in two_genes:
            probability = PROBS['trait'][0][True]
        # calculate probability of trait, given 1 gene
        if person in one_gene:
            probability = PROBS['trait'][1][True]
        # calculate probability of trait, given 2 genes
        if person in two_genes:
            probability = PROBS['trait'][2][True]

        have_trait_probabilities.append(probability)

    # calculate probabilities for persons to not have trait
    not_have_trait_probabilities = []
    for person in people:
        if person not in have_trait:
            # calculate probability of no trait, given 0 genes
            if person not in one_gene and person not in two_genes:
                probability = PROBS['trait'][0][False]
            # calculate probability of no trait, given 1 gene
            if person in one_gene:
                probability = PROBS['trait'][1][False]
            # calculate probability of no trait, given 2 genes
            if person in two_genes:
                probability = PROBS['trait'][2][False]
            
            not_have_trait_probabilities.append(probability)

    all_probabilities = one_gene_probabilities + two_genes_probabilities + no_gene_probabilities + have_trait_probabilities + not_have_trait_probabilities

    final_probability = 1

    for probability in all_probabilities:
        final_probability = final_probability * probability


    return final_probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person not in one_gene and person not in two_genes:
            probabilities[person]['gene'][0] = probabilities[person]['gene'][0] + p

        if person in one_gene:
            probabilities[person]['gene'][1] = probabilities[person]['gene'][1] + p

        if person in two_genes:
            probabilities[person]['gene'][2] = probabilities[person]['gene'][2] + p
        
        if person in have_trait:
            probabilities[person]['trait'][True] = probabilities[person]['trait'][True] + p

        if person not in have_trait:
            probabilities[person]['trait'][False] = probabilities[person]['trait'][False] + p
    print("\n\n\n\n\n\n\n\n\n\n")
    print(have_trait)
    print(probabilities)



def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        for gene_trait in probabilities[person]:
            total_distribution = 0
            for category in probabilities[person][gene_trait]:
                total_distribution = total_distribution + probabilities[person][gene_trait][category]

            for category in probabilities[person][gene_trait]:
                probabilities[person][gene_trait][category] = float(probabilities[person][gene_trait][category]) / total_distribution



if __name__ == "__main__":
    main()
