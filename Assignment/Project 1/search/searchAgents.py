# searchAgents.py
# ---------------
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
This file contains all of the agents that can be selected to control Pacman.  To
select an agent, use the '-p' option when running pacman.py.  Arguments can be
passed to your agent using '-a'.  For example, to load a SearchAgent that uses
depth first search (dfs), run the following command:

> python pacman.py -p SearchAgent -a fn=depthFirstSearch

Commands to invoke other search strategies can be found in the project
description.

Please only change the parts of the file you are asked to.  Look for the lines
that say

"*** YOUR CODE HERE ***"

The parts you fill in start about 3/4 of the way down.  Follow the project
description for details.

Good luck and happy searching!
"""

from game import Directions
from game import Agent
from game import Actions
import util
import time
import search

class GoWestAgent(Agent):
    "An agent that goes West until it can't."

    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        if Directions.WEST in state.getLegalPacmanActions():
            return Directions.WEST
        else:
            return Directions.STOP

#######################################################
# This portion is written for you, but will only work #
#       after you fill in parts of search.py          #
#######################################################

class SearchAgent(Agent):
    """
    This very general search agent finds a path using a supplied search
    algorithm for a supplied search problem, then returns actions to follow that
    path.

    As a default, this agent runs DFS on a PositionSearchProblem to find
    location (1,1)

    Options for fn include:
      depthFirstSearch or dfs
      breadthFirstSearch or bfs


    Note: You should NOT change any code in SearchAgent
    """

    def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
        # Warning: some advanced Python magic is employed below to find the right functions and problems

        # Get the search function from the name and heuristic
        if fn not in dir(search):
            raise AttributeError(fn + ' is not a search function in search.py.')
        func = getattr(search, fn)
        if 'heuristic' not in func.__code__.co_varnames:
            print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        else:
            if heuristic in globals().keys():
                heur = globals()[heuristic]
            elif heuristic in dir(search):
                heur = getattr(search, heuristic)
            else:
                raise AttributeError(heuristic + ' is not a function in searchAgents.py or search.py.')
            print('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic))
            # Note: this bit of Python trickery combines the search algorithm and the heuristic
            self.searchFunction = lambda x: func(x, heuristic=heur)

        # Get the search problem type from the name
        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError(prob + ' is not a search problem type in SearchAgents.py.')
        self.searchType = globals()[prob]
        print('[SearchAgent] using problem type ' + prob)

    def registerInitialState(self, state):
        """
        This is the first time that the agent sees the layout of the game
        board. Here, we choose a path to the goal. In this phase, the agent
        should compute the path to the goal and store it in a local variable.
        All of the work is done in this method!

        state: a GameState object (pacman.py)
        """
        if self.searchFunction == None: raise Exception("No search function provided for SearchAgent")
        starttime = time.time()
        problem = self.searchType(state) # Makes a new search problem
        self.actions  = self.searchFunction(problem) # Find a path
        totalCost = problem.getCostOfActions(self.actions)
        print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
        if '_expanded' in dir(problem): print('Search nodes expanded: %d' % problem._expanded)

    def getAction(self, state):
        """
        Returns the next action in the path chosen earlier (in
        registerInitialState).  Return Directions.STOP if there is no further
        action to take.

        state: a GameState object (pacman.py)
        """
        if 'actionIndex' not in dir(self): self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP

class PositionSearchProblem(search.SearchProblem):
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1), start=None, warn=True, visualize=True):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print('Warning: this does not look like a regular search maze')

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable

        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append( ( nextState, action, cost) )

        # Bookkeeping for display purposes
        self._expanded += 1 # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999.
        """
        if actions == None: return 999999
        x,y= self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x,y))
        return cost

class StayEastSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the West side of the board.

    The cost function for stepping into a position (x,y) is 1/2^x.
    """
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: .5 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn, (1, 1), None, False)

class StayWestSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the East side of the board.

    The cost function for stepping into a position (x,y) is 2^x.
    """
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: 2 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn)

