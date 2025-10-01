# viz-ikemen

Viz Ikemen is a game AI enviornment that can be used to train bots to play the game Ikemen GO entirely with visual information. Ikemen GO is an open source fighting game built in the GO programming language. Viz-ikemen uses the games "VS" mode as an enviornment to train an agent learner to battle the CPU opponents that exist in Ikemen GO.

## Setup Instructions

1. Clone [this fork of Ikemen GO](https://github.com/JohnAsaro/Ikemen-GO) into folder A
2. Build the game in folder A (if the provided screenpack in future versions of Ikemen-GO causes issues, note this was built with [this](https://github.com/ikemen-engine/Ikemen_GO-Elecbyte-Screenpack/tree/f5d97fcd33f452b8cfd40f8981a1c15b5478cda2) edition of the screenpack in mind.)
3. Clone this repository into folder B
4. Paste the contents of folder A into folder B. The following files from this repository must be preserved:
   - `external/script/external_interface.lua`
   - `external/script/main.lua`

## To Use

There is a wrapper for Ikemen GO contained in this repository called ikemen_wrapper_sb3. This is a wrapper for Viz Ikemen using the Gymnasium API. 
It assumes some stablebaselines3 reinforcement learning algorithm will be used with it, and is set up to train models with PPO, but one could easily delete 
any refrence to PPO, and use any Gymnasium supported learning algorithm. 

By default Viz-ikemen uses the "Kung Fu Man" (KFM) character as both the learner and CPU oponent, however, this can be easily configured in the wrappers to be a battle against any character supported by the Ikemen GO game. To change the learner character, one must update commands.py (or remove it entirely and replace the action space in the wrapper with one that will work for your new character), edit the wrapper to lead to this new learner, this new learner must have a command list layed out the same way and placed into an external.zss file the same way as kfm_env. Then you must edit external_interface.lua so that the action space table matches the action space of your new learner, and you must remove the refrences to KFM in the action handlers or change them such that they refrence the new learner.

## Whats Actually Happening?

The reason we have to compile my fork of Ikemen GO is that the communication between the game and Python wrapper happens through a SQLite datebase called bridge.db. This obviously doesn't work natively, so I made the following modifications:
   - Added the fps parameter to the quick launch 
   - Adding SQLite functionality to the compiled game file
   - Adding a function in the games code that writes the screen buffer to bridge.db

Actions are actually called in the game through the lua script external_interface.lua. We have 1 action for any unique combination of inputs that can cause KFM to do something, each action corresponds to a map defined the as defined by external.zss in kfm_env, which is why we must have our action space match that map. 

The pipeline is: Python wrapper writes an action to bridge.db, external_interface.lua recognizes this and changes the map in the zss script, the zss script has KFM do one of the defined actions. On each in game tick, the screen buffer is also written to bridge.db, we always take the latest screen buffer as an observation when training the learner.

## Results

After training a model for 2048000 steps, it converged to a 90% winrate against the level 1 CPU training partner. 
These results, the model trained, and hyperparameters used can be found in PPO_results. 

## TODO

- Expand to other algorithms
- Make enviornment into an API that can be installed through pip (its almost there, I just need the time to actually do it)