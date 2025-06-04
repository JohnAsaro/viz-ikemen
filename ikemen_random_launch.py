# Launch ikemen with a random action agent.

import time
from ikemen_wrapper import IkemenEnv      
from config import ACTIONS, DEFAULT_ACTION_MAPPING

N_EPISODES = 1                         # how many two-round matches to run
STEP_DELAY = 0.016                      # ≈60 FPS

def run_episode(ai_level=4):
    """Play N 2-round matchs and return when Ikemen closes."""
    env = IkemenEnv(ai_level=ai_level)
    obs, _ = env.reset()
    total_reward_episode = 0.0

    while env.proc.poll() is None:      # loop until the IKEMEN window quits
        a = env.action_space.sample()
        obs, r, done, trunc, _ = env.step(a)
        print(f"Action: {DEFAULT_ACTION_MAPPING[ACTIONS[a]]}, Reward: {r:.2f}, Done: {done}")
        time.sleep(STEP_DELAY)
        total_reward_episode += r

    # process has exited (rounds limit reached); clean up
    env.proc.wait()                     # reap zombie on Unix
    return total_reward_episode

# ------------------------------------------------------------
if __name__ == "__main__":  

    total_reward = 0.0
    for ep in range(N_EPISODES):
        print(f"\n=== Episode {ep+1}/{N_EPISODES} ===")
        total_reward += run_episode(ai_level=4)
    print("All episodes finished.")
    print(f"Total reward: {total_reward:.2f}")
    print("Environment closed.")
