# ikemen_env.py
import gymnasium as gym
import numpy as np
import cv2
import mss
import pydirectinput
import time
import subprocess 
import os 
from config import ACTIONS, DEFAULT_ACTION_MAPPING
import pygetwindow as gw
import sqlite3

# Ikemen GO executable path
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))   # change to the parent folder where you placed your Ikemen_GO folder if you don't want to install Ikemen_GO in the same folder as this repository
IKEMEN_EXE = os.path.join(BASE_DIR, "Ikemen_GO", "Ikemen_GO.exe")
IKEMEN_DIR = os.path.join(BASE_DIR, "Ikemen_GO")          # folder that contains Ikemen_GO.exe
DB_PATH = os.path.join(IKEMEN_DIR, "external", "mods", "bridge.db")  # path to the database file
CHAR_DEF = os.path.relpath(
    os.path.join(BASE_DIR, "sf_alpha_ryu", "ryu.def"),   # → ../sf_alpha_ryu/ryu.def
    IKEMEN_DIR
)

def find_ikemen_rect():
    # Look for any window title containing “Ikemen”
    wins = [w for w in gw.getAllTitles() if "Ikemen" in w]
    if not wins:
        raise RuntimeError("Could not find an IKEMEN GO window on your desktop.")
    # Grab the actual Window object
    win = gw.getWindowsWithTitle(wins[0])[0]
    return win.left, win.top, win.width, win.height

class IkemenEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60}

    def __init__(self, ai_level=4):
        self.action_space      = gym.spaces.Discrete(len(ACTIONS))
        self.observation_space = gym.spaces.Box(0,255, shape=(4,84,84), dtype=np.uint8)

        cmd = [
            IKEMEN_EXE,
            "-p1", CHAR_DEF,                 # P1 human
            "-p1.color", "1",
            "-p2", CHAR_DEF,                 # P2 CPU
            "-p2.ai", str(ai_level),  
            "-p2.color", "2",
            "-s", "stages/training.def",
            "-rounds", "1",
            "--nosound", "--windowed", "--width", "320", "--height", "240",
        ]

        # launch Ikemen once, keep handle
        self.proc = subprocess.Popen(
            cmd,
            cwd=IKEMEN_DIR,                     # run inside Ikemen_GO folder
            stdout=subprocess.DEVNULL,          # keep console clean (optional)
            stderr=subprocess.STDOUT
        )
        time.sleep(2)                             # give window time
        x, y, w, h = find_ikemen_rect()
        # The capture is exactly at (x, y), with a size of (w, h)
        self.sct  = mss.mss()
        self.win = {"left": x, "top": y, "width": w, "height": h}
    # -----------------------------------------------------------------
    
    def _grab(self):
        frm = np.array(self.sct.grab(self.win))[:,:,:3]
        frm = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
        frm = cv2.resize(frm, (84,84), interpolation=cv2.INTER_AREA)
        return frm

    def _press(self, a):
        key = ACTIONS[a]
        pydirectinput.keyDown(key); pydirectinput.keyUp(key)

    # -----------------------------------------------------------------
    def reset(self, seed=None, options=None):
        # F4 is Ikemen’s hard reset
        pydirectinput.keyDown("f4"); pydirectinput.keyUp("f4"); time.sleep(0.1)
        frame = self._grab()
        self.stack = [frame]*4
        self.prev_p2 = self._lifebar_p2()
        return np.stack(self.stack,0), {}

    def step(self, action):
        self._press(action)
        frame = self._grab()
        self.stack.pop(0); self.stack.append(frame)

        # reward = delta damage dealt - taken
        p2 = self._lifebar_p2()
        r  = (self.prev_p2 - p2)/100.0
        self.prev_p2 = p2
        done = False
        if self.proc.poll() is not None:  # process has exited
            done = True
        trunc= False
        return np.stack(self.stack,0), r, done, trunc, {}

    # --- helpers -----------------------------------------------------
    def _lifebar_p2(self):
        x0 = self.win["left"] + 210
        y0 = self.win["top"]  + 40
        bar = self.sct.grab({"left":x0, "top":y0, "width":450, "height":30})
        return np.count_nonzero(np.asarray(bar)[:,:,2] > 200)


    def debug_show_grabs(self):
        frame = self._grab()
        cv2.imshow("Full 84×84 Crop", frame)

        x0 = self.win["left"] + 750
        y0 = self.win["top"]  +  110
        lifebar = np.asarray(
            self.sct.grab({"left":x0, "top":y0, "width":450, "height":30})
        )[:, :, 2]
        cv2.imshow("Lifebar Strip (red channel)", lifebar)
        cv2.waitKey(1) # Update OpenCV window every 1 ms

def init_db(overwrite=True):
    """Initialize the database, optionally overwriting if it exists."""
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
      CREATE TABLE IF NOT EXISTS commands (
        id   INTEGER PRIMARY KEY AUTOINCREMENT,
        cmd  TEXT    NOT NULL,
        arg  INTEGER,
        done INTEGER NOT NULL DEFAULT 0
      )
    """)
    conn.commit()
    conn.close()
    
    print(f"Database initialized at {DB_PATH}")

def enqueue_command(cmd, arg=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO commands (cmd, arg) VALUES (?, ?)", (cmd, arg))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    env = IkemenEnv(ai_level=4)
    init_db()
    obs, _ = env.reset()
    total_reward = 0.0
    for i in range(1, 6001):           # 1000 seconds at 60 FPS
        if env.proc.poll() is None: # proess is still running
            a  = env.action_space.sample()
            #obs, r, done, trunc, _ = env.step(a)
            enqueue_command("forceAction", 1000)
            print(f"Enqueued command: forceAction at step {i}")
            #if done:
            #    obs, _ = env.reset()
            time.sleep(0.016)  # 60 FPS
            #print(f"Action: {DEFAULT_ACTION_MAPPING[ACTIONS[a]]}, Reward: {r:.2f}, Done: {done}")
            env.debug_show_grabs()
            #total_reward += r
        else:
            break
    env.proc.terminate()           # close Ikemen when done
    cv2.destroyAllWindows()        # close all OpenCV windows
    print(f"Total reward: {total_reward:.2f}")
    print("Environment closed.")
