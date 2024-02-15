A Categorical DQN Agent that plays Asteroids

Includes a reimplementation of the game alongside a custom environment and agent.
Made for my thesis.

# How to use
- Create a python environment (for example miniconda)
- Install the following packages: tensorflow, tf-agents-nightly, pygame and matplotlib
- Pull this repository
- Start the agent

What the game looks like:
![image](https://github.com/PrinceAria/asteroids_ai/assets/124070450/4f93cf15-b771-4e67-9dc5-d4e255a699cc)

The agent is rewarded based on the amount of asteroids it shoots as well as the amount of time it was alive for.
The reward is also increased by the score-time ratio.
