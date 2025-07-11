# ikemen_wrapper_sb3.py
# ikemen environment written to work with stable_baselines3 algorithms
# uses PPO for training as an example

import gymnasium as gym
import cv2
import time
import subprocess 
import os 
import platform
import shutil
from commands import ACTIONS
import sqlite3
import numpy as np
from stable_baselines3.common import env_checker #Import the env_checker class from stable_baselines3 to check the environment
from stable_baselines3 import PPO #Import the PPO class for training
from stable_baselines3.common.evaluation import evaluate_policy #Import the evaluate_policy function to evaluate the model
from stable_baselines3.common.callbacks import BaseCallback #Import the BaseCallback class from stable_baselines3 to learn from the environment
import os #To save the model to the correct pathfrom stable_baselines3.common.callbacks import BaseCallback #Import the BaseCallback class from stable_baselines3 to learn from the environment
if platform.system() == "Linux": # Signal for headless pausing
    import signal

# Constants
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))   # change to the parent folder where you placed your Ikemen_GO folder if you don't want to install Ikemen_GO in the same folder as this repository
IKEMEN_EXE = os.path.join(BASE_DIR, "Ikemen_GO", "Ikemen_GO")
IKEMEN_DIR = os.path.join(BASE_DIR, "Ikemen_GO")          # folder that contains Ikemen_GO
DB_PATH = os.path.join(IKEMEN_DIR, "external", "mods", "bridge.db")  # path to the database file
CHAR_DEF = os.path.relpath(
    os.path.join(BASE_DIR, "kfm_env", "kfm_env.def"),
    IKEMEN_DIR
)
RL_SAVES = "RL_SAVES" # Folder to save the trained models


