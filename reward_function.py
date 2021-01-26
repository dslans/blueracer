# ==========================================================
# ==========================================================
# DeepRacer Reward Function
#
# ==========================================================
# ==========================================================


def reward_function(params):
    '''
    Reward Function for BakerTilly DeepRacer League
    '''
    # ------------------------------------------------------
    # Input Parameters
    # ------------------------------------------------------
    all_wheels_on_track = params['all_wheels_on_track']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']


    # ------------------------------------------------------
    # Default Reward
    # ------------------------------------------------------
    reward  = 1.0

    # ------------------------------------------------------
    # Keep the car on the track
    # ------------------------------------------------------

    ## ------ Rewards ------
    if all_wheels_on_track and (0.5*track_width - distance_from_center) >= 0.05:
        reward += 1.0

    ## ------ Punishments ------

    # If the car goes off the track, assign zero reward
    if not all_wheels_on_track:
        reward = 1e-3

    # ------------------------------------------------------
    # Speed
    # ------------------------------------------------------

    SPEED_THRESHOLD = 1.0 # threshold for low speed
    if speed < SPEED_THRESHOLD:
        reward *= 0.5

    # ------------------------------------------------------
    # Steering
    # ------------------------------------------------------

    # Penalize if car steer too much to prevent zigzag (range -30:30 degrees)
    ABS_STEERING_THRESHOLD = 20.0
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    # ------------------------------------------------------
    # Waypoints
    # ------------------------------------------------------

    return float(reward)
