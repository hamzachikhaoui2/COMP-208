import numpy as np
import random as random
import math
import matplotlib.pyplot as plt
from typing import List


def score_state_log(X: List[int], G: List[int], Beta: float) -> float:
    ''' Return the log of score by taking as parameters a state X , The gold vector G and a Beta Value.
    '''
    return Beta*np.dot(X,G)


def random_coin(p: float) -> float:
    '''Return True iff we get a head after tossing a random coin with robability of head p. 
    '''
    unif = random.uniform(0,1)
    if unif>=p:
        return False
    else:
        return True


def create_proposal(X: List[int], W: List[int], W_max: int) -> List[int]:
    '''Returns a new valid proposal state by randomly toggle one index of X. The state is valid if the sum of the elements of W is less or equal than W_max
    '''
    M = len(W)
    random_index = random.randint(0,M-1)
    #print random_index
    proposal = list(X)
    proposal[random_index] = 1 - proposal[random_index]  #Toggle
    #print proposal
    if np.dot(proposal,W)<=W_max:
        return proposal
    else:
        return create_proposal(X, W, W_max)
    
def MC(n_iter: int, W:List[int], G:List[int], W_max:int, B_start:float, B_incr:float) -> List[int]:
    ''' Returns the best valid state found after runing a Monte Carlo algorithm during n_iter iterations with parameters W, G, W_max, Beta_start and Beta_increments 
    '''
    M = len(W)
    Beta = B_start
    current_X = [0]*M # We start with all 0's
    best_state = ''
    best_score = 0
    gold_keeper = []
    for i in range(n_iter):
        proposed_X = create_proposal(current_X, W, W_max)
        score_current_X = score_state_log(current_X, G, Beta)
        gold_keeper.append(np.dot(current_X, G))
        score_proposed_X = score_state_log(proposed_X, G, Beta)
        acceptance_probability = min(1,math.exp(score_proposed_X-score_current_X))
        if score_current_X>best_score:
            best_state = current_X
            best_score = score_current_X
        if random_coin(acceptance_probability):
            current_X = proposed_X
        if i%500==0:
            Beta += B_incr         
    return gold_keeper, best_state

def plot_mcmc_scores(values: List[List[int]]):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    x = [i for i in range(len(values[0]))]
    for index in range(len(values)):
        plt.plot(x, values[index], colors[index]+'-', label = index)
    plt.legend()
    plt.show()

if __name__== '__main__':
    '''
    The main function initialize the arrays and runs 10 instances of the MC algorithm
    '''
    W = [20,40,60,12,34,45,67,33,23,12,34,56,23,56]
    G = [120,420,610,112,341,435,657,363,273,812,534,356,223,516]
    W_max = 150
    max_state_value =0 
    Solution_MCMC = []
    all_gold_keeper = []
    for i in range(5):
        print(i)
        gold_keeper, best_state = MC(50000,W, G, W_max, 0.0005, .0005)
        all_gold_keeper.append(gold_keeper)
        state_value=np.dot(best_state,G)
        if state_value>max_state_value:
            max_state_value = state_value
            Solution_MCMC = best_state
    
    print("MCMC Solution is :" , str(Solution_MCMC) , "with Gold Value:", str(max_state_value)) 
    plot_mcmc_scores(all_gold_keeper)
