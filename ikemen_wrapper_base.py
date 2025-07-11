# ikemen_wrapper_base.py

import gymnasium as gym
import cv2
import time
import subprocess 
import os 
from commands import ACTIONS
import sqlite3
import numpy as np

# Constants
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))   # change to the parent folder where you placed your Ikemen_GO folder if you don't want to install Ikemen_GO in the same folder as this repository
IKEMEN_EXE = os.path.join(BASE_DIR, "Ikemen_GO", "Ikemen_GO")
IKEMEN_DIR = os.path.join(BASE_DIR, "Ikemen_GO")          # folder that contains Ikemen_GO
DB_PATH = os.path.join(IKEMEN_DIR, "external", "mods", "bridge.db")  # path to the database file
CHAR_DEF = os.path.relpath(
    os.path.join(BASE_DIR, "kfm_env", "kfm_env.def"),
    IKEMEN_DIR
)

class IkemenEnv(gym.Env):

    def __init__(self, ai_level=1, screen_width=640, screen_height=480, step_delay=0.0):
        """
        Initialize the Ikemen GO environment.
        
        Parameters:
        - ai_level: Difficulty level of the CPU opponent (1-8).
        - screen_width: Width of the game window.
        - screen_height: Height of the game window.
        - step_delay: How long we wait between actions in seconds, this is so we don't overwhelm the game with actions.
        """

        self.action_space      = gym.spaces.Discrete(len(ACTIONS))
        self.step_delay = step_delay  # How long we wait between actions in seconds, this is so we don't overwhelm the game with actions

        cmd = [
            IKEMEN_EXE,
            "-p1", CHAR_DEF,                 # P1 Learner
            "-p1.color", "1",
            "-p2", CHAR_DEF,                 # P2 CPU
            "-p2.ai", str(ai_level),  
            "-p2.color", "3",
            "-s", "stages/training.def",
            "-rounds", "1", 
            "-windowed",
            "-nosound",
            "-width", str(screen_width), 
            "-height", str(screen_height), 
        ]

        # launch Ikemen, keep handle
        self.proc = subprocess.Popen(
            cmd,
            cwd=IKEMEN_DIR,                     # run inside Ikemen_GO folder
            stdout=subprocess.DEVNULL,          # keep console clean (optional)
            stderr=subprocess.STDOUT    
        )
        self.init_db() 
        #time.sleep(2)                             # give window time

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
            c.execute("INSERT INTO buffer (width, height, buffer_data, done) VALUES (-1, -1, x'', -1)") # Insert empty buffer row to signal new command
            # Update the existing active command
            c.execute("INSERT INTO buffer (width, height, buffer_data, done) VALUES (-1, -1, x'', -1)") # Insert empty buffer row to signal new command
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
        
        c.execute("DELETE FROM buffer")  # Clear the buffer table for the next episode

        conn.commit()
        conn.close()

        return result[0] if result else -1  # Return the winner or -1 if no episode was found
    
    # ----------------------------------------------------------------

    def reset(self):
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

        # TODO add an obs to return for compatibility with openai ppo models and stuff,
        #  probably can just be an empty np file tho idk
        
        return None
    
    def toggle_pause(self):
        """
        Pause the environment.
        """

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute("SELECT pause FROM environment")
        pause = c.fetchone()
        
        if pause is not None:
            # TOGGLE PAUSE
            c.execute(
                "UPDATE environment SET pause = 1"
            )
        
        conn.commit()
        conn.close()
        
        return
    
    # -----------------------------------------------------------------    
    def step(self, action):
        self.enqueue_command(cmd = "assertCommand", arg = action)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
       # Get the buffer_data from the maximum id where done = 0
        c.execute("SELECT buffer_data FROM buffer WHERE id = (SELECT MAX(id) FROM buffer WHERE done = 0)")
        result = c.fetchone()
        # Set all buffers where done = 0 to done = 1
        c.execute("UPDATE buffer SET done = 1 WHERE done = 0")
        conn.commit()
        conn.close()
        time.sleep(self.step_delay)  # Wait for the specified step delay before returning

        return result[0] if result else None  # Return the buffer data or None if no buffer was found

    def debug_show_capture(self):

        # TODO this is like a second behind now after I messed with the buffer system, either need to fix this
        # or just merge this and sb3 wrapper so I don't have to mantain two things that work differently but achieve the same goal
        
        try:            # Connect to database and get the first buffer entry with done=0
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT id, width, height, buffer_data FROM buffer WHERE done = 0 LIMIT 1")
            result = c.fetchone()
            conn.close()
            
            if not result:
                return  # No buffer data available
            
            buffer_id, width, height, buffer_data = result
            
            # Convert buffer_data BLOB to numpy array
            frame_data = np.frombuffer(buffer_data, dtype=np.uint8)
            frame = frame_data.reshape((height, width, 4)) # Data given in RGBA format
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)  # Convert to BGR for OpenCV
            frame = np.flipud(frame)  # Flip the image vertically to correct orientation

            cv2.imshow("Window", frame)
            cv2.waitKey(16) # Update OpenCV window every frame
                
        except Exception as e:
            print(f"Error reading screen buffer from database: {e}")
            return

    # -----------------------------------------------------------------

if __name__ == "__main__":
    env = IkemenEnv(ai_level=1, screen_width=640, screen_height=480, step_delay=0.00555555555)  # 1 step every 3 frames, ≈60 FPS
    total_reward = 0.0
    for i in range(1, 6001):           # 1000 seconds at 60 FPS
        if env.proc.poll() is None: # Process is still running
            a = env.action_space.sample()
            env.step(a) # Random action
            #print(f"Enqueued command: assertCommand at step {i}")
            #print(f"Action: {[ACTIONS[a]]}")
            env.debug_show_capture()
        else:
            break
    if env.finish_episode() == 1:               # Mark row as done in the database and get the winner 
        total_reward += 1.0
    env.proc.terminate()           # Close Ikemen when done
    cv2.destroyAllWindows()        # Close all OpenCV windows
    print(f"Total reward: {total_reward:.2f}")
    print("Environment closed.")
