# ikemen_wrapper_sb3.py
# ikemen environment written to work with stable_baselines3 algorithms
# uses PPO for training as an example

import gymnasium as gym
import cv2
import time
import subprocess 
import os 
from commands import ACTIONS
import sqlite3
import numpy as np
from stable_baselines3.common import env_checker #Import the env_checker class from stable_baselines3 to check the environment
from stable_baselines3 import PPO #Import the PPO class for training
from stable_baselines3.common.evaluation import evaluate_policy #Import the evaluate_policy function to evaluate the model
from stable_baselines3.common.callbacks import BaseCallback #Import the BaseCallback class from stable_baselines3 to learn from the environment
import os #To save the model to the correct pathfrom stable_baselines3.common.callbacks import BaseCallback #Import the BaseCallback class from stable_baselines3 to learn from the environment

# Constants
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))   # change to the parent folder where you placed your Ikemen_GO folder if you don't want to install Ikemen_GO in the same folder as this repository
IKEMEN_EXE = os.path.join(BASE_DIR, "Ikemen_GO", "Ikemen_GO.exe")
IKEMEN_DIR = os.path.join(BASE_DIR, "Ikemen_GO")          # folder that contains Ikemen_GO.exe
DB_PATH = os.path.join(IKEMEN_DIR, "external", "mods", "bridge.db")  # path to the database file
CHAR_DEF = os.path.relpath(
    os.path.join(BASE_DIR, "kfm_env", "kfm_env.def"),
    IKEMEN_DIR
)
RL_SAVES = "RL_SAVES" # Folder to save the trained models


