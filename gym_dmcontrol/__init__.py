import gym
from dm_control import suite
from dm_control.rl.control import flatten_observation, FLAT_OBSERVATION_KEY

from gym import spaces
from gym.envs.registration import register
import numpy as np


class DMControlEnv(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, domain, task, task_kwargs=None, visualize_reward=False):
        self._dmenv = suite.load(domain, task, task_kwargs, visualize_reward)

    @property
    def observation_space(self):
        obs = flatten_observation(
            self._dmenv.task.get_observation(self._dmenv.physics))[FLAT_OBSERVATION_KEY]
        return spaces.Box(-np.inf, np.inf, shape=obs.shape)

    @property
    def action_space(self):
        aspec = self._dmenv.action_spec()
        return spaces.Box(aspec.minimum, aspec.maximum)

    def _step(self, action):
        ts = self._dmenv.step(action)
        obs = flatten_observation(ts.observation)[FLAT_OBSERVATION_KEY]
        reward = ts.reward
        done = ts.step_type.last()
        return obs, reward, done, {}

    def _reset(self):
        ts = self._dmenv.reset()
        obs = flatten_observation(ts.observation)
        return obs[FLAT_OBSERVATION_KEY]

    def _render(self, mode='human', close=False):
        pixels = self._dmenv.physics.render()
        if mode == 'rgb_array':
            return pixels

for domain_name, task_name in suite.BENCHMARKING:
    register(id='DMBench{}{}-v0'.format(domain_name.capitalize(), task_name.capitalize()),
             entry_point='gym_dmcontrol:DMControlEnv',
             kwargs={'domain': domain_name,
                     'task': task_name})
