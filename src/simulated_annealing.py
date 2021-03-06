import math
import random
import time
from collections import defaultdict
from copy import deepcopy

from src.preprocesses import *
from text_coverage_data import sets_universe


def simulated_annealing(sets, predefined_solution, amount_elements_covered_dict, running_time, neighbourhood_scale=0.001, search_depth=2, temp=1.3, temp_length=5, cooling_factor=0.9, print_logs=False):
    """
    Find a feasible solution for the set cover problem with greedy heuristic and optimize the solution via
    simulated annealing.

    This algorithm is the main contribution of:
        Jacobs, L. W., & Brusco, M. J. (1995). Note: A local‐search heuristic for large set‐covering problems.
        Naval Research Logistics (NRL), 42(7), 1129-1140.

    :param sets: collection of len_set_collection subsets / and a copy of it; = sets_universe

    :param predefined_solution: for multiple iterations of testing you can give this method a feasable solution to start with
    :param amount_elements_covered_dict: a dict which saves the numbers, how often each element is covered

    :param temp: initial temperature - controls the probability of accepting an inferior solution
    :param temp_length: number of iterations at a particular value of the temperature
    :param cooling_factor: percentage by which the temperature is reduced after temp_length iterations
    :param running_time: maximum computation time

    :param neighbourhood_scale: percentage of sets in tentative solution to be removed at each iteration; magnitude of neighbourhood-search
    :param search_depth: percentage of set cost(=length) that is accepted for new solution at each iteration; control for search-depth

    :param print_logs: prints outputs and parameters of used functions.

    :return: solution set containing a sub-collection of indices of set_collection
    """

    print("+---------------------+")
    print("| Simulated Annealing |")
    print("+---------------------+\n")

    """
    Initialization
    """
    set_collection = deepcopy(sets)


    solution = predefined_solution
    solution_cost = len(solution)
    solution_elements_covered_dict = amount_elements_covered_dict
    best_solution = solution

    if print_logs:
        print("Starting simulated annealing with solution size:", solution_cost)

    start_time = time.time()
    iterations = 0
    while True:
        i = 1
        while i <= temp_length:
            new_solution, new_solution_elements_dict = local_search_heuristic_simplified(set_collection, solution, solution_elements_covered_dict, neighbourhood_scale, print_logs)
            new_cost = len(new_solution)
            iterations += 1
            delta = new_cost - solution_cost
            if delta <= 0:
                solution = new_solution
                solution_cost = new_cost
                solution_elements_covered_dict = new_solution_elements_dict
                best_solution = new_solution
                if print_logs:
                    print("+-----------------------------+")
                    print("| New best solution found!    |")
                    print("| It has ", len(best_solution), " sets.")
                    print("+-----------------------------+")

            else:
                # When delta is less than zero, then exp( -(-delta) / temp )
                # 1) if delta is low, the probability for a change of the solution gets high
                # 2) if temperature is low, the probability for a change of the solution gets high
                prob = math.pow(math.e, (-delta)/temp)
                if prob > random.random():
                    solution = new_solution
                    solution_cost = new_cost
                    solution_elements_covered_dict = new_solution_elements_dict
                    if print_logs:
                        print("+------------------------------+")
                        print("| Accepted a inferior solution |")
                        print("| It has ", len(best_solution), " sets.")
                        print("+------------------------------+")

            i += 1
        temp = temp * cooling_factor

        if print_logs:
            print("+-------------------------------+")
            print("| Cooling temperature down: ", round(temp, 4))
            print("+-------------------------------+")

        if (time.time() - start_time) > running_time:
            break
    return best_solution, iterations



