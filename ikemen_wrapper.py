# ikemen_env.py
import gymnasium as gym, numpy as np, cv2, mss, pydirectinput, time, subprocess, os

ACTIONS = ["left", "right", "up", "down", "x", "y", "z", "a", "s", "d"]  # 10-button discrete

# Ikemen GO executable path
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))   # change to the parent folder where you placed your Ikemen_GO folder if you don't want to install Ikemen_GO in the same folder as this repository
IKEMEN_EXE = os.path.join(BASE_DIR, "Ikemen_GO", "Ikemen_GO.exe")

class IkemenEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60}

    def __init__(self):
        self.action_space      = gym.spaces.Discrete(len(ACTIONS))
        self.observation_space = gym.spaces.Box(0,255, shape=(4,84,84), dtype=np.uint8)

        # launch Ikemen once, keep handle
        self.proc = subprocess.Popen(["Ikemen_GO.exe","--nosound","--windowed",
                                      "--width","320","--height","240"])
        time.sleep(2)                             # give window time
        self.sct  = mss.mss()
        self.win  = {"top":60,"left":160,"width":320,"height":240}

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

        done = self._round_over()
        trunc= False
        return np.stack(self.stack,0), r, done, trunc, {}

    # --- helpers -----------------------------------------------------
    def _lifebar_p2(self):
        # quick & dirty: sample 1px strip of red HP bar
        bar = self.sct.grab({"left":210,"top":40,"width":100,"height":1})
        return np.count_nonzero(np.asarray(bar)[:,:,2] > 200)

    def _round_over(self):
        # white “KO” flashes = high average brightness top centre
        patch = np.asarray(self.sct.grab({"left":150,"top":20,"width":40,"height":10}))[:,:,:3]
        return patch.mean() > 200
