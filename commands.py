# commands.py  -------------------------------------------
RYU_STATES = { # Statedefs for Ryu, will add all later, but thats like a whole thing and I low key need to do it through lua because of close buttons
    "hop-fwd":  "100",
    "hop-back": "105",
    "fireball":    "1300",
    "tatsu":  "1110",
    "dp": "1000",
    "c.mk": "440"
}

ACTIONS = list(RYU_STATES.keys())  # Numbers of statedefs fed directly to Ikemen
