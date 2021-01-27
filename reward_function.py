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
    speed = params['speed'] # 0-5.0 meters/sec
    steps = params['steps'] # runs about 15 steps/sec
    progress = params['progress'] # progress is 0-100 (percent)
    is_left_of_center = params['is_left_of_center']
    is_reversed = params['is_reversed'] # True=Clockwise
    steering = abs(params['steering_angle'])

    # ------------------------------------------------------
    # Default Reward
    # ------------------------------------------------------
    reward  = 1.0

    # ------------------------------------------------------
    # Keep the car on the track in one lane
    # ------------------------------------------------------

    # Note: Staying in one lane may not be optimal route

    # Stay on track
    if all_wheels_on_track:
        reward += 1.0 # reward for staying on track

        # track direction: clockwise
        if is_reversed:
            # penalize if it goes in the left lane
            if is_left_of_center:
                reward *= 0.5
            else:
                reward += 1.0 # additional reward for being in right lane
        # track direction: counterclockwise
        elif not is_reversed:
            # penalize if it goes in the left lane
            if not is_left_of_center:
                reward *= 0.5
            else:
                reward += 1.0 # additional reward for being in left lane
    # ------------------------------------------------------
    # Finish the track
    # ------------------------------------------------------

    # Total number of steps to finish track (15 steps/sec)
    TOTAL_NUM_STEPS = 300 # In the future, use track_length to estimate steps

    # Give additional reward if the car pass every 100 steps faster than expected
    if (steps % 100) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100 :
        reward += 10.0

    # ------------------------------------------------------
    # Obvious Punishments
    # ------------------------------------------------------

    # Penalize if car steer too much to prevent zigzag (range -30:30 degrees)
    ABS_STEERING_THRESHOLD = 20.0
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    # If the car goes off the track, assign zero reward
    if not all_wheels_on_track:
        reward = 1e-3

    # Penalize slow speed
    SPEED_THRESHOLD = 0.5 # threshold for low speed
    if speed < SPEED_THRESHOLD:
        reward *= 0.5

    # ------ End of Function ------
    return float(reward)
