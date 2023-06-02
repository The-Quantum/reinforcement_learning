# REINFORCEMENT LEARNING : MAZE PROBLEM

In machine learning, there are three methods for training a model to perform a task. This include **supervised learning**, **unsupervised Learning** and **reinforcement learning**. The supervised learning involves training a model on labeled data while unsupervised learning relises on unlabeled data and the objective consiste of extracting patterns, structures, or relationships that exits within the training data. The reinforcement learning is an approch that consist of training and agent to execute and action which consist of multiple step by rewarding at each step the desired actions that enables acheiving the goal in a fastest way a or in opposite punishing undesired actions that does not enable acheiving the goal.

One of the best example of problem that reinforcement learning approach is suitable for is the so call `maze problem`. The simple version of maze problem consists of finding the shortest path to exit a 2D maze. The problem can be complexified by requiring to first find the shortest path a potential treasor hidden somewhere in the maze before to find the shortest path to exit.  In this repository, will apply reinforment learning to solve both maze use case problem.

## General background 
In reinforcement learning, the problem is state the following way. An `agent` (in this case the person finding the shortest path to exit) takes `action` (in this case chose the next cell to move to) in the `environement` (in this case the maze) multiple times until it acheives the final goal (which in this case is to exit the maze). To take an `action`, the agent observes the current `state` of the environement and applies a decision process call `policy`. Once the action is taken, the agent recives a `reward` and the `state` of the environment is modified. The process is repeated until the goal is acheived. This process of training based on `policy` and `reward` enables the `agent` to learn the shortest path to the exit while having visited or not other cells of the maze such as location of the treasure. 

### EXECUTION 

`
 python train.py
`
