# ==========================================================
# ==========================================================
# Minimalist function 2
# - Started with S Pletcher minimalist Function
#
# Updates from version 1
# -------------------------------
# - Added obvious penalties
# - Added excessive steering penalty
# - Added reward for faster progress
# ==========================================================
# ==========================================================

def reward_function(params):
    # ------------------------------------------------------
    # Input Parameters
    # ------------------------------------------------------
    all_wheels_on_track = params['all_wheels_on_track']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed'] # 0-5.0 meters/sec
    steps = params['steps'] # runs about 15 steps/sec
    progress = params['progress'] # progress is 0-100 (percent)
    steering = abs(params['steering_angle'])

    # ------------------------------------------------------
    # Reward for progress
    # ------------------------------------------------------

    # Steps are 15 steps/sec
    TOTAL_NUM_STEPS = 15*15 # I want the car to finish in 15 seconds

    if all_wheels_on_track:
        reward = progress

        # Give additional reward if the car pass every 60 steps faster than expected
        if (steps % TOTAL_NUM_STEPS/5) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100:
            reward *= 1.25
    else:
        # If car goes off track, assign 0 reward
        reward = 1e-3

    # ------------------------------------------------------
    # Obvious Punishments
    # ------------------------------------------------------

    # Penalize if car steer too much to prevent zigzag (range -30:30 degrees)
    ABS_STEERING_THRESHOLD = 15.0
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8


    return float(reward)