class IkemenEnv(gym.Env):

    def __init__(self, ai_level=1, screen_width=640, screen_height=480, show_capture=False):
        
        # Constants
        self.winner = -1 # -1 = no winner, 1 = P1 wins, 2 = P2 wins
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.show_capture = show_capture
        
        # Gym spaces
        self.action_space      = gym.spaces.Discrete(len(ACTIONS))
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(screen_height, screen_width, 3), dtype=np.uint8)
        
        # Game parameters
        cmd = [
            IKEMEN_EXE,
            "-p1", CHAR_DEF,                 # P1 Learner
            "-p1.color", "1",
            "-p2", CHAR_DEF,                 # P2 CPU
            "-p2.ai", str(ai_level),  
            "-p2.color", "3",
            "-s", "stages/training.def",
            "-rounds", "10", # Hardcoded to only evaluate 1 round, we do this many to give the algorithms time to rollout new policies
            "-nosound",
            "-windowed",
            "-width", str(screen_width), 
            "-height", str(screen_height), 
        ]

        # Launch Ikemen, keep handle
        self.proc = subprocess.Popen(
            cmd,
            cwd=IKEMEN_DIR,                     # run inside Ikemen_GO folder
            stdout=subprocess.DEVNULL,          # keep console clean (optional)
            stderr=subprocess.STDOUT    
        )

        # Initialize database
        self.init_db() 

        #time.sleep(2)                             # give window time

    # -----------------------------------------------------------------
    # Database methods

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
        
        # Connect and create episodes table
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

        # Insert a default row if the episodes table is empty
        c.execute("""
        INSERT INTO episodes (cmd, arg, done, winner) 
        SELECT 'setup', 0, 0, -1 
        WHERE NOT EXISTS (SELECT 1 FROM episodes)
        """)

        # Create environment table
        c.execute("""
        CREATE TABLE IF NOT EXISTS environment (
            reset INTEGER NOT NULL DEFAULT 0
        )
        """)
          # Insert a default row if the environment table is empty
        c.execute("INSERT INTO environment (reset) SELECT 0 WHERE NOT EXISTS (SELECT 1 FROM environment)")

        # Create buffer table
        c.execute("""
        CREATE TABLE IF NOT EXISTS buffer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            width INTEGER NOT NULL,
            height INTEGER NOT NULL,
            buffer_data BLOB NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
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
            c.execute("INSERT INTO buffer (width, height, buffer_data, done) VALUES (-1, -1, x'', -1)") # Insert empty buffer row to signal new command
        else:
            # No active episode, insert a new one
            c.execute(
                "INSERT INTO episodes (cmd, arg, done) VALUES (?, ?, 0)",
                (cmd, arg)
            )
        
        conn.commit()
        conn.close()

    # ----------------------------------------------------------------
    # Mess with game state

    def check_winner(self):
        """
        - Check the database for a winner.
        - If we have one, the round is over, move on to finish_episode().
        - Mark self.winner with the winner for reward calculation.
        - Return: True if we have a winner, False otherwise.
        """
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Query the most recent episode that is not done
        c.execute("SELECT winner FROM episodes WHERE done = 0 ORDER BY id DESC LIMIT 1")
        result = c.fetchone()
        conn.close()

        # Check if we have a winner (1 or 2)
        if result and result[0] in (1, 2):
            self.winner = result[0]
            return True
        return False 


    def finish_episode(self):
        """
        -Mark row with that told KFM what to do in the last episode as done.
        """
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Find the most recent episode that is not done, note the winner and mark as done
        c.execute("UPDATE episodes SET done = 1 WHERE id = (SELECT MAX(id) FROM episodes WHERE done = 0) RETURNING winner")
        result = c.fetchone()

        # Check if any row was affected
        if c.rowcount > 0:
            print("Marked episode as complete.")
        
        c.execute("DELETE FROM buffer")  # Clear the buffer table for the next episode

        conn.commit()
        conn.close()
            

    def reset(self, seed=None):
        """
        Reset the environment and return the initial observation.
        """
        # Reset game/get initial state of screen

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("SELECT reset FROM environment")
        reset_env = c.fetchone()
        
        if reset_env is not None:
            # RESET
            c.execute(
                "UPDATE environment SET reset = 1"
            )
        
        conn.commit()
        conn.close()
        
        info = {"winner": self.winner} # Return winner of last episode in info dict
        obs = np.zeros(self.observation_space.shape, dtype=np.uint8) # Initial observation (black screen)

        return (obs, info)
    
    # -----------------------------------------------------------------    
    # Take a step in the environment

    def step(self, action):
        self.enqueue_command(cmd = "assertCommand", arg = action)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("UPDATE buffer SET done = 1 WHERE id = (SELECT MIN(id) FROM buffer WHERE done = 0) RETURNING buffer_data") # Process image
        screen_buffer = c.fetchone()
        if not screen_buffer: # No buffer data available
            conn.close()
            return np.zeros(self.observation_space.shape, dtype=np.uint8), 0.0, False, False, {} # Return black screen as observation, reward=0.0, terminated=False, truncated=False, info={}
        conn.commit()
        conn.close()

        # See if episode is still going
        if self.check_winner(): # We have a winner, episode over
            self.finish_episode() # Finish episode in db, mark as done
            terminated = True
        else:
            terminated = False 

        if self.show_capture:
            self.debug_show_capture()

        # Return variables
        result = self.process_image(screen_buffer[0], self.screen_width, self.screen_height) # Buffer data to numpy array
        reward = 1.0 if self.winner == 1 else 0.0 # Reward 1.0 if P1 (learner) wins, else 0.0
        truncated = False # Not using truncation
        info = {"winner": self.winner} # Return winner in info dict
        if terminated: # Reset winner for next episode
            self.winner = -1
        return (result, reward, terminated, truncated, info) # Return buffer_data as observation, reward=0.0, terminated=False, truncated=False, info={}

    # -----------------------------------------------------------------
    # Image processing 
    def process_image(self, buffer_data, width, height):
        """
        Convert buffer_data BLOB to numpy array
        - buffer_data: BLOB data from the database
        - width: Width of the image
        - height: Height of the image
        - Returns: Processed image as a numpy array
        """

        frame_data = np.frombuffer(buffer_data, dtype=np.uint8)
        frame = frame_data.reshape((height, width, 4)) # Data given in RGBA format
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)  # Convert to BGR for OpenCV
        frame = np.flipud(frame)  # Flip the image vertically to correct orientation

        return frame
    
    # -----------------------------------------------------------------
    # Debug 

    def debug_show_capture(self):
        
        try: # Connect to database and get the first buffer entry with done=0
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT buffer_data FROM buffer WHERE done = 0 LIMIT 1")
            result = c.fetchone()
            conn.close()
            
            if not result:
                return  # No buffer data available
            
            # You can technically pull width and height from db if needed,
            # and that would dynamically resize the window, but we use fixed size
            # because why are you resizing the window while training anyway

            # Convert buffer_data BLOB to numpy array
            frame = self.process_image(result[0], self.screen_width, self.screen_height)

            cv2.imshow("Window", frame)
            cv2.waitKey(16) # Update OpenCV window every frame
                
        except Exception as e:
            print(f"Error reading screen buffer from database: {e}")
            return

    # -----------------------------------------------------------------


# ------------------------------------------------------------------
# PPO Training and evaluation

class TrainAndLogCallback(BaseCallback):
    
    def __init__(self, check_freq, save_path, verbose = 1):

        #Args:
            #check_freq (int): Frequency to check the model
            #save_path (str): Path to save the model
            #verbose (int): Verbosity level, 1 by default

        # Inherit from BaseCallback
        # The RL model
        # self.model = None  # type: BaseAlgorithm
        # An alias for self.model.get_env(), the environment used for training
        # self.training_env # type: VecEnv
        # Number of time the callback was called
        # self.n_calls = 0  # type: int
        # num_timesteps = n_envs * n times env.step() was called
        # self.num_timesteps = 0  # type: int
        # local and global variables
        # self.locals = {}  # type: Dict[str, Any]
        # self.globals = {}  # type: Dict[str, Any]
        # The logger object, used to report things in the terminal
        # self.logger # type: stable_baselines3.common.logger.Logger
        # Sometimes, for event callback, it is useful
        # to have access to the parent object
        # self.parent = None  # type: Optional[BaseCallback]

        super(TrainAndLogCallback, self).__init__(verbose)
        self.check_freq = check_freq #Frequency to check the model
        self.save_path = save_path #Path to save the model

    def _init_callback(self): #Initialize the callback
        if self.save_path is not None: 
            os.makedirs(self.save_path, exist_ok=True) #Create the save path if it doesn't exist
        
    def _on_step(self): #Check the model after each step
        if self.n_calls % self.check_freq == 0:
            model_path = os.path.join(self.save_path, 'best_model_{}'.format(self.n_calls))
            self.model.save(model_path)
        
        return True

def train_PPO(env, timesteps=100000, check=10000):
    """
    Train a PPO model on the Ikemen environment
    - env: The Ikemen environment
    """
    callback = TrainAndLogCallback(check_freq=check, save_path=os.path.join(RL_SAVES, "models")) # Callback to save the model every 'check' timesteps

    # Create PPO model
    model = PPO(
        "CnnPolicy",  # CNN policy for image observations
        env,
        verbose=1,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        tensorboard_log=os.path.join(RL_SAVES, "tensorboard") # Tensorboard log path
    )

    model.learn(total_timesteps=timesteps, callback=callback, progress_bar=True) # Train the model


if __name__ == "__main__":
    env = IkemenEnv(ai_level=1, screen_width=640, screen_height=480, show_capture=True)
    #env_checker.check_env(env)  # Check the environment
    train_PPO(env, timesteps=10000, check=2500)