def local_search_heuristic_simplified(sets, solution, amount_elements_covered_dict, neighbourhood_scale=0.001, print_logs=False):
    """
    This algorithm is based on:
        Jacobs, L. W., & Brusco, M. J. (1995). Note: A local‐search heuristic for large set‐covering problems.
        Naval Research Logistics (NRL), 42(7), 1129-1140.

    :param sets: collection of len_set_collection subsets / and a copy of it; = sets_universe

    :param solution: a feasible solution to start with
    :param amount_elements_covered_dict: a dict which saves the numbers, how often each element is covered

    :param neighbourhood_scale: percentage of sets in tentative solution to be removed at each iteration; magnitude of neighbourhood-search

    :param print_logs: prints outputs and parameters of used functions.
    :return: solution set containing a sub-collection of indices of set_collection
    """

    if print_logs:
        print("\n")
        print("| Local-Search-Heuristic |")
        print()



    """
    Initialization & Pre-processes
    """

    feasible_solution = solution
    amount_elements_covered_dict = amount_elements_covered_dict


    set_collection = deepcopy(sets)


    # 0.
    current_solution_list_indices = list(feasible_solution)

    d = 0
    D = neighbourhood_scale * len(current_solution_list_indices)

    not_in_solution = list()


    """
    Main Algorithm
    """
    if print_logs:
        print("Removing sets from solution randomly...")

    while d <= D:
        # 1. Randomly select a set from solution
        current_set_index = random.choice(current_solution_list_indices)

        # 2. Move the set from solution to not-covered;
        not_in_solution.append(current_set_index)
        current_solution_list_indices.remove(current_set_index)

        for element in set_collection[current_set_index]:
            amount_elements_covered_dict[element] -= 1

        d += 1

    # Getting a complete indices list of sets, that are currently not in the solution
    for j in range(0, len(set_collection)):
        if j in current_solution_list_indices:
            continue
        else:
            not_in_solution.append(j)

    if print_logs:
        print("Sets, that are currently not in solution: ", len(not_in_solution))


    if print_logs:
        print("\nCheck which elements now got uncovered...")
        print("Checking which sets can be brought into solution \n")

    added_to_solution = list()
    uncovered_elements_existing = True
    # If all elements are still covered, go to step 6, otherwise continue with step 4.
    while uncovered_elements_existing: # should be True if that dict has entries!
        # 3. Update the dict: set the elements that are still covered (-> value is higher than 0)
        uncovered_count = 0
        for element in amount_elements_covered_dict:
            if amount_elements_covered_dict[element] == 0:
                uncovered_count += 1


        if uncovered_count == 0:
            break


        random_set = random.choice(not_in_solution)

        add_random_set_to_solution = False
        for element in set_collection[random_set]:
            if amount_elements_covered_dict[element] != 0:
                continue
            else:
                amount_elements_covered_dict[element] += 1
                add_random_set_to_solution = True


        if add_random_set_to_solution:
            current_solution_list_indices.append(random_set)
            added_to_solution.append(random_set)
            #if print_logs:
            #    print("Set added!", "Uncovered Words: ", uncovered_count)

        not_in_solution.remove(random_set)
        if len(not_in_solution) == 0:
            break


    # 6. Remove all duplicates
    solution_indices = set(current_solution_list_indices)

    if print_logs:
        print("Added sets: ", len(added_to_solution), "Difference: len(Solution-now) - len(Solution-before)  = ", len(solution_indices)-len(solution))


    return solution_indices, amount_elements_covered_dict


