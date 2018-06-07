import collections
import gym
import gym.spaces

from dm_control.rl import control
from dm_control.rl import environment
from dm_control.rl import specs


def _action_spec_from_action_space(action_space):
    if isinstance(action_space, gym.spaces.Box):
        spec = specs.BoundedArraySpec(shape=action_space.shape, dtype=action_space.dtype,
                                      minimum=action_space.low, maximum=action_space.high)
    elif isinstance(action_space, gym.spaces.Discrete):
        spec = specs.BoundedArraySpec(shape=(1,), dtype=action_space.dtype, minimum=0,
                                      maximum=action_space.n)

    else:
        raise NotImplementedError(action_space)

    return spec


class DummyPhysics:

    def __init__(self, gym_env):
        self._gym_env = gym_env

    def render(self, *args, **kwargs):
        mode = kwargs.pop('mode', 'human')
        return self._gym_env.render(mode=mode)


class Gym2DMControl(environment.Base):

    def __init__(self, gym_env):
        if callable(gym_env):
            gym_env = gym_env()
        elif isinstance(gym_env, str):
            gym_env = gym.make(gym_env)

        self._gym_env = gym_env
        self._physics = DummyPhysics(self._gym_env)
        self._action_spec = _action_spec_from_action_space(self._gym_env.action_space)
        self._observation_spec = control._spec_from_observation(self.reset().observation)
        self._reset_next_step = True

    @property
    def physics(self):
        return self._physics

    def reset(self):
        self._reset_next_step = False
        obs = self._gym_env.reset()
        observation = collections.OrderedDict()
        observation[control.FLAT_OBSERVATION_KEY] = obs
        return environment.TimeStep(
            step_type=environment.StepType.FIRST,
            reward=None,
            discount=None,
            observation=observation,)

    def step(self, action):
        if self._reset_next_step:
            return self.reset()

        obs, reward, done, _ = self._gym_env.step(action)
        observation = collections.OrderedDict()
        observation[control.FLAT_OBSERVATION_KEY] = obs

        if done:
            self._reset_next_step = True
            return environment.TimeStep(environment.StepType.LAST, reward, 0.0, observation)

        return environment.TimeStep(environment.StepType.LAST, reward, 1.0, observation)

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec


if __name__ == '__main__':
    env = gym.make('HalfCheetah-v2')
    env = Gym2DMControl(env)
    print(env.observation_spec())
    print(env.action_spec())
    ts = env.reset()
    print(ts)
