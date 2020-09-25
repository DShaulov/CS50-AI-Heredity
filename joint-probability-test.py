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




def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.
``
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
        if person_father == None:
            if person_mother == None:
                one_gene_probabilities.append(PROBS['gene'][1])
                continue

        # either person gets the gene from his mother and not his father
        # or he gets it from his father and not his mother
        if person_father in one_gene:
            father_passing_probability = 0.49 # 0.5 - 0.01 (the probability of mutation to not the specified gene)
        elif person_father in two_genes:
            father_passing_probability = 0.99 # 1 - 0.01 (the probability of mutation to not the specified gene)
        else:
            father_passing_probability = 0.01 # (the probability of not the specified gene mutating into the specified gene)


        if person_mother in one_gene:
            mother_passing_probability = 0.49 # 0.5 - 0.01 (the probability of mutation to not the specified gene)
        elif person_mother in two_genes:
            mother_passing_probability = 0.99 # 1 - 0.01 (the probability of mutation to not the specified gene)
        else:
            mother_passing_probability = 0.01 # (the probability of not the specified gene mutating into the specified gene)
        
        # probability = gets gene ONLY from mother OR gets gene ONLY from father
        probability = mother_passing_probability * (1 - father_passing_probability) + (1 - mother_passing_probability) * father_passing_probability
        # add the probability of person having one gene to the list of probabilities
        one_gene_probabilities.append(probability)

    two_genes_probabilities = []
    for person in two_genes:
        # check who the parents of the person are
        person_mother = people[person]['mother']
        person_father = people[person]['father']

        # if person has no parents, use the probability distribution PROBS['genes']
        if person_father == None:
            if person_mother == None:
                two_genes_probabilities.append(PROBS['gene'][2])
                continue

        # check probability of passing the gene by persons parents
        if person_father in one_gene:
            father_passing_probability = 0.49 # 0.5 - 0.01 (the probability of mutation to not the specified gene)
        elif person_father in two_genes:
            father_passing_probability = 0.99 # 1 - 0.01 (the probability of mutation to not the specified gene)
        else:
            father_passing_probability = 0.01 # (the probability of not the specified gene mutating into the specified gene)


        if person_mother in one_gene:
            mother_passing_probability = 0.49 # 0.5 - 0.01 (the probability of mutation to not the specified gene)
        elif person_father in two_genes:
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
        if person_father == None:
            if person_mother == None:
                no_gene_probabilities.append(PROBS['gene'][0])
                continue
        
        # check probability of passing the gene by persons parents
        if person_father in one_gene:
            father_passing_probability = 0.49 # 0.5 - 0.01 (the probability of mutation to not the specified gene)
        elif person_father in two_genes:
            father_passing_probability = 0.99 # 1 - 0.01 (the probability of mutation to not the specified gene)
        else:
            father_passing_probability = 0.01 # (the probability of not the specified gene mutating into the specified gene)


        if person_mother in one_gene:
            mother_passing_probability = 0.49 # 0.5 - 0.01 (the probability of mutation to not the specified gene)
        elif person_mother in two_genes:
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

if __name__ == '__main__':
    people = {
    'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
    'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
    'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
    }
    print(joint_probability(people, {"Harry","Lily"}, {"James"}, {"Harry", "Lily", "James"}))