def manhattanHeuristic(position, problem, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def euclideanHeuristic(position, problem, info={}):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################

class CornersProblem(search.SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function
    """

    def __init__(self, startingGameState):
        """
        Stores the walls, pacman's starting position and corners.
        """
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top, right = self.walls.height-2, self.walls.width-2
        self.corners = ((1,1), (1,top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print('Warning: no food in corner ' + str(corner))
        self._expanded = 0 # DO NOT CHANGE; Number of search nodes expanded
        # Please add any code here which you would like to use
        # in initializing the problem
        "*** YOUR CODE HERE ***"
        # corresponds with corners have food, 0 - empty, 1 - food
        self.goal = [1, 1, 1, 1]
        # precompute heuristic list
        # self.pre_heu = {}
        # backward trace waypoints
        self.way_points = {}

    def getStartState(self):
        """
        Returns the start state (in your state space, not the full Pacman state
        space)
        """
        "*** YOUR CODE HERE ***"
        x, y = self.startingPosition
        return (x, y, tuple(self.goal))
        # util.raiseNotDefined()

    def isGoalState(self, state):
        """
        Returns whether this search state is a goal state of the problem.
        """
        "*** YOUR CODE HERE ***"
        return sum(state[2]) == 0
        # util.raiseNotDefined()

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
            For a given state, this should return a list of triples, (successor,
            action, stepCost), where 'successor' is a successor to the current
            state, 'action' is the action required to get there, and 'stepCost'
            is the incremental cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            # Add a successor state to the successor list if the action is legal
            # Here's a code snippet for figuring out whether a new position hits a wall:
            #   x,y = currentPosition
            #   dx, dy = Actions.directionToVector(action)
            #   nextx, nexty = int(x + dx), int(y + dy)
            #   hitsWall = self.walls[nextx][nexty]

            "*** YOUR CODE HERE ***"
            x, y, _ = state

            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                pos = (nextx, nexty)
                if pos in self.corners and _[self.corners.index(pos)] != 0:
                    # reaches one corner
                    new_state = [i for i in _]
                    new_state[self.corners.index(pos)] = 0
                    nextState = (nextx, nexty, tuple(new_state))
                    # update game state
                    successors.append((nextState, action, 1))
                else:
                    # nodes need to be at same time dimension
                    nextState = (nextx, nexty, tuple([i for i in _]))
                    successors.append((nextState, action, 1))

        self._expanded += 1 # DO NOT CHANGE
        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999.  This is implemented for you.
        """
        if actions == None: return 999999
        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)


def cornersHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

      state:   The current search state
               (a data structure you chose in your search problem)

      problem: The CornersProblem instance for this layout.

    This function should always return a number that is a lower bound on the
    shortest path from the state to a goal of the problem; i.e.  it should be
    admissible (as well as consistent).
    """
    corners = problem.corners # These are the corner coordinates
    walls = problem.walls # These are the walls of the maze, as a Grid (game.py)

    "*** YOUR CODE HERE ***"
    # basic attribute of the maze
    width = walls.width
    height = walls.height
    # current state
    x, y, _ = state
    heu_list = []

    # local function for getSuccessors
    def localSuccessors(local_state):
        local_successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            l_x, l_y = local_state
            l_dx, l_dy = Actions.directionToVector(action)
            nextx, nexty = int(l_x + l_dx), int(l_y + l_dy)
            if not walls[nextx][nexty]:
                nextState = (nextx, nexty)
                local_successors.append(nextState)

        return local_successors

    # attempt 1
    # default start position
    '''
    if _ == (1, 1, 1, 1):
        for i in corners:
            dx1 = x - i[0]
            dy1 = y - i[1]
            # from start to goal
            dx2 = problem.startingPosition[0] - i[0]
            dy2 = problem.startingPosition[1] - i[1]
            # euclid distance
            net_heu = (dx1 ** 2 + dy1 ** 2) ** 0.5
            # cross product to approach the straight line
            cross = abs(dx1*dy2 - dx2*dy1)

            heu_list.append(net_heu + cross * (1 / 1000))
    # start from one corner
    else:
        start = []
        goal = []
        for index in range(len(_)):
            if _[index] == 1:
                goal.append(corners[index])
            else:
                start.append(corners[index])

        for s in start:
            for g in goal:
                dx1 = x - g[0]
                dy1 = y - g[1]
                # from one corner to another
                dx2 = s[0] - g[0]
                dy2 = s[1] - g[1]
                # euclid distance
                net_heu = (dx1 ** 2 + dy1 ** 2) ** 0.5
                # cross product to approach the straight line
                cross = abs(dx1 * dy2 - dx2 * dy1)

                heu_list.append(net_heu + cross * (1 / 1000))
    return min(heu_list)
    '''
    # attempt 2
    '''
    for index in range(len(_)):
        if _[index] == 1:
            tx, ty = corners[index]
            l_x, l_y = x, y
            dx = tx - x
            dy = ty - y
            # manhattan distance
            # net_heu = abs(dx) + abs(dy)
            # euclid distance
            net_heu = (dx ** 2 + dy ** 2) ** 0.5

            # calculated a linear algebra towards the goal
            if dx == 0:
                while l_y <= ty:
                    if walls[l_x][l_y]:
                        # minimal cost to get around a wall
                        net_heu += 2
                    l_y += 1
                heu_list.append(net_heu)
            # default case
            else:
                m = dy / dx
                c = ty - m * tx
                # progress alone x-axis
                while l_x <= tx:
                    if walls[int(l_x)][int(m * l_x + c)]:
                        net_heu += 2
                    # progress
                    l_x += 1
                heu_list.append(net_heu)

    return min(heu_list)
    '''
    # attempt 3 (exceed maximum recursion depth)
    '''
    goal = []
    for index in range(len(_)):
        if _[index] == 1:
            goal.append(corners[index])
    # iterate through all possible moves neglect walls
    for g in goal:
        dx = g[0] - x
        dy = g[1] - y

        action_space = []

        # generate all possible actions within the constraint
        def action_generator(accumulator, ava_x, ava_y, direction):
            if ava_x == 0 and ava_y == 0:
                action_space.append(accumulator)

            if direction == 'N':
                # deep copy
                temp = [i for i in accumulator]
                temp.append('N')
                action_generator(accumulator, ava_x, ava_y - 1, 'N')
                if ava_x > 0:
                    action_generator(accumulator, ava_x, ava_y - 1, 'E')
                else:
                    action_generator(accumulator, ava_x, ava_y - 1, 'W')
            elif direction == 'S':
                # deep copy
                temp = [i for i in accumulator]
                temp.append('S')
                action_generator(accumulator, ava_x, ava_y + 1, 'S')
                if ava_x > 0:
                    action_generator(accumulator, ava_x, ava_y + 1, 'E')
                else:
                    action_generator(accumulator, ava_x, ava_y + 1, 'W')
            elif direction == 'W':
                # deep copy
                temp = [i for i in accumulator]
                temp.append('W')
                action_generator(accumulator, ava_x + 1, ava_y, 'W')
                if ava_y > 0:
                    action_generator(accumulator, ava_x + 1, ava_y, 'N')
                else:
                    action_generator(accumulator, ava_x + 1, ava_y, 'S')
            elif direction == 'E':
                # deep copy
                temp = [i for i in accumulator]
                temp.append('E')
                action_generator(accumulator, ava_x - 1, ava_y, 'E')
                if ava_y > 0:
                    action_generator(accumulator, ava_x - 1, ava_y, 'N')
                else:
                    action_generator(accumulator, ava_x - 1, ava_y, 'S')

        # in +y direction
        if dy > 0:
            action_generator([], dx, dy, 'N')
        else:
            action_generator([], dx, dy, 'S')

        # in +x direction
        if dx > 0:
            action_generator([], dx, dy, 'E')
        else:
            action_generator([], dx, dy, 'W')

        # generate total heuristic of the actions
        def action_cost(action_list):
            total_cost = 0
            curr_pos = (x, y)

            for _ in range(len(action_list)):
                action = action_list[_]
                if action == 'N':
                    curr_pos = (curr_pos[0], curr_pos[1] + 1)
                    if curr_pos in walls2d:
                        # minimum cost to bypass a wall
                        total_cost += 2
                    else:
                        # normal
                        total_cost += 1
                elif action == 'S':
                    curr_pos = (curr_pos[0], curr_pos[1] - 1)
                    if curr_pos in walls2d:
                        # minimum cost to bypass a wall
                        total_cost += 2
                    else:
                        # normal
                        total_cost += 1
                elif action == 'E':
                    curr_pos = (curr_pos[0] + 1, curr_pos[1])
                    if curr_pos in walls2d:
                        # minimum cost to bypass a wall
                        total_cost += 2
                    else:
                        # normal
                        total_cost += 1
                elif action == 'W':
                    curr_pos = (curr_pos[0] - 1, curr_pos[1])
                    if curr_pos in walls2d:
                        # minimum cost to bypass a wall
                        total_cost += 2
                    else:
                        # normal
                        total_cost += 1

            return total_cost

    # get all heuristics
    for _ in action_space:
        heu_list.append(action_cost(_))
    '''
    # attempt 4
    '''
    # stored computed heuristic
    past_cache = [0, 0, 0, 0]
    # bfs search
    if (x, y) not in problem.pre_heu:
        path = util.Queue()
        # only stores cost of actions
        discovered = {}
        curr_state = (x, y)
        path.push(curr_state)
        discovered[curr_state] = 0
        goal_reached = sum(_)

        while goal_reached < 4:
            curr_state = path.pop()
            # fake state
            successors = problem.getSuccessors(curr_state)
            past_cost = discovered[curr_state]
            # iterate through the frontiers
            for s in successors:
                temp = s[0]
                if temp not in discovered:
                    path.push(temp)
                    discovered[temp] = past_cost + 1
                    # goal check
                    if temp in corners:
                        goal_reached += 1
                        past_cache[corners.index(temp)] = discovered[temp]
                        
        problem.pre_heu[(x, y)] = past_cache

    temp = problem.pre_heu[(x, y)]
    # return only available heuristic
    for index in range(len(_)):
        if _[index] == 1:
            heu_list.append(temp[index])
    '''
    # attempt 5 with backward track (1966)
    # run once
    '''
    if len(problem.way_points) == 0:
        search_constraint = int(max((height - 2) / 2, (width - 2) / 2)) - 1

        for index in range(len(corners)):
            # goal as the starting state
            g = corners[index]
            path = util.Queue()
            # only stores discovered nodes
            discovered = []
            curr_state = (g[0], g[1])
            path.push(curr_state)
            discovered.append(curr_state)
            layer_count = 0

            while layer_count < search_constraint:
                curr_state = path.pop()
                # frontiers
                successors = localSuccessors(curr_state)
                # iterate through the frontiers
                for s in successors:
                    if s not in discovered:
                        path.push(s)
                        discovered.append(s)
                        # check if s is stored
                        if s in problem.way_points:
                            problem.way_points[s][index] = layer_count + 1
                        else:
                            # undiscovered goals marked as cost 999999
                            temp = [999999 for _ in range(len(corners))]
                            temp[index] = layer_count + 1
                            problem.way_points[s] = temp

                layer_count += 1

    if (x, y) in problem.way_points:
        cost_cache = problem.way_points[(x, y)]
        for i in range(len(_)):
            if _[i] == 1:
                heu_list.append(cost_cache[i])

    # return minimum cached heuristic
    if len(heu_list) != 0:
        return min(heu_list)

    # default return as combined with attempt 2
    for index in range(len(_)):
        if _[index] == 1:
            tx, ty = corners[index]
            dx = tx - x
            dy = ty - y
            # manhattan distance
            # net_heu = abs(dx) + abs(dy)
            # euclid distance
            net_heu = (dx ** 2 + dy ** 2) ** 0.5

            # calculated a linear algebra towards the goal
            # same y-axis as the goal
            if dx == 0:
                while y <= ty:
                    if walls[x][y]:
                        # minimal cost to get around a wall
                        net_heu += 2
                    y += 1
                heu_list.append(net_heu)
            # default case
            else:
                m = dy / dx
                c = ty - m * tx
                # progress alone x-axis
                while x <= tx:
                    if walls[int(x)][int(m * x + c)]:
                        net_heu += 2
                    # progress
                    x += 1
                heu_list.append(net_heu)
                
    return min(heu_list)
    '''
    # attempt 6 L1-path-finder (1512)
    # reduce maze complexity by waypoints
    # calculated once
    if 'waypoints' not in problem.way_points:
        waypoints = [g for g in corners]
        for i in range(1, width - 1):
            for j in range(1, height - 1):
                curr_pos = (i, j)
                # get available directions
                successors = localSuccessors(curr_pos)
                # guaranteed turning point
                if len(successors) > 2:
                    if curr_pos not in waypoints:
                        waypoints.append(curr_pos)
                # might be cornered point or straight line
                elif len(successors) == 2:
                    d1 = successors[0]
                    d2 = successors[1]
                    # check if not on a straight line
                    if d1[0] != d2[0] and d1[1] != d2[1]:
                        if curr_pos not in waypoints:
                            waypoints.append(curr_pos)

        problem.way_points['waypoints'] = waypoints

        # BFS from waypoints to all goals
        for node in waypoints:
            # cache for calculated heuristic
            heu_cache = [0 for _ in range(len(corners))]
            # 0 - unexplored, 1 - explored
            explored_goal = 0
            # cost from current position
            path = util.Queue()
            discovered = []
            curr_state = node
            path.push((curr_state, 0))
            discovered.append(curr_state)
            # if start from goal
            if curr_state in corners:
                heu_cache[corners.index(curr_state)] = 0
                explored_goal += 1

            # until all goals are reached
            while explored_goal != len(corners):
                curr_state = path.pop()
                successors = localSuccessors(curr_state[0])
                for _ in successors:
                    temp = _
                    if temp not in discovered:
                        curr_cost = curr_state[1] + 1
                        path.push((temp, curr_cost))
                        discovered.append(temp)
                        # goal check
                        if temp in corners:
                            heu_cache[corners.index(temp)] = curr_cost
                            explored_goal += 1

            # store cache into precompute dictionary
            problem.way_points[node] = heu_cache

    curr_state = (x, y)
    if curr_state in problem.way_points:
        return min(problem.way_points[curr_state])

    # BFS on current position to find nearby waypoint, relative fast
    '''
    path = util.Queue()
    path.push((curr_state, 0))
    discovered = [curr_state]
    # cost to nearby waypoint
    while True:
        curr_state = path.pop()
        successors = localSuccessors(curr_state[0])
        for _ in successors:
            temp = _
            if temp not in discovered:
                curr_cost = curr_state[1] + 1
                path.push((temp, curr_cost))
                discovered.append(temp)
                # goal check
                if temp in problem.way_points:
                    pre_heu = [curr_cost + _ for _ in problem.way_points[temp]]
                    # get only cost of available goals, 999999 otherwise
                    for index in range(len(_)):
                        if _[index] == 0:
                            pre_heu[index] = 999999
                    # minimum cost
                    heu_list = [_ for _ in pre_heu]

                    return min(heu_list)
    '''
    # reachable waypoints from current location and cost
    reachable_list = []
    # +x direction
    for _ in range(width):
        curr_pos = (x + _, y)
        # if hit wall
        if walls[x + _][y]:
            break
        # if reached waypoint
        if curr_pos in problem.way_points:
            reachable_list.append((curr_pos, _))
            break
    # -x direction
    for _ in range(width):
        curr_pos = (x - _, y)
        # if hit wall
        if walls[x - _][y]:
            break
        # if reached waypoint
        if curr_pos in problem.way_points:
            reachable_list.append((curr_pos, _))
            break
    # +y direction
    for _ in range(height):
        curr_pos = (x, y + _)
        # if hit wall
        if walls[x][y + _]:
            break
        # if reached waypoint
        if curr_pos in problem.way_points:
            reachable_list.append((curr_pos, _))
            break
    # -y direction
    for _ in range(height):
        curr_pos = (x, y - _)
        # if hit wall
        if walls[x][y - _]:
            break
        # if reached waypoint
        if curr_pos in problem.way_points:
            reachable_list.append((curr_pos, _))
            break

    heu_list = [_[1] + min(problem.way_points[_[0]]) for _ in reachable_list]
    return min(heu_list)
    # return 0

class AStarCornersAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, cornersHeuristic)
        self.searchType = CornersProblem

class FoodSearchProblem:
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """
    def __init__(self, startingGameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0 # DO NOT CHANGE
        self.heuristicInfo = {} # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of 1."
        successors = []
        self._expanded += 1 # DO NOT CHANGE
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append( ( ((nextx, nexty), nextFood), direction, 1) )
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x,y= self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost


class AStarFoodSearchAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, foodHeuristic)
        self.searchType = FoodSearchProblem


def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come
    up with an admissible heuristic; almost all admissible heuristics will be
    consistent as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the
    other hand, inadmissible or inconsistent heuristics may find optimal
    solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a Grid
    (see game.py) of either True or False. You can call foodGrid.asList() to get
    a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the
    problem.  For example, problem.walls gives you a Grid of where the walls
    are.

    If you want to *store* information to be reused in other calls to the
    heuristic, there is a dictionary called problem.heuristicInfo that you can
    use. For example, if you only want to count the walls once and store that
    value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access
    problem.heuristicInfo['wallCount']
    """
    position, foodGrid = state
    "*** YOUR CODE HERE ***"
    # 2d list of the game grid
    food_coord = foodGrid.asList()
    walls = problem.walls
    width = walls.width
    height = walls.height
    x, y = position
    # heu_list = []

    # local function for getSuccessors
    def localSuccessors(local_state):
        local_successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            l_x, l_y = local_state
            l_dx, l_dy = Actions.directionToVector(action)
            nextx, nexty = int(l_x + l_dx), int(l_y + l_dy)
            if not walls[nextx][nexty]:
                nextState = (nextx, nexty)
                local_successors.append(nextState)

        return local_successors

    # weird edge case
    if len(food_coord) == 0:
        return 0
    # reduce maze complexity by waypoints (14299)
    # calculated once
    if 'waypoints' not in problem.heuristicInfo:
        waypoints = [g for g in food_coord]
        for i in range(1, width - 1):
            for j in range(1, height - 1):
                curr_pos = (i, j)
                # get available directions
                successors = localSuccessors(curr_pos)
                # guaranteed turning point
                if len(successors) > 2:
                    if curr_pos not in waypoints:
                        waypoints.append(curr_pos)
                # might be cornered point or straight line
                elif len(successors) == 2:
                    d1 = successors[0]
                    d2 = successors[1]
                    # check if not on a straight line
                    if d1[0] != d2[0] and d1[1] != d2[1]:
                        if curr_pos not in waypoints:
                            waypoints.append(curr_pos)

        problem.heuristicInfo['waypoints'] = waypoints

        # BFS from waypoints to all goals
        for node in waypoints:
            # cache for calculated heuristic
            heu_cache = [0 for _ in range(len(food_coord))]
            # 0 - unexplored, 1 - explored
            explored_goal = 0
            # cost from current position
            path = util.Queue()
            discovered = []
            curr_state = node
            path.push((curr_state, 0))
            discovered.append(curr_state)
            # if start from goal
            if curr_state in food_coord:
                heu_cache[food_coord.index(curr_state)] = 0
                explored_goal += 1

            # until all goals are reached
            while explored_goal != len(food_coord):
                curr_state = path.pop()
                successors = localSuccessors(curr_state[0])
                for _ in successors:
                    temp = _
                    if temp not in discovered:
                        curr_cost = curr_state[1] + 1
                        path.push((temp, curr_cost))
                        discovered.append(temp)
                        # goal check
                        if temp in food_coord:
                            heu_cache[food_coord.index(temp)] = curr_cost
                            explored_goal += 1

            # store cache into precompute dictionary
            problem.heuristicInfo[node] = heu_cache

    curr_state = (x, y)
    if curr_state in problem.heuristicInfo:
        return min(problem.heuristicInfo[curr_state])

    reachable_list = []
    # +x direction
    for _ in range(width):
        curr_pos = (x + _, y)
        # if hit wall
        if walls[x + _][y]:
            break
        # if reached waypoint
        if curr_pos in problem.heuristicInfo:
            reachable_list.append((curr_pos, _))
            break
    # -x direction
    for _ in range(width):
        curr_pos = (x - _, y)
        # if hit wall
        if walls[x - _][y]:
            break
        # if reached waypoint
        if curr_pos in problem.heuristicInfo:
            reachable_list.append((curr_pos, _))
            break
    # +y direction
    for _ in range(height):
        curr_pos = (x, y + _)
        # if hit wall
        if walls[x][y + _]:
            break
        # if reached waypoint
        if curr_pos in problem.heuristicInfo:
            reachable_list.append((curr_pos, _))
            break
    # -y direction
    for _ in range(height):
        curr_pos = (x, y - _)
        # if hit wall
        if walls[x][y - _]:
            break
        # if reached waypoint
        if curr_pos in problem.heuristicInfo:
            reachable_list.append((curr_pos, _))
            break

    heu_list = [_[1] + min(problem.heuristicInfo[_[0]]) for _ in reachable_list]
    return min(heu_list)


class ClosestDotSearchAgent(SearchAgent):
    "Search for all food using a sequence of searches"
    def registerInitialState(self, state):
        self.actions = []
        currentState = state
        while(currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState) # The missing piece
            self.actions += nextPathSegment
            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    t = (str(action), str(currentState))
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' % t)
                currentState = currentState.generateSuccessor(0, action)
        self.actionIndex = 0
        print('Path found with cost %d.' % len(self.actions))

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition()
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState)

        "*** YOUR CODE HERE ***"
        food2d = food.asList()
        # simplified BFS
        path = util.Queue()
        discovered = {}
        curr_state = startPosition
        path.push(curr_state)
        discovered[curr_state] = []

        while True:
            curr_state = path.pop()
            successors = problem.getSuccessors(curr_state)
            past_actions = discovered[curr_state]
            # iterate through the frontiers
            for _ in successors:
                temp = _[0]
                if temp not in discovered:
                    path.push(temp)
                    curr_actions = [i for i in past_actions]
                    discovered[temp] = curr_actions + [_[1]]
                    # goal check
                    if temp in food2d:
                        return discovered[temp]

        # util.raiseNotDefined()

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state

        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def mazeDistance(point1, point2, gameState):
    """
    Returns the maze distance between any two points, using the search functions
    you have already built. The gameState can be any game state -- Pacman's
    position in that state is ignored.

    Example usage: mazeDistance( (2,4), (5,6), gameState)

    This might be a useful helper function for your ApproximateSearchAgent.
    """
    x1, y1 = point1
    x2, y2 = point2
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + str(point1)
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False, visualize=False)
    return len(search.bfs(prob))
