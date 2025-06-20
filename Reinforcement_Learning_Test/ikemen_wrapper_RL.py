# ikemen_wrapper_windows_RL.py
# Note: This wrapper uses win32api for screen capture, ikemen_wrapper_ubuntu will use x11 probably when I get around to it.

import gymnasium as gym
import numpy as np
import cv2
import time
import subprocess 
import os 
import sqlite3
from windowcapture_windows import WindowCapture
from stable_baselines3.common.callbacks import BaseCallback #Import the BaseCallback class from stable_baselines3 to learn from the environment
from stable_baselines3 import PPO #Import the PPO class for training

ACTIONS = ["None", "Triple Kung Fu Palm", "Smash Kung Fu Upper", "Kung Fu Blocking (Air/High)", "Kung Fu Blocking (Low)",
            "Light KF Upper", "Strong KF Upper", "Fast KF Upper", "Light KF Palm", "Strong KF Palm", "Fast KF Palm", 
            "Light KF Blow", "Strong KF Blow", "Fast KF Blow", "Light KF Zankou", "Strong KF Zankou", "Fast KF Zankou", 
            "Light KF Knee", "Strong KF Knee", "Fast KF Knee", "Forward Run", "Backdash", "Neutral Recovery", "Forward Recovery", 
            "Backward Recovery", "Upward Recovery", "Downward Recovery", "Light Punch", "Strong Punch", "Light Kick", "Strong Kick",
            "Crouching Light Punch", "Crouching Strong Punch", "Crouching Light Kick", "Crouching Strong Kick", "Taunt",
            "Forward Throw", "Back Throw", "Walk Forward", "Walk Back", "Jump", "Crouch", "Jump Forward", "Jump Back",
            "Down Forward", "Down Back"]  # KFMs commands, index corresponds directly to the action mapping in external.zss

# Ikemen GO executable path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # change to the parent folder where you placed your Ikemen_GO folder if you don't want to install Ikemen_GO in the same folder as this repository
IKEMEN_EXE = os.path.join(BASE_DIR, "Ikemen_GO", "Ikemen_GO.exe")
IKEMEN_DIR = os.path.join(BASE_DIR, "Ikemen_GO")          # folder that contains Ikemen_GO.exe
DB_PATH = os.path.join(IKEMEN_DIR, "external", "mods", "bridge.db")  # path to the database file
CHAR_DEF = os.path.relpath(
    os.path.join(BASE_DIR, "kfm_env", "kfm_env.def"),
    IKEMEN_DIR
)
CHECKPOINT_DIR = "RL_SAVES/checkpoints" # Directory to save the model checkpoints
LOG_DIR = "RL_SAVES/logs" # Directory to save the logs


