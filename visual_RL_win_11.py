# Using PPO to train an agent in the Ikemen environment using visual information. 
# This is a proof of concept showing how this enviornment can be used as a strong baseline for visual reinforcement learning tasks.
# This code uses Win32 API for screen capture, so it is Windows-specific. A Linux version would use X11 or similar libraries.

import gymnasium as gym
import numpy as np
import cv2
import time
import subprocess 
import os 
from commands import ACTIONS
import sqlite3
from windowcapture_windows import WindowCapture

wc = WindowCapture("Ikemen GO") # Capture the Ikemen window