def local_search_heuristic(sets, solution, amount_elements_covered_dict, neighbourhood_scale=0.001, search_depth=2, print_logs=False):
    """
    This algorithm is the main contribution of:
        Jacobs, L. W., & Brusco, M. J. (1995). Note: A local‐search heuristic for large set‐covering problems.
        Naval Research Logistics (NRL), 42(7), 1129-1140.

    :param sets: collection of len_set_collection subsets / and a copy of it; = sets_universe

    :param solution: a feasible solution to start with
    :param amount_elements_covered_dict: a dict which saves the numbers, how often each element is covered

    :param neighbourhood_scale: percentage of sets in tentative solution to be removed at each iteration; magnitude of neighbourhood-search
    :param search_depth: percentage of set cost(=length) that is accepted for new solution at each iteration; control for search-depth

    :param print_logs: prints outputs and parameters of used functions.
    :return: solution set containing a sub-collection of indices of set_collection
    """

    if print_logs:
        print("\n")
        print("| Local-Search-Heuristic |")
        print()



    """
    Initialization & Pre-processes
    """

    feasible_solution = solution
    amount_elements_covered_dict = amount_elements_covered_dict


    set_collection = deepcopy(sets)


    # 0.
    if print_logs:
        print("Initialization.")

    current_solution_list_indices = list(feasible_solution)

    set_lengths = compute_set_lengths(get_set_list_of_solution_indices(collection=set_collection, solution_indices=current_solution_list_indices))
    d = 0
    D = neighbourhood_scale * len(current_solution_list_indices)
    maximum_set_length_allowed = max(set_lengths) * search_depth

    not_in_solution = list()


    """
    Main Algorithm
    """
    if print_logs:
        print("\nMain Algorithm.")
        print("Solution optimization by simulated annealing approach")
        print("Removing sets from solution randomly...")

    while d <= D:
        # 1. Randomly select a set from solution
        current_set_index = random.choice(current_solution_list_indices)

        # 2. Move the set from solution to not-covered;
        not_in_solution.append(current_set_index)
        current_solution_list_indices.remove(current_set_index)

        for element in set_collection[current_set_index]:
            amount_elements_covered_dict[element] -= 1

        d += 1

    # Getting a complete indices list of sets, that are currently not in the solution
    for j in range(0, len(set_collection)):
        if j in current_solution_list_indices:
            continue
        else:
            not_in_solution.append(j)

    if print_logs:
        print("Set, that are currently not in solution: ", len(not_in_solution))


    if print_logs:
        print("\nCheck which elements now got uncovered...")
        print("Checking which sets are short enough to be brought into solution again")
        print("and how many elements get 'recovered' by those sets...\n")
        print("---Amount Elements covered now: ", len(amount_elements_covered_dict), "\n")


    added_to_solution = list()
    uncovered_elements_existing = True
    # If all elements are still covered, go to step 6, otherwise continue with step 4.
    while uncovered_elements_existing: # should be True if that dict has entries!
        # 3. Update the dict: set the elements that are still covered (-> value is higher than 0)
        uncovered_count = 0
        for element in amount_elements_covered_dict:
            if amount_elements_covered_dict[element] == 0:
                uncovered_count += 1

        #if print_logs:
        #    print("Uncovered Words: ", uncovered_count)

        if uncovered_count == 0:
            break


        # 4. Make a dict of sets which have a length that lower-equals maximum_set_length_allowed
        # and recover enough uncovered elements
        recovering_dict = defaultdict()
        for set_i in not_in_solution:

            # Checking set size
            set_length = len(set_collection[set_i])
            print(len(not_in_solution))
            print(maximum_set_length_allowed, "\n")
            if set_length <= maximum_set_length_allowed:

                # Initialize set value with 0
                recovering_dict[set_i] = 0

                # Compute how many current-uncovered-elements this set recovers and save it as value in recovering_dict
                for element in amount_elements_covered_dict:
                    if amount_elements_covered_dict[element] != 0:
                        continue
                    if element in set_collection[set_i]:
                        recovering_dict[set_i] += 1

                if recovering_dict[set_i] == 0:
                    del recovering_dict[set_i]


                else:  # Taking the amount recovering sets worked best
                    recovering_dict[set_i] = set_length / recovering_dict[set_i]  # Quite slow!
                    # recovering_dict[set_i] = recovering_dict[set_i] / set_length    # Totally bad!!


        # Select a set where the "cost"-value of the recovering_dict is minimum
        key_of_cost_min = min(recovering_dict.keys(), key=(lambda k: recovering_dict[k]))

        current_solution_list_indices.append(key_of_cost_min)
        added_to_solution.append(key_of_cost_min)
        not_in_solution.remove(key_of_cost_min)


        for element in set_collection[key_of_cost_min]:
            amount_elements_covered_dict[element] += 1

    # 6. Remove all duplicates
    solution_indices = set(current_solution_list_indices)

    if print_logs:
        print("Added sets: ", added_to_solution)


    return solution_indices, amount_elements_covered_dict


if __name__ == "__main__":
    print("")

    """
    Execution of the the simulated annealing algorithm for the given set cover problem.
    The set collection is contained in sets_universe,
    the elements to cover are stored in wds_universe.

    2 Test sets are also prepared further down.
    """

    # Test set containing only a partition of sets_universe:
    test_sets_1 = [sets_universe[0],
                   sets_universe[1],
                   sets_universe[2],
                   sets_universe[3],
                   sets_universe[5],
                   sets_universe[6],
                   sets_universe[7],
                   sets_universe[8],
                   sets_universe[9]
                   ]
    # Test set containing sets as in the paper example and the corresponding wds universe:
    test_sets_2 = [
        {'A', 'B', 'C', 'D', 'E'},
        {'A', 'B', 'D', 'F', 'G'},
        {'A', 'F', 'G'},
        {'B', 'C', 'G'},
        {'G', 'H'},
        {'E', 'H'},
        {'C', 'I'},
        {'A'},
        {'E'},
        {'I'}
    ]
    wds_2 = {
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'
    }

    bla = random.sample(sets_universe, 1)
    print(bla)
    print(bla.__class__)
    print(sets_universe.__class__)