class IkemenEnv(gym.Env):

    def __init__(self, ai_level=4, window_capture=True):
        self.action_space      = gym.spaces.Discrete(len(ACTIONS))
        
        cmd = [
            IKEMEN_EXE,
            "-p1", CHAR_DEF,                 # P1 Learner
            "-p1.color", "1",
            "-p2", CHAR_DEF,                 # P2 CPU
            "-p2.ai", str(ai_level),  
            "-p2.color", "3",
            "-s", "stages/training.def",
            "-rounds", "1",
            "--nosound",
            "--windowed",
        ]

        # launch Ikemen, keep handle
        self.proc = subprocess.Popen(
            cmd,
            cwd=IKEMEN_DIR,                     # run inside Ikemen_GO folder
            stdout=subprocess.DEVNULL,          # keep console clean (optional)
            stderr=subprocess.STDOUT    
        )
        time.sleep(2)                             # give window time

        self.init_db() 
        self.enqueue_command(cmd = "setup", arg = 0)

        if window_capture:
            self.wc = WindowCapture("Ikemen GO") # Capture the Ikemen window
            self.observation_space = self.wc.get_screenshot()  # Initialobservation space
        else:
            self.wc, self.observation_space = None, None

    # -----------------------------------------------------------------
    def init_db(self, overwrite=True):
        """Initialize the database, overwriting if it exists."""
        # Remove existing database if overwrite is True
        if overwrite and os.path.exists(DB_PATH):
            try:
                os.remove(DB_PATH)
                print(f"Removed existing database at {DB_PATH}")
            except Exception as e:
                print(f"Failed to remove existing database: {e}")
        
        # Create the directory structure if it doesn't exist
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        # Connect and create tables
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS episodes (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            cmd  TEXT    NOT NULL DEFAULT '',
            arg  INTEGER NOT NULL DEFAULT 0,
            done INTEGER NOT NULL DEFAULT 0,
            winner INTEGER NOT NULL DEFAULT -1
        )
        """)
        conn.commit()
        conn.close()
        
        print(f"Database initialized at {DB_PATH}")

    def enqueue_command(self, cmd, arg):
        """
        - Update the existing episodes command column
        - If no episode active, insert a new episode 
        """
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Check if there's any active episode (done=0)
        c.execute("SELECT id FROM episodes WHERE done = 0 LIMIT 1")
        active_cmd = c.fetchone()
        
        if active_cmd:
            # Update the existing active command
            c.execute(
                "UPDATE episodes SET cmd = ?, arg = ? WHERE id = ?",
                (cmd, int(arg), active_cmd[0])
            )
            #print(f"Updated existing episode ID {active_cmd[0]}")
        else:
            # No active episode, insert a new one
            c.execute(
                "INSERT INTO episodes (cmd, arg, done) VALUES (?, ?, 0)",
                (cmd, arg)
            )
        
        conn.commit()
        conn.close()

    def finish_episode(self):
        """Mark row with that told KFM what to do in the last episode as done."""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Find the most recent episode that is not done, note the winner and mark as done
        c.execute("UPDATE episodes SET done = 1 WHERE id = (SELECT MAX(id) FROM episodes WHERE done = 0) RETURNING winner")
        result = c.fetchone()

        # Check if any row was affected
        if c.rowcount > 0:
            print("Marked episode as complete.")
        
        conn.commit()
        conn.close()
        self.reward = 1.0 if result and result[0] == 1 else 0.0 # Assuming winner is 1 for P1, adjust as needed
        return 
    
    # ----------------------------------------------------------------

    def reset(self, seed=None, options=None):
        # Reset game/get initial state of screen
        # RESET GAME FUNCTION NOT IMPLEMENTED, PUT HERE WHEN IMPLEMENTED 
        # (although im only gonna put it in if there is another reason for me to interact with the game outside the episodes table 
        # besides that, because that would be a whole other query every frame for the loop just for something not that helpful)
        if self.wc is not None:
            return self.wc.get_screenshot(), None
        return None, None
    
    def close(self):
        """Close the environment and the Ikemen process."""
        if self.proc.poll() is None:
            self.proc.terminate()
        
    # -----------------------------------------------------------------
    def step(self, action):
        self.enqueue_command(cmd = "assertCommand", arg = action)
        obs = self.get_observation() if self.wc is not None else None
        reward = self.reward
        return obs, reward, False, False, {}

    def debug_show_capture(self):
        try:
            frame = self.wc.get_screenshot()
        except Exception as e: # Theres going to be a frame or two when we try and capture nothing
            return
        cv2.imshow("Window", frame)
        cv2.waitKey(1) # Update OpenCV window every 1 ms

# Define train and log callback class
class TrainAndLogCallback(BaseCallback):
    
    def __init__(self, check_freq, save_path, verbose = 1):

        #Args:
            #check_freq (int): Frequency to check the model
            #save_path (str): Path to save the model
            #verbose (int): Verbosity level, 1 by default

        super(TrainAndLogCallback, self).__init__(verbose)
        self.check_freq = check_freq #Frequency to check the model
        self.save_path = save_path #Path to save the model

    def _init_callback(self): #Initialize the callback
        if self.save_path is not None: 
            os.makedirs(self.save_path, exist_ok=True) #Create the save path if it doesn't exist
        
    def _on_step(self): #Check the model after each step
        if self.n_calls % self.check_freq == 0:
            model_path = os.path.join(self.save_path, 'best_model_{}'.format(self.n_calls)) #Might change this to be a pathfinder function later if I use it more than once
            self.model.save(model_path)
        
        return True

# if __name__ == "__main__":
#     env = IkemenEnv(ai_level=1)
#     total_reward = 0.0
#     for i in range(1, 6001):           # 1000 seconds at 60 FPS
#         if env.proc.poll() is None: # Process is still running
#             a = env.action_space.sample()
#             env.step(a) # Random action
#             time.sleep(0.016)  # 60 FPS
#         else:
#             break
#     if env.finish_episode() == 1:               # Mark row as done in the database and get the winner 
#         total_reward += 1.0
#     env.proc.terminate()           # Close Ikemen when done
#     cv2.destroyAllWindows()        # Close all OpenCV windows
#     print(f"Total reward: {total_reward:.2f}")
#     print("Environment closed.")

if __name__ == "__main__":
    env = IkemenEnv(ai_level=1, window_capture=True) # Initialize the Ikemen environment 
    callback = TrainAndLogCallback(check_freq=8400, save_path=CHECKPOINT_DIR) # We save the model every 8400 steps (140 seconds at 60 FPS, which is about matches) 
    model = PPO('CnnPolicy', env, verbose=1, tensorboard_log=LOG_DIR, learning_rate=0.0001, n_steps=8192) # Create the model with more n_steps, more n_steps for more complex things
    model.learn(total_timesteps=1000000, callback=callback) # Train the model for 1000000 steps
