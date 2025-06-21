# ikemen_wrapper_base.py
# Note: This wrapper assumes some external window capture utility is used and passed to functions that require it. 
# If no external capture utility is needed, simply set `capture=False` in the `IkemenEnv` constructor, and do not pass a `WindowCapture` instance to the `reset` or `debug_show_capture` methods.

import gymnasium as gym
import cv2
import time
import subprocess 
import os 
from commands import ACTIONS
import sqlite3

# Ikemen GO executable path
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))   # change to the parent folder where you placed your Ikemen_GO folder if you don't want to install Ikemen_GO in the same folder as this repository
IKEMEN_EXE = os.path.join(BASE_DIR, "Ikemen_GO", "Ikemen_GO.exe")
IKEMEN_DIR = os.path.join(BASE_DIR, "Ikemen_GO")          # folder that contains Ikemen_GO.exe
DB_PATH = os.path.join(IKEMEN_DIR, "external", "mods", "bridge.db")  # path to the database file
CHAR_DEF = os.path.relpath(
    os.path.join(BASE_DIR, "kfm_env", "kfm_env.def"),
    IKEMEN_DIR
)

class IkemenEnv(gym.Env):

    def __init__(self, ai_level=4, capture=False):
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
        self.init_db() 
        self.capture = capture
        #time.sleep(2)                             # give window time

    # -----------------------------------------------------------------

    def init_db(self, overwrite=False):
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

        return result[0] if result else -1  # Return the winner or -1 if no episode was found
    
    # ----------------------------------------------------------------

    def reset(self, wc=None):
        """
        Reset the environment and return the initial observation.
        - wc: WindowCapture instance to capture the screen
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

        if self.capture:
            return wc.get_screenshot()
        
        return None
    
    # -----------------------------------------------------------------
    def step(self, action):
        self.enqueue_command(cmd = "assertCommand", arg = action)

    def debug_show_capture(self, wc):
        """
        Capture the screen and display it using OpenCV.
        - wc: WindowCapture instance to capture the screen
        """
        if not self.capture:
            print("Capture is disabled. Set capture=True to enable.")
            return
        try:
            frame = wc.get_screenshot()
        except Exception as e: # Theres going to be a frame or two when we try and capture nothing
            return
        cv2.imshow("Window", frame)
        cv2.waitKey(1) # Update OpenCV window every 1 ms

if __name__ == "__main__":
    env = IkemenEnv(ai_level=1, capture=False)
    total_reward = 0.0
    for i in range(1, 6001):           # 1000 seconds at 60 FPS
        if env.proc.poll() is None: # Process is still running
            a = env.action_space.sample()
            env.step(a) # Random action
            time.sleep(0.016)  # 60 FPS
            print(f"Enqueued command: assertCommand at step {i}")
            print(f"Action: {[ACTIONS[a]]}")
        else:
            break
    if env.finish_episode() == 1:               # Mark row as done in the database and get the winner 
        total_reward += 1.0
    env.proc.terminate()           # Close Ikemen when done
    cv2.destroyAllWindows()        # Close all OpenCV windows
    print(f"Total reward: {total_reward:.2f}")
    print("Environment closed.")
