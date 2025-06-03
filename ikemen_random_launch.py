# Launch ikemen with a random action agent.

import time
from ikemen_wrapper import IkemenEnv      
from config import ACTIONS, DEFAULT_ACTION_MAPPING

N_EPISODES = 1                         # how many two-round matches to run
STEP_DELAY = 0.016                      # ≈60 FPS

def run_episode(ai_level=4):
    """Play one 2-round match and return when Ikemen closes."""
    env = IkemenEnv(ai_level)
    obs, _ = env.reset()

    while env.proc.poll() is None:      # loop until the IKEMEN window quits
        a = env.action_space.sample()
        obs, r, done, trunc, _ = env.step(a)
        print(f"Action: {DEFAULT_ACTION_MAPPING[ACTIONS[a]]}, Reward: {r:.2f}, Done: {done}")
        time.sleep(STEP_DELAY)

    # process has exited (rounds limit reached); clean up
    env.proc.wait()                     # reap zombie on Unix
    return

# ------------------------------------------------------------
if __name__ == "__main__":
    for ep in range(N_EPISODES):
        print(f"\n=== Episode {ep+1}/{N_EPISODES} ===")
        run_episode(ai_level=4)
    print("All episodes finished.")
