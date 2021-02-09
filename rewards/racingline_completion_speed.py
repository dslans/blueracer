# ==========================================================
# ==========================================================
# Racing line, speed, progress
# ==========================================================
# ==========================================================

def reward_function(params):
    # ------------------------------------------------------
    # Input Parameters
    # ------------------------------------------------------
    all_wheels_on_track = params['all_wheels_on_track']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center'] # 0:track_width/2
    speed = params['speed'] # 0-3.0 meters/sec
    steps = params['steps'] # runs about 15 steps/sec
    progress = params['progress'] # progress is 0-100 (percent)
    steering = abs(params['steering_angle'])

    # Initialize reward
    reward = 1e-3

    # ------------------------------------------------------
    # Racing Line
    # ------------------------------------------------------

    # For now I will use the centerline and migrate to waypoints later

    # In the AWS example, it uses markers to reward distance from centerline.
    # This method uses a formula to give the highest reward if the car is
    # on the centerline.

    # Want a higher reward if distance_from_center = 0
    # Use track_width to figure out what % distance car is away from centerline
    # The maximum distance from the center is track_width/2

    # EDIT v2: Originally there was too much reward for speed, so I increased
    # the reward for the centerline (added **2)
    if all_wheels_on_track:
        reward = (1 - (distance_from_center - track_width/2))**4

        # reward speed
        reward *= speed**2

        # reward progress
        reward += ((progress / steps))

    else:
        # if the car is off track, no reward
        reward = 1e-3

    # ------------------------------------------------------
    # Additional Punishments
    # ------------------------------------------------------

    # Penalize if car steers too much to prevent zigzag (range -30:30 degrees)
    ABS_STEERING_THRESHOLD = 15.0
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    if progress == 100:
        reward = 50000

    return float(reward)
