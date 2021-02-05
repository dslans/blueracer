# ==========================================================
# ==========================================================
# Simple progress reward
# ==========================================================
# ==========================================================



def reward_function(params):

    # ------------------------------------------------------
    # Input Parameters
    # ------------------------------------------------------
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed'] # 0-3.0 meters/sec
    steps = params['steps'] # runs about 15 steps/sec
    progress = params['progress'] # progress is 0-100 (percent)

    # progress / steps will give a higher reward for making greater progress
    # in fewer steps

    # speed**2 will incentivize speed (exponential reward for faster speed)

    if all_wheels_on_track and steps > 0:
        reward = ((progress / steps) * 100) + (speed**2)
    else:
        reward = 1e-3

    return float(reward)
