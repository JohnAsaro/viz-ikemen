# Launch ikemen with a random action agent, use ikemen_wrapper_base.py

import time
from ikemen_wrapper_base import IkemenEnv      
from commands import ACTIONS

N_EPISODES = 3                         # how many matches to run
STEP_DELAY = 0.0167                      # 1 every 3 frames, ≈60 FPS

def run_episode(ai_level=4):
    """Play N 1-round matchs and return when Ikemen closes."""
    env = IkemenEnv(ai_level=ai_level)
    reward = 0.0
    while env.proc.poll() is None:      # Loop until the IKEMEN window quits
        a = env.action_space.sample()
        env.step(a)
        #print(f"Action: {[ACTIONS[a]]}")
        time.sleep(STEP_DELAY)
        env.debug_show_capture()          


    if env.finish_episode() == 1:               # Mark row as done in the database and get the winner 
        reward += 1.0     
    env.proc.terminate()           # Close Ikemen when done
    return reward

# ------------------------------------------------------------
if __name__ == "__main__":  

    total_reward = 0.0
    for ep in range(N_EPISODES):
        print(f"\n=== Episode {ep+1}/{N_EPISODES} ===")
        total_reward += run_episode(ai_level=1)
    print("All episodes finished.")
    print(f"Total reward: {total_reward:.2f}")
    print("Environment closed.")
