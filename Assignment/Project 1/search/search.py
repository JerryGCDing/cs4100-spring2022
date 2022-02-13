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
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    path = util.Stack()
    # discovered nodes with its corresponding path
    discovered = {}
    curr_state = problem.getStartState()
    path.push((curr_state, 'S', 'S'))
    discovered[curr_state] = []
    # goal check
    while not problem.isGoalState(curr_state):
        successors = problem.getSuccessors(curr_state)
        # Iterate through the frontier
        for _ in successors:
            temp = _[0]
            # check if the node is already discovered
            if temp not in discovered:
                # stores parent and relevant action from parent
                path.push((temp, _[1], curr_state))

        next_state = path.pop()
        curr_state = next_state[0]
        curr_action = [i for i in discovered[next_state[2]]]
        discovered[curr_state] = curr_action + [next_state[1]]

    return discovered[curr_state]
    # print(path.list)
    # util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    path = util.Queue()
    # discovered nodes with its corresponding path
    discovered = {}
    curr_state = problem.getStartState()
    discovered[curr_state] = []
    # goal check
    while not problem.isGoalState(curr_state):
        successors = problem.getSuccessors(curr_state)
        past_actions = discovered[curr_state]
        # Iterate through the frontier
        for _ in successors:
            temp = _[0]
            # check if the node is already discovered
            if temp not in discovered:
                path.push(temp)
                curr_actions = [i for i in past_actions]
                discovered[temp] = curr_actions + [_[1]]

        curr_state = path.pop()

    return discovered[curr_state]
    # util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # discovered nodes
    discovered = {}
    # queue sorted by nodes with its current path cost
    path = util.PriorityQueueWithFunction(lambda state: problem.getCostOfActions(state[1]))
    curr_state = problem.getStartState()
    discovered[curr_state] = []

    # goal check
    while not problem.isGoalState(curr_state):
        successors = problem.getSuccessors(curr_state)
        # past action history
        past_actions = discovered[curr_state]
        # Iterate through the frontier
        for _ in successors:
            node = _[0]
            curr_action = [i for i in past_actions] + [_[1]]
            # check if the state is already expanded
            if node not in discovered:
                path.push([node, curr_action])
                discovered[node] = curr_action
            # check if lower cost than current solution
            elif problem.getCostOfActions(curr_action) < problem.getCostOfActions(discovered[node]):
                path.push([node, curr_action])
                discovered[node] = curr_action

        curr_state = path.pop()[0]

    return discovered[curr_state]

    # util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # discovered nodes
    discovered = {}
    # queue sorted by nodes with its current path cost and heuristic value
    path = util.PriorityQueueWithFunction(lambda state: problem.getCostOfActions(state[1]) + heuristic(state[0], problem))
    curr_state = problem.getStartState()
    discovered[curr_state] = []

    # goal check
    while not problem.isGoalState(curr_state):
        successors = problem.getSuccessors(curr_state)
        # past action history
        past_actions = discovered[curr_state]
        # Iterate through the frontier
        for _ in successors:
            node = _[0]
            curr_action = [i for i in past_actions] + [_[1]]
            # check if the state is already expanded
            if node not in discovered:
                path.push([node, curr_action])
                discovered[node] = curr_action
            # check if lower cost than current solution
            elif problem.getCostOfActions(curr_action) < problem.getCostOfActions(discovered[node]):
                path.push([node, curr_action])
                discovered[node] = curr_action

        curr_state = path.pop()[0]

    return discovered[curr_state]
    # util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
