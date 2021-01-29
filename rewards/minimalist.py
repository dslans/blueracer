# ==========================================================
# ==========================================================
# Minimalist function from Scott Pletcher Github
#
# ==========================================================
# ==========================================================

def reward_function(params):

    if params['all_wheels_on_track']:
        reward = params['progress']
    else:
        reward = 1e-3

    return float(reward)