class IkemenEnv(gym.Env):

    def __init__(self, ai_level=1, screen_width=640, screen_height=480, show_capture=False, n_steps=-1, showcase=False, step_delay=0.0, headless = False, speed = 1, fps = 60, log_episode_result=True):
        """
        Parameters:
        - ai_level: Difficulty level of the CPU opponent (1-8).
        - screen_width: Width of the game window.
        - screen_height: Height of the game window.
        - show_capture: If True, display the screen capture using OpenCV.
        - n_steps: If training for a fixed number of steps, set this to that number; otherwise, -1 for infinite.
        - showcase: If True, use a larger screen (640x480) size for showcasing the environment, if true, actual screen width trained must be some resolution that can be scaled up or down to 640x480.
        - step_delay: How long we wait between actions in seconds, this is so we don't overwhelm the game with actions.
        - Note: This should be set to different values on whether or not you are training headlessly, 
        - if you are headless, this should be set to the minimum delay you can get to where each episode is still logged, 
        - this will vary by system and take some trial and error to find,
        - if you are training with show_capture on or not headlessly, this should be set to 1/fps. 
        - headless: If True, run the game without the window open.
        - speed: How fast the game runs, 1 = run the game 5 frames faster, 2 = 10, etc...
        - fps: How many frames per second game is rendered at, should be set to 60 + speed*9.
        - log_episode_result: True if you want to save the episodes column results in bridge.db for logging later.
        """
        
        # Constants
        self.winner = -1 # -1 = no winner, 1 = P1 wins, 2 = P2 wins
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.show_capture = show_capture
        self.n_steps = n_steps # If training for a fixed number of steps, set this to that number; otherwise, -1 for infinite.
        self.current_step = 0 # Current step in the episode
        self.showcase = showcase # True if showcase mode is on
        self.step_delay = step_delay # How long we wait between actions in seconds, this is so we don't overwhelm the game with actions
        self.headless = headless 
        self.log_episode_result = log_episode_result
        self.episodes_log_path = os.path.join(RL_SAVES, "current_episode_log.db") # TODO: Make this dynamically increase like tensorboard and model directories do
        self.batch_id = 1 # Batch id for logging

        # Gym spaces
        self.action_space      = gym.spaces.Discrete(len(ACTIONS) - 1) # -1 after actions to disable taunt
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(screen_height, screen_width, 3), dtype=np.uint8)
        
        # Redundancy buffer for the screen capture
        self.last_buffer = None

        # Sanity check
        if headless and showcase:
            raise RuntimeError("You can't showcase and be headless at the same time, choose one or the other!")

        if headless and platform.system() != "Linux":
            raise EnvironmentError("Headless mode is currently only supported on Linux systems.")
        
        if headless and not shutil.which("xvfb-run"):
            raise EnvironmentError("xvfb-run is required for headless mode but was not found. Try installing it with: sudo apt install xvfb")

        # Game parameters
        
        cmd = [
                IKEMEN_EXE,
                "-p1", CHAR_DEF,                 # P1 Learner
                "-p1.color", "1",
                "-p2", CHAR_DEF,                 # P2 CPU
                "-p2.ai", str(ai_level),  
                "-speed", str(speed),
                "-fps", str(fps),
                "-p2.color", "3",
                "-s", "stages/training.def",
                "-rounds", "10", # Hardcoded to only evaluate 1 round
                "-nosound",
                "-windowed",
            ]

        # Showcase

        if showcase:
            cmd += ["-width", "640", "-height", "480"] # Showcase in 640x480, adjust with real screen width and height of the model in mind
        else:
            cmd += ["-width", str(screen_width), "-height", str(screen_height)]

        # Headless

        if headless:
            full_cmd = ["xvfb-run", "-a"] + cmd
            print("WARNING: HEADLESS MODE HAS ONLY BEEN TESTED ON DEBAIN BASED SYSTEMS.")
        else:
            full_cmd = cmd

        # Launch Ikemen
        self.proc = subprocess.Popen(
            full_cmd,
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
            reset INTEGER NOT NULL DEFAULT 0,
            pause INTEGER NOT NULL DEFAULT 0,
            ispaused INTEGER NOT NULL DEFAULT 0
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
            c.execute("INSERT INTO buffer (width, height, buffer_data, done) VALUES (-1, -1, x'', -1)") # Insert empty buffer row to signal new screen capture
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
        observation = np.zeros(self.observation_space.shape, dtype=np.uint8) # Initial observation (black screen)

        return (observation, info)
    
    def pause(self):
        """
        Pause the environment.
        """

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("SELECT pause, ispaused FROM environment")
        pause, ispaused = c.fetchone()
        
        if pause is not None and ispaused == 0:
            # PAUSE
            c.execute(
                "UPDATE environment SET pause = 1"
            )
        
        conn.commit()
        conn.close()
        
        return
    

    def unpause(self):
        """
        Pause the environment.
        """

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("SELECT pause, ispaused FROM environment")
        pause, ispaused = c.fetchone()
        
        if pause is not None and ispaused == 1:
            # UNPAUSE
            c.execute(
                "UPDATE environment SET pause = 1"
            )
        
        conn.commit()
        conn.close()
        
        return
    
    # -----------------------------------------------------------------    
    # Take a step in the environment

    def step(self, action):
        
        if self.headless: # We run really fast in headless 
            os.kill(self.proc.pid, signal.SIGSTOP) # So we stop during each step to make sure the game and the program are communicating

        self.current_step += 1
        self.unpause() # Unpause the environment if it was paused
        # Note: We do this EVERY time in case there is a freak accident and the environment is paused when it shouldn't be

        if self.n_steps > 0 and self.current_step > 0 and self.current_step % self.n_steps == 0:
            self.pause() # Pause the environment if we reached the max number of steps
            if self.log_episode_result:
                with sqlite3.connect(DB_PATH) as src_conn, sqlite3.connect(self.episodes_log_path) as log_conn:
                    src_cursor = src_conn.cursor()
                    log_cursor = log_conn.cursor()

                    # Select all episodes (or filter if needed)
                    src_cursor.execute("SELECT id, done, winner FROM episodes WHERE done = 1")
                    episodes = src_cursor.fetchall()
                    episodes_with_batch = [(eid, winner, self.batch_id) for (eid, done, winner) in episodes]

                    # Insert into log DB
                    log_cursor.executemany("""
                        INSERT OR IGNORE INTO episodes (id, winner, batch_id)
                        VALUES (?, ?, ?)
                    """, episodes_with_batch)

                    self.batch_id += 1 
                    log_conn.commit()

        self.enqueue_command(cmd = "assertCommand", arg = action)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # Get the buffer_data from the maximum id where done = 0
        c.execute("SELECT buffer_data FROM buffer WHERE id = (SELECT MAX(id) FROM buffer WHERE done = 0)")
        screen_buffer = c.fetchone()
        # Set all buffers where done = 0 to done = 1
        c.execute("UPDATE buffer SET done = 1 WHERE done = 0")

        if self.last_buffer is None and not screen_buffer: # No buffer data available
            conn.close()
            if not self.headless:
                print(f"No screen buffer data available at step {self.current_step}, returning black screen.")
            return np.zeros(self.observation_space.shape, dtype=np.uint8), 0.0, False, False, {} # Return black screen as observation, reward=0.0, terminated=False, truncated=False, info={}
        elif not screen_buffer: # No new buffer data, use the last one
            screen_buffer = self.last_buffer
            # print(f"No new screen buffer data at step {self.current_step}, using last captures data.")
        else:
            self.last_buffer = screen_buffer # Store the current buffer data for next step

        conn.commit()
        conn.close()

        # See if episode is still going
        if self.check_winner(): # We have a winner, episode over
            self.finish_episode() # Finish episode in db, mark as done
            terminated = True
        else:
            terminated = False 

        # Return variables
        observation = self.process_image(screen_buffer[0], self.screen_width, self.screen_height) # Buffer data to numpy array

        if self.show_capture:
            self.debug_show_capture(capture=observation)
        
        reward = 1.0 if self.winner == 1 else 0.0 # Reward 1.0 if P1 (learner) wins, else 0.0
        
        truncated = False # Not using truncation
        
        info = {"winner": self.winner} # Return winner in info dict
        
        if terminated: # Reset winner for next episode
            self.winner = -1
        
        time.sleep(self.step_delay) # Wait for the specified step delay 
        
        if self.headless:
            os.kill(self.proc.pid, signal.SIGCONT) # Unpause
        
        return (observation, reward, terminated, truncated, info) # Return buffer_data as observation, reward=0.0, terminated=False, truncated=False, info={}

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
        
        # Determine actual dimensions for reshaping
        if self.showcase:
            # In showcase mode, the game runs at 640x480
            actual_width, actual_height = 640, 480
        else:
            actual_width, actual_height = width, height
            
        frame = frame_data.reshape((actual_height, actual_width, 4)) # Data given in RGBA format
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)  # Convert to BGR for OpenCV
        frame = np.flipud(frame)  # Flip the image vertically to correct orientation
        
        if self.showcase:
            # Resize from 640x480 to the target screen dimensions
            frame = cv2.resize(frame, (self.screen_width, self.screen_height), interpolation=cv2.INTER_AREA)
            
        return frame
    
    # -----------------------------------------------------------------
    # Debug 

    def debug_show_capture(self, capture=None):
        
        """
        Show the current screen capture using OpenCV.
        - capture: Optional pre-fetched/pre-processed capture to display. If None, fetch from DB.
        """

        try: 

            if capture is not None:
                frame = capture # Use provided capture if available
            else:
                # Connect to database and get the first buffer entry with done=0
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute("SELECT buffer_data FROM buffer WHERE done = 0 LIMIT 1")
                result = c.fetchone()
                conn.close()
                if not result:
                    return  # No buffer data available
                # Convert buffer_data BLOB to numpy array
                # You can technically pull width and height from db if needed,
                # and that would dynamically resize the window, but we use fixed size
                # because why are you resizing the window while training anyway
                frame = self.process_image(result[0], self.screen_width, self.screen_height)

            cv2.imshow("Window", frame)
            cv2.waitKey(5) # Update OpenCV window every frame
                
        except Exception as e:
            print(f"Error reading screen buffer {e}")
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

