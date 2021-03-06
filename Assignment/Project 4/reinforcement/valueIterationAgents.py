# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for _ in range(self.iterations):
            # deep copy dict for bottom-up batch update
            new_values = self.values.copy()

            for s in self.mdp.getStates():
                opt_action = self.getAction(s)
                if opt_action is not None:
                    opt_value = self.getQValue(s, opt_action)
                    new_values[s] = opt_value

            self.values = new_values

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        value = 0
        for s, p in self.mdp.getTransitionStatesAndProbs(state, action):
            value += p * (self.mdp.getReward(state, action, s) + self.discount * self.getValue(s))

        return value
        # util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
            return None

        actions = self.mdp.getPossibleActions(state)
        next_state = util.Counter()
        for _ in actions:
            next_state[_] = self.getQValue(state, _)

        return next_state.argMax()
        # util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()

        for _ in range(self.iterations):
            s = states[_ % len(states)]
            opt_action = self.getAction(s)
            if opt_action is not None:
                opt_value = self.getQValue(s, opt_action)
                self.values[s] = opt_value

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        # Stage 1
        states = self.mdp.getStates()
        predeDict = {}
        for start in states:
            if self.mdp.isTerminal(start):
                continue
            actions = self.mdp.getPossibleActions(start)
            for _ in actions:
                successors = self.mdp.getTransitionStatesAndProbs(start, _)
                for end, prob in successors:
                    if prob > 0:
                        if end not in predeDict:
                            predeDict[end] = [start]
                        elif start not in predeDict[end]:
                            predeDict[end].append(start)
        # Stage 2
        queue = util.PriorityQueue()
        newVal = {}
        for s in states:
            if self.mdp.isTerminal(s):
                continue

            currentVal = self.getValue(s)
            maxAction = self.computeActionFromValues(s)
            if maxAction is not None:
                maxQVal = self.computeQValueFromValues(s, maxAction)
                newVal[s] = maxQVal
                diff = abs(maxQVal - currentVal)
                queue.push(s, -diff)
            else:
                newVal[s] = currentVal
        # Stage 3
        for _ in range(self.iterations):
            if queue.isEmpty():
                return
            s = queue.pop()
            if not self.mdp.isTerminal(s):
                self.values[s] = newVal[s]

            for p in predeDict[s]:
                currentVal = self.getValue(p)
                maxAction = self.computeActionFromValues(p)

                if maxAction is not None:
                    maxQVal = self.computeQValueFromValues(p, maxAction)
                    diff = abs(maxQVal - currentVal)
                    newVal[p] = maxQVal

                    if diff > self.theta:
                        queue.update(p, -diff)
