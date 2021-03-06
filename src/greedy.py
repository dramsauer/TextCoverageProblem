import random
from collections import defaultdict
from copy import deepcopy

from src.preprocesses import sort_collection_by_set_sizes_with_comparison_list


def greedy_by_balas(sets, elements, print_logs=False):
    """
    Find a feasible solution for the set cover problem with greedy heuristic.

    This algorithm was found in:
        Jacobs, L. W., & Brusco, M. J. (1995). Note: A local‐search heuristic for large set‐covering problems.
        Naval Research Logistics (NRL), 42(7), 1129-1140.
    They based this algorithm on an approach by:
        Balas, E., & Ho, A. (1980). Set covering algorithms using cutting planes, heuristics, and subgradient
        optimization: a computational study. In Combinatorial optimization (pp. 37-60). Springer, Berlin, Heidelberg.
    :param sets: collection of sets; with set_collection as a copy of it
    :param elements: set of words/elements to be covered; with words_to_cover as a copy of it
    :param print_logs: prints outputs and parameters of used functions.
    :return: solution set containing a sub-collection of indices of set_collection; <class 'set'>

    """
    print("\n\n____________________\n")
    print("| Greedy Heuristic |")
    print()


    """
    Initialization & Pre-processes
    """

    print("\nInitialization.")

    set_collection = deepcopy(sets)
    sorted_collection, comparison_list = sort_collection_by_set_sizes_with_comparison_list(set_collection)

    words_to_cover = list(deepcopy(elements))
    amount_uncovered_words = len(words_to_cover)

    solution_indices = list()

    """
    Main-Algorithm
    """

    print("\nLoop.")
    print("Iterating over all words that need to get covered...")

    # Iterating over all words that need to get covered (= step 3 in paper also)
    while amount_uncovered_words > 0:
        # 1. Select randomly one of the words
        random_index = random.randint(0, amount_uncovered_words-1)
        random_word = words_to_cover[random_index]

        # 2. Select first set in natural order
        for set_i in sorted_collection:
            # If the random word is part of the current chosen set,
            # then add the index of the set to solution_indices
            if random_word in set_i:

                sorted_set_index = sorted_collection.index(set_i)
                original_set_index = comparison_list[sorted_set_index]

                solution_indices.append(original_set_index)
                break

        words_to_cover.remove(random_word)
        amount_uncovered_words -= 1

    # 4. Remove redundant entries in list by saving it as a set
    solution_indices = set(solution_indices)



    if print_logs:
        print("Amount of indices in Greedy-Solution: ", len(solution_indices))
    print("____________________\n\n")

    return solution_indices


def greedy_by_balas_with_coverage_matrix(sets, elements, print_logs=False):
    """
    Find a feasible solution for the set cover problem with greedy heuristic.

    This algorithm was found in:
        Jacobs, L. W., & Brusco, M. J. (1995). Note: A local‐search heuristic for large set‐covering problems.
        Naval Research Logistics (NRL), 42(7), 1129-1140.
    They based this algorithm on an approach by:
        Balas, E., & Ho, A. (1980). Set covering algorithms using cutting planes, heuristics, and subgradient
        optimization: a computational study. In Combinatorial optimization (pp. 37-60). Springer, Berlin, Heidelberg.
    :param sets: collection of sets; with set_collection as a copy of it
    :param elements: set of words/elements to be covered; with words_to_cover as a copy of it
    :param print_logs: prints outputs and parameters of used functions.
    :return: solution set containing a sub-collection of indices of set_collection; <class 'set'> and a dict which saves the numbers, how often each element is covered

    """
    print("\n\n____________________\n")
    print("| Greedy Heuristic |")
    print()


    """
    Initialization & Pre-processes
    """

    print("\nInitialization.")

    set_collection = deepcopy(sets)
    sorted_collection, comparison_list = sort_collection_by_set_sizes_with_comparison_list(set_collection)

    words_to_cover = list(deepcopy(elements))
    words_to_cover_dict = defaultdict()
    for word in words_to_cover:
        words_to_cover_dict[word] = 0
    amount_uncovered_words = len(words_to_cover)

    solution_indices = list()

    """
    Main-Algorithm
    """

    print("\nLoop.")
    print("Iterating over all words that need to get covered...")

    # Iterating over all words that need to get covered (= step 3 in paper also)
    while amount_uncovered_words > 0:
        # 1. Select randomly one of the words
        random_index = random.randint(0, amount_uncovered_words-1)
        random_word = words_to_cover[random_index]

        # 2. Select first set in natural order
        for set_i in sorted_collection:
            # If the random word is part of the current chosen set,
            # then add the index of the set to solution_indices
            if random_word in set_i:

                sorted_set_index = sorted_collection.index(set_i)
                original_set_index = comparison_list[sorted_set_index]

                solution_indices.append(original_set_index)
                break

        words_to_cover.remove(random_word)
        words_to_cover_dict[random_word] += 1
        amount_uncovered_words -= 1

    # 4. Remove redundant entries in list by saving it as a set
    solution_indices = set(solution_indices)



    if print_logs:
        print("Amount of indices in Greedy-Solution: ", len(solution_indices))
    print("____________________\n\n")

    return solution_indices, words_to_cover_dict
