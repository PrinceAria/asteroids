import math
import time

import numpy as np
from tf_agents.environments import tf_py_environment
from tf_agents.trajectories import time_step as ts
from tf_agents.specs import array_spec
from gym import spaces


class AsteroidsEnvironment(tf_py_environment.py_environment.PyEnvironment):
    def __init__(self, asteroids_game):
        super().__init__()
        self._observation_shape = (7,)
        self._asteroids_game = asteroids_game
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(), dtype=np.int32, minimum=0, maximum=5, name='action')
        self._observation_spec = array_spec.ArraySpec(
            shape=self._observation_shape, dtype=np.float32, name='observation')
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=self._observation_shape, dtype=np.float32)
        self._reward = 0.0
        self._score = 0
        self._last_score = 0
        self._distance = 0
        self._episode_ended = False
        self._observation = np.full(self._observation_shape, 0, dtype=np.float32)

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self._episode_ended = False
        self._asteroids_game.reset()
        self._observation = np.full(self._observation_shape, 0, dtype=np.float32)
        self._reward = 0.0
        self._last_score = 0
        return ts.restart(np.squeeze(self._observation))

    def random_action(self):
        self.random_action = np.random.Generator(np.random.MT19937()).integers(0, 2)
        return self.random_action

    def _step(self, action):
        if self._episode_ended:
            return self.reset()

        if action == 0:
            self._asteroids_game.move_player_left()
        elif action == 1:
            self._asteroids_game.move_player_right()
        elif action == 2:
            self._asteroids_game.move_player_up()
        elif action == 3:
            self._asteroids_game.move_player_down()
        elif action == 4:
            if self._asteroids_game.bullet_timer >= 5:
                self._asteroids_game.shoot_bullet()

        self._asteroids_game.render()

        observation = self.get_observation()
        self.set_observation(observation)

        self._score = self._asteroids_game.get_score()

        time_reward = self._asteroids_game.game_timer / 1000.0
        score_time_ratio = self._score / (time_reward * 100)
        self._reward = time_reward + score_time_ratio

        if self._score > self._last_score:
            self._reward = self._score + time_reward + score_time_ratio
            self._last_score = self._score

        if self._asteroids_game.get_collided():
            self._episode_ended = True
            print(f"Episode ended, last_reward: {self._reward}, score: {self._score}")
            return ts.termination(observation=np.squeeze(observation), reward=-10)

        return ts.transition(observation=np.squeeze(observation), reward=np.squeeze(self._reward), discount=1.0)

    def set_observation(self, observation):
        self._observation = observation

    def calculate_closest_asteroid(self):
        player_x = self._asteroids_game.get_player_x()
        player_y = self._asteroids_game.get_player_y()
        closest_asteroid_dx = float('inf')
        closest_asteroid_dy = float('inf')

        for asteroid in self._asteroids_game.get_asteroids():
            dx = asteroid[0] - player_x
            dy = asteroid[1] - player_y
            distance = dx ** 2 + dy ** 2
            if distance < closest_asteroid_dx ** 2 + closest_asteroid_dy ** 2:
                closest_asteroid_dx = dx
                closest_asteroid_dy = dy

        # Return the distances if asteroids exist, else return zeros
        if closest_asteroid_dx == float('inf') and closest_asteroid_dy == float('inf'):
            return 0, 0
        else:
            return closest_asteroid_dx, closest_asteroid_dy

    def calculate_closest_bullet(self):
        player_x = self._asteroids_game.get_player_x()
        player_y = self._asteroids_game.get_player_y()
        closest_bullet_dx = float('inf')
        closest_bullet_dy = float('inf')

        for bullet in self._asteroids_game.get_bullets():
            dx = bullet[0] - player_x
            dy = bullet[1] - player_y
            distance = dx ** 2 + dy ** 2
            if distance < closest_bullet_dx ** 2 + closest_bullet_dy ** 2:
                closest_bullet_dx = dx
                closest_bullet_dy = dy

        # Return the distances if bullets exist, else return zeros
        if closest_bullet_dx == float('inf') and closest_bullet_dy == float('inf'):
            return 0, 0
        else:
            return closest_bullet_dx, closest_bullet_dy

    def get_observation(self):
        player_x = self._asteroids_game.get_player_x()
        player_y = self._asteroids_game.get_player_y()
        player_angle = self._asteroids_game.get_player_angle()

        closest_asteroid_dx, closest_asteroid_dy = self.calculate_closest_asteroid()
        closest_bullet_dx, closest_bullet_dy = self.calculate_closest_bullet()

        observation = np.array([
            player_x,
            player_y,
            player_angle,
            closest_asteroid_dx,
            closest_asteroid_dy,
            closest_bullet_dx,
            closest_bullet_dy
        ], dtype=np.float32)

        return observation

    def get_score(self):
        return self._score

    def get_distance(self):
        return self._distance

    def get_reward(self):
        return self._reward

    def get_episode_ended(self):
        return self._episode_ended
