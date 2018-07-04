# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    #Creem la pila i el vector de nodes visitats
    pila = util.Stack()
    visitat = set()

    #Afegim el node inicial a la pila
    pila.push((problem.getStartState(),[],0))

    #Mentres la pila no estigui buida
    while not pila.isEmpty():

        #Buidem la pila i guardem els seus valors en les variables estat, accions i cost
        estat, accions_fetes, cost_total = pila.pop()

        #Si el node es el node goal, retornem el cami desde el node inicial fins al node goal
        if problem.isGoalState(estat):
            return accions_fetes

        #Si el estat no ha estat visitat l'afegim al vector de nodes visitats, sino, continua
        if not estat in visitat:
            visitat.add(estat)
        else:
            continue

        #Expandim el estat i mirem els seus fills
        for fill, accio, cost in problem.getSuccessors(estat):
            #Si el node fill no ha estat visitat, l'afegim a la pila
            if not fill in visitat:                            
                pila.push((fill, accions_fetes+[accio], cost_total+cost))



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #Creem la cua i el vector de nodes visitats
    cua = util.Queue()
    visitat = set()

    #Afegim el node inicial a la cua
    cua.push((problem.getStartState(),[],0))

    #Mentres la cua no estigui buida
    while not cua.isEmpty():
        
        #Buidem la cua i guardem els seus valors en les variables estat, accions i cost
        estat, accions_fetes, cost_total = cua.pop()

        #Si el node es el node goal, retornem el cami desde el node inicial fins al node goal
        if problem.isGoalState(estat):
            return accions_fetes

        #Si el estat no ha estat visitat l'afegim al vector de nodes visitats, sino, continua
        if not estat in visitat:
            visitat.add(estat)
        else:
            continue

        #Expandim el estat i mirem els seus fills
        for fill, accio, cost in problem.getSuccessors(estat):
            #Si el node fill no ha estat visitat, l'afegim a la cua
            if not fill in visitat:                            
                cua.push((fill, accions_fetes+[accio], cost_total+cost))


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    #Creem la cua de prioritat i el vector de nodes visitats
    cua_prioritat = util.PriorityQueue()
    visitat = set()

    #Afegim el node inicial a la cua de prioritat
    #la cua de prioritat te dos parametres {estat, cost}
    cua_prioritat.push((problem.getStartState(), []), 0)

    #Mentres la cua de prioritat no estigui buida
    while not cua_prioritat.isEmpty():

        #Buidem la cua i guardem els seus valors en les variables estat, accions i cost
        estat, accions_fetes = cua_prioritat.pop()

        #Si el node es el node goal, retornem el cami desde el node inicial fins al node goal
        if problem.isGoalState(estat):
            return accions_fetes

        #Si el estat no ha estat visitat l'afegim al vector de nodes visitats, sino, continua
        if not estat in visitat:
            visitat.add(estat)
        else:
            continue

        #Expandim el estat i mirem els seus fills
        for fill, accio, cost in problem.getSuccessors(estat):
            #Si el node fill no ha estat visitat, l'afegim a la cua de prioritat
            #La prioritat del estat es el cost acumulat del node inicial al fill
            if not fill in visitat:
                cua_prioritat.push((fill, accions_fetes+[accio]), problem.getCostOfActions(accions_fetes+[accio]))


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"    
    
    #Creem la cua de prioritat i el vector de nodes visitats
    cua_prioritat = util.PriorityQueue()
    visitat = set()

    #Afegim el node inicial a la cua de prioritat
    #la cua de prioritat te dos parametres {estat, heuristica}
    cua_prioritat.push((problem.getStartState(), []), heuristic(problem.getStartState(), problem))

    #Mentres la cua de prioritat no estigui buida
    while not cua_prioritat.isEmpty():
        estat, accions_fetes = cua_prioritat.pop()

        #Si el node es el node goal, retornem el cami desde el node inicial fins al node goal
        if problem.isGoalState(estat):
            return accions_fetes

        #Si el estat no ha estat visitat l'afegim al vector de nodes visitats, sino, continua
        if not estat in visitat:
            visitat.add(estat)
        else:
            continue 

        #Expandim el estat i mirem els seus fills
        for fill, accio, cost in problem.getSuccessors(estat):
            #Si el node fill no ha estat visitat, l'afegim a la cua de prioritat
            #La prioritat del estat es el cost acumulat del node inicial al fill + la heuristica del estat
            if not fill in visitat:
                cua_prioritat.push((fill, accions_fetes+[accio]), problem.getCostOfActions(accions_fetes+[accio]) + heuristic(fill, problem))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