def make_new_model_path(base_dir="RL_SAVES/models", prefix="PPO_"):
    """
    Create a new model path with an incremented number.
    - base_dir: The base directory where the model will be saved.
    - prefix: The prefix for the model directory.
    - Returns: The new model path.
    """

    os.makedirs(base_dir, exist_ok=True)
    existing = {name for name in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, name)) and name.startswith(prefix)}
    
    # Find the smallest available number
    i = 1
    while f"{prefix}{i}" in existing:
        i += 1

    new_path = os.path.join(base_dir, f"{prefix}{i}")
    os.makedirs(new_path)
    return new_path

def train_PPO(env, timesteps=100000, check=10000, num_steps=2048, model_path=None):
    """
    Train a PPO model on the Ikemen environment
    - env: The Ikemen environment
    - timesteps: Total number of timesteps to train the model
    - check: Frequency to save the model
    - num_steps: Number of steps to take before re-evaluating the policy
    - model_path: Path to an existing model to load, if None, a new model will be created
    """

    episodes_log_path = os.path.join(RL_SAVES, "current_episode_log.db") # TODO: Make this make its own directory with PPO matching models and tensorboard number

    # Initialize the log DB if needed
    conn = sqlite3.connect(episodes_log_path)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS episodes (
        id   INTEGER PRIMARY KEY AUTOINCREMENT,
        winner INTEGER NOT NULL DEFAULT -1,
        batch_id INTEGER NOT NULL DEFAULT 1
    )
    """)
    conn.commit()
    conn.close()

    verbose = 1 # Verbosity level for the model training
    learning_rate = 0.0001 # Learning rate for the PPO model
    batch_size = 64 # Batch size for the PPO model
    n_epochs = 10 # Number of epochs for the PPO model
    gamma = 1.0 # Discount factor for the PPO model, since no reward shaping, 1.0 because just win/lose
    gae_lambda = 1.0 # GAE lambda for the PPO model, sparse reward so 1.0
    clip_range = 0.1 # Clipping range for the PPO model
    device = "cpu" # PPO works well on cpu, but can be changed to "cuda" for GPU training
    tensorboard_log=os.path.join(RL_SAVES, "tensorboard") # Tensorboard log path

    if model_path is None: # If no model path is provided, create a new one

        # Create PPO model
        model = PPO(
            "CnnPolicy",  # CNN policy for image observations
            env,
            verbose=verbose,
            learning_rate=learning_rate,
            n_steps=num_steps,
            batch_size=batch_size,
            n_epochs=n_epochs,
            gamma=gamma,
            gae_lambda=gae_lambda,
            clip_range=clip_range,
            device=device,
            tensorboard_log=tensorboard_log # Tensorboard log path
        )

    else: 
        # Load existing PPO model
        model = PPO.load(model_path, env, device=device)

    new_model_path = make_new_model_path(base_dir=os.path.join(RL_SAVES, "models"), prefix="PPO_") # Create a new model path with an incremented number
    callback = TrainAndLogCallback(check_freq=check, save_path=new_model_path) # Callback to save the model every 'check' timesteps

    model.learn(total_timesteps=timesteps, callback=callback, progress_bar=True) # Train the model

def test_ppo(env, model_path, n_episodes=10):
    """
    Test the trained PPO model on the Ikemen environment
    - env: The Ikemen environment
    """ 
    total_reward = 0.0  # Start total reward at 0
    model = PPO.load(model_path)  # Load the trained model

    episodes_log_path = os.path.join(RL_SAVES, "current_episode_log.db") # TODO: Make this make its own directory with PPO matching models and tensorboard number

    # Initialize the log DB if needed
    conn = sqlite3.connect(episodes_log_path)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS episodes (
        id   INTEGER PRIMARY KEY AUTOINCREMENT,
        winner INTEGER NOT NULL DEFAULT -1,
        batch_id INTEGER NOT NULL DEFAULT 1
    )
    """)
    conn.commit()
    conn.close()

    for episode in range(n_episodes):  # For each episode
        episode_reward = 0.0
        print(f'Episode: {episode + 1}')  # Print the episode number
        obs, _ = env.reset()  # Reset the environment and get only the observation
        obs = obs.copy() # Work around negative stride error 
        done = False  # Start done at false
        while not done:  # While the game isn't done
            action, _ = model.predict(obs)  # Get the action
            obs, reward, done, truncated, info = env.step(action)  # Take the action
            obs = obs.copy() # Work around negative stride error
            episode_reward += reward  # Add the reward to the total reward
        total_reward += episode_reward
        print(f'Episode: {episode + 1}, Reward: {episode_reward}, Current Total Reward: {total_reward}')  # Print the episode and total reward
        time.sleep(2)  # Sleep for 2 seconds

if __name__ == "__main__":
    n_steps = 32768 # Number of steps to take before revaluting the policy
    env = IkemenEnv(ai_level=1, screen_width=80, screen_height=60, show_capture=False, n_steps=n_steps, showcase=False, step_delay = 0.00555555555, headless = False, speed = 24, fps = 180, log_episode_result=True)  # Create the Ikemen environment
    # Note: Screen width and height below 160x120 are wonkey on windows
    # env_checker.check_env(env)  # Check the environment
    train_PPO(env, timesteps=8000000, check=32768, num_steps=n_steps, model_path=os.path.join(RL_SAVES, "models", "PPO_15", "best_model_5013504.zip"))  # Train the PPO model
    # test_ppo(env, model_path=os.path.join(RL_SAVES, "models", "PPO_14", "best_model_425984.zip"), n_episodes=999)  # Test the trained model
