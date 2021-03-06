task="gamble"
"""specify custom settings for session in this file:

How to:
	edit values for capital variables
	do not change capital cariable names

"""

GAMBLE_SIDE = "Left"

# Blocks ========================================================
"""Construct a Block like this:
{
	TRIAL_NUM_BLOCK: [int, int], #(50 - 80) #will chose a random length in between
	PROB_REWARD_GAMBLE_BLOCK: int,  #(0-100)
	prob_reward_save_block: int  #(0-100)
},
"""

BLOCKS = [
    {
        "trial_range_block": [
            1,
            2
        ],
        "prob_reward_gamble_block": 10.0,
        "prob_reward_save_block": 20.0
    },
    {
        "trial_range_block": [
            3,
            4
        ],
        "prob_reward_gamble_block": 30.0,
        "prob_reward_save_block": 40.0
    },
    {
        "trial_range_block": [
            5,
            6
        ],
        "prob_reward_gamble_block": 50.0,
        "prob_reward_save_block": 50.0
    }
]

#========================================================
# reward
# big reward in ml
BIG_REWARD = 0.11
# small rewar in ml
SMALL_REWARD = 0.12

LAST_CALLIBRATION = "2020.06.10"

# state machine settings ======================================
# waiting time beginning of each trial
TIME_START = 1.0
# time the wheel has to be stopped
TIME_WHEEL_STOPPING_CHECK = 1.0
# time wait if the wheel is not stopped bevore new trial starts
TIME_WHEEL_STOPPING_PUNISH = 0.0
# time stimulus is presented but not movable
TIME_PRESENT_STIM = 1.0
# time of open loop where wheel moves the stimulus
TIME_OPEN_LOOP = 10.0
# time wait if stimulus not moved far enough to position
TIME_OPEN_LOOP_FAIL_PUNISH = 0.0
# time stimulus is presented at reached position but not movable anymore
TIME_STIM_FREEZ = 2.0
# time the animal has for the reard = valve open + time after
REWARD_TIME = 1.0
# no reward time
NOREWARD_TIME = 1.0
# time at end of each trial_num
INTER_TRIAL_TIME = 1.5

# stimulus size and color - only for moving stimulus
STIMULUS_RAD = 45 # pixel radius of stimulus
STIMULUS_COL = [0, 255, 0] #color of stimulus

BACKGROUND_COL = [0, 0, 0] #-1,-1,-1 for black
# rotary Encoder ==============================================
""" Construct thresholds like this:
[
	-90, 90, # stimulus position in degrees of wheel movement
	-1, 1    # wheel not stoping sthreshold in degrees of wheel movement
]
"""
# threhsolds for event signaling between rotary encoder and bpod
ALL_THRESHOLDS = [
    -90,
    90,
    -2,
    2
]
# speed of movement
STIM_END_POS = [
    -2048,
    2048
] # pixel
"""
end of 1st screen from center = 960 px
end of 2nd screen from center = 960 + 1920px
"""

LIFE_PLOT = False
# Animal ===================================================
# animal waight in grams
ANIMAL_WAIGHT = 10.0
