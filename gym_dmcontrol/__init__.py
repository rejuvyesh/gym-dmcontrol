import gym
from dm_control import suite
from dm_control.rl.control import flatten_observation, FLAT_OBSERVATION_KEY

from gym import spaces
from gym.envs.registration import register
import numpy as np

from gym_dmcontrol.viewer import Viewer


class DMControlEnv(gym.Env):
    """
    Wrapper for dm_control suite task environments
    """
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, domain, task, task_kwargs=None, visualize_reward=False):
        self._dmenv = suite.load(domain, task, task_kwargs, visualize_reward)
        self._viewer = None

    @property
    def observation_space(self):
        obs = flatten_observation(
            self._dmenv.task.get_observation(self._dmenv.physics))[FLAT_OBSERVATION_KEY]
        return spaces.Box(-np.inf, np.inf, shape=obs.shape)

    @property
    def action_space(self):
        aspec = self._dmenv.action_spec()
        return spaces.Box(aspec.minimum, aspec.maximum)

    def seed(self, seed=None):
        self._dmenv.task._random = np.random.RandomState(seed)

    def step(self, action):
        ts = self._dmenv.step(action)
        obs = flatten_observation(ts.observation)[FLAT_OBSERVATION_KEY]
        reward = ts.reward
        done = ts.step_type.last()
        return obs, reward, done, {}

    def reset(self):
        ts = self._dmenv.reset()
        obs = flatten_observation(ts.observation)
        return obs[FLAT_OBSERVATION_KEY]

    def render(self, mode='human', close=False):
        if close:
            if self._viewer is not None:
                self._viewer.close()
                self._viewer = None
            return

        pixels = self._dmenv.physics.render(width=320, height=240)
        if mode == 'rgb_array':
            return pixels
        elif mode == 'human':
            self.viewer.update(pixels)
        else:
            raise NotImplementedError(mode)

    @property
    def viewer(self):
        if self._viewer is None:
            self._viewer = Viewer(width=320, height=240)

        return self._viewer


for domain_name, task_name in suite.BENCHMARKING:
    register(id='DMBench{}{}-v0'.format(domain_name.capitalize(), task_name.capitalize()),
             entry_point='gym_dmcontrol:DMControlEnv',
             kwargs={'domain': domain_name,
                     'task': task_name})
