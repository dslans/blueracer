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
    reward  = 1e-3 # Should default reward be high or low?

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
        reward = 0.5
    else:
        reward = 1.0

    # ------------------------------------------------------
    # Steering
    # ------------------------------------------------------


    # ------------------------------------------------------
    # Waypoints
    # ------------------------------------------------------

    return reward
