# ==========================================================
# ==========================================================
# Racing line Reward Function
# ==========================================================
# ==========================================================
from shapely.geometry import Point, Polygon
from shapely.geometry.polygon import LinearRing, LineString
import math
def reward_function(params):
    # ------------------------------------------------------
    # Input Parameters
    # ------------------------------------------------------
    all_wheels_on_track = params['all_wheels_on_track']
    track_width = params['track_width']
    x = params['x']
    y = params['y']
    progress = params['progress']
    heading = params['heading']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    steps = params['steps']
    steering = abs(params['steering_angle'])
    speed = params['speed']


    # Define the optimal racing line
    # (found using cdthompson/deepracer-k1999-race-lines github)
    RACING_LINE = [[2.88738855, 0.72646774],
                   [3.16759122, 0.70478649],
                   [3.45517317, 0.69217863],
                   [3.75325158, 0.68581005],
                   [4.07281434, 0.68360819],
                   [4.50000223, 0.68376092],
                   [4.54999507, 0.68377879],
                   [5.11738115, 0.69080411],
                   [5.44798256, 0.7112322 ],
                   [5.71126558, 0.7422347 ],
                   [5.94137211, 0.78496462],
                   [6.1491271 , 0.84078035],
                   [6.33675893, 0.91066736],
                   [6.50351669, 0.99483994],
                   [6.64762588, 1.09336367],
                   [6.76714849, 1.20640158],
                   [6.85790417, 1.33508669],
                   [6.92193762, 1.47646609],
                   [6.96026824, 1.62797346],
                   [6.96689958, 1.7888072 ],
                   [6.92976742, 1.95515434],
                   [6.85379617, 2.11910271],
                   [6.72693273, 2.26841633],
                   [6.56582731, 2.3979065 ],
                   [6.38075512, 2.50632652],
                   [6.18037171, 2.5960265 ],
                   [5.97126499, 2.67207187],
                   [5.75829177, 2.74110301],
                   [5.5588064 , 2.81130664],
                   [5.36088415, 2.88623818],
                   [5.16456229, 2.96629375],
                   [4.96988832, 3.05190956],
                   [4.77697334, 3.14377629],
                   [4.58660766, 3.24539747],
                   [4.39799283, 3.35419739],
                   [4.21046443, 3.46760151],
                   [4.02347669, 3.58333046],
                   [3.8506858 , 3.68988272],
                   [3.6826464 , 3.79114179],
                   [3.51884306, 3.88569665],
                   [3.35641365, 3.97361826],
                   [3.19259098, 4.05426986],
                   [3.02554648, 4.12572184],
                   [2.85392239, 4.18548215],
                   [2.67754933, 4.23399905],
                   [2.49618509, 4.27140786],
                   [2.30880373, 4.29610891],
                   [2.11373905, 4.30523325],
                   [1.90856103, 4.29409449],
                   [1.68968426, 4.25390854],
                   [1.45387751, 4.16915111],
                   [1.21119005, 4.00653223],
                   [1.01922953, 3.74402202],
                   [0.92220549, 3.42050544],
                   [0.88926604, 3.10443889],
                   [0.89600747, 2.82076036],
                   [0.92404943, 2.56281185],
                   [0.96605253, 2.32460305],
                   [1.01802833, 2.11228544],
                   [1.08079017, 1.91512981],
                   [1.15513698, 1.73107571],
                   [1.24162317, 1.56014807],
                   [1.34112998, 1.40323884],
                   [1.45472589, 1.2610932 ],
                   [1.58653095, 1.13641183],
                   [1.74472608, 1.03228688],
                   [1.92655529, 0.94305481],
                   [2.13282228, 0.86779425],
                   [2.36411252, 0.80679887],
                   [2.61751276, 0.75992145],
                   [2.88738855, 0.72646774]]

    # ------------------------------------------------------
    # Initialize reward
    # ------------------------------------------------------
    reward = 1e-3

    # ------------------------------------------------------
    # Version 1 - Racing Line Only
    # ------------------------------------------------------

    Reward formula:
    f(r) = r
    r: racing line factor

    # Reward if the car is close to the racing line
    # Distance Formula: d = sqrt((x2-x1)**2 + (y2-y1)**2)
    # The distance formula is calculated in the shapely package
    current_position = Point(x,y)
    race_line = LineString(RACING_LINE) # ordered sequence of tuples
    distance_from_racingline = current_position.distance(race_line) # distance formula

    if all_wheels_on_track:
        # If car is half the width of the track away from the racing line = negative factor
        raceline_factor = 1 - (distance_from_racingline / (track_width * 0.3))
        raceline_factor = float(max(raceline_factor,0)) # gets rid of negative factors
        reward += raceline_factor # rewards are in range 0,1
    else:
        reward = 1e-3

    # ------------------------------------------------------
    # Version 2 - Racing Line and Progress
    # ------------------------------------------------------

    # # Reward formula:
    # # f(r) = r * p
    # # r: racing line factor
    # # p: progress factor
    #
    # # ------------ Racing Line ------------
    # # Reward if the car is close to the racing line
    # # Distance Formula: d = sqrt((x2-x1)**2 + (y2-y1)**2)
    # # The distance formula is calculated in the shapely package
    # current_position = Point(x,y)
    # race_line = LineString(RACING_LINE) # ordered sequence of tuples
    # distance_from_racingline = current_position.distance(race_line) # distance formula
    #
    # # If car is half the width of the track away from the racing line = negative factor
    # raceline_factor = 1 - (distance_from_racingline / (track_width * 0.5))
    # raceline_factor = float(max(raceline_factor,0)) # gets rid of negative factors
    #
    # # ------------ Progress ------------
    #
    # progress_factor = progress / 100
    #
    # # ------------ Reward ------------
    # if all_wheels_on_track:
    #     reward *= raceline_factor # rewards are in range 0,1
    #     reward *= progress_factor
    # else:
    #     reward = 1e-3

    # ------------------------------------------------------
    # Version 3 - Racing Line, Progress, Heading
    # ------------------------------------------------------
    #
    # # Reward formula:
    # # f(r) = r * p
    # # r: racing line factor
    # # p: progress factor
    #
    # # ------------ Racing Line ------------
    # # Reward if the car is close to the racing line
    # # Distance Formula: d = sqrt((x2-x1)**2 + (y2-y1)**2)
    # # The distance formula is calculated in the shapely package
    # current_position = Point(x,y)
    # race_line = LineString(RACING_LINE) # ordered sequence of tuples
    # distance_from_racingline = current_position.distance(race_line) # distance formula
    #
    # # If car is half the width of the track away from the racing line = negative factor
    # raceline_factor = 1 - (distance_from_racingline / (track_width * 0.5))
    # raceline_factor = float(max(raceline_factor,0)) # gets rid of negative factors
    #
    # # ------------ Progress ------------
    #
    # progress_factor = progress / 100
    #
    # # ------------ Heading ------------
    #
    # # Uses direction of the centerline. Might want to change for new racing line
    # waypoints = params['waypoints']
    # closest_waypoints = params['closest_waypoints']
    # heading = params['heading']
    #
    # # Calculate the direction of the center line based on the closest waypoints
    # next_point = waypoints[closest_waypoints[1]]
    # prev_point = waypoints[closest_waypoints[0]]
    #
    # # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    # track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    #
    # # Convert to degree
    # track_direction = math.degrees(track_direction)
    #
    # # Calculate the difference between the track direction and the heading direction of the car
    # direction_diff = abs(track_direction - heading)
    # if direction_diff > 180:
    #     direction_diff = 360 - direction_diff
    #
    # # Penalize the reward if the difference is too large
    # DIRECTION_THRESHOLD = 10.0
    #
    # # ------------ Reward ------------
    # if all_wheels_on_track:
    #     # racing line
    #     reward *= raceline_factor
    #     # progress
    #     reward *= progress_factor
    #     # heading
    #     if direction_diff > DIRECTION_THRESHOLD:
    #         reward *= 0.5
    # else:
    #     reward = 1e-3

    # # ------------------------------------------------------
    # # Version 4 - Racing Line, Faster Progress
    # # ------------------------------------------------------
    #
    # # Reward formula:
    # # f(r) = r * p
    # # r: racing line factor
    # # p: progress factor
    #
    # # ------------ Racing Line ------------
    # # Reward if the car is close to the racing line
    # # Distance Formula: d = sqrt((x2-x1)**2 + (y2-y1)**2)
    # # The distance formula is calculated in the shapely package
    # current_position = Point(x,y)
    # race_line = LineString(RACING_LINE) # ordered sequence of tuples
    # distance_from_racingline = current_position.distance(race_line) # distance formula
    #
    # # If car is half the width of the track away from the racing line = negative factor
    # raceline_factor = 1 - (distance_from_racingline / (track_width * 0.5))
    # raceline_factor = float(max(raceline_factor,0)) # gets rid of negative factors
    #
    # # ------------ Progress ------------
    # # Based on other evaluation logs, it takes 192-199 steps to finish 100%
    # # progress is never greater than steps
    # progress_factor = (progress/steps) # The amount of progress per step
    #
    # # ------------ Reward ------------
    # if all_wheels_on_track:
    #     # racing line
    #     reward *= raceline_factor
    #     # progress
    #     reward *= progress_factor
    #
    # else:
    #     reward = 1e-3

    # # ------------------------------------------------------
    # # Version 5 - Racing Line, Faster Progress, Steering
    # # ------------------------------------------------------
    #
    # # Reward formula:
    # # f(r) = r * p * s
    # # r: racing line factor
    # # p: progress factor
    # # s: steering factor
    #
    # # ------------ Racing Line ------------
    # # Reward if the car is close to the racing line
    # # Distance Formula: d = sqrt((x2-x1)**2 + (y2-y1)**2)
    # # The distance formula is calculated in the shapely package
    # current_position = Point(x,y)
    # race_line = LineString(RACING_LINE) # ordered sequence of tuples
    # distance_from_racingline = current_position.distance(race_line) # distance formula
    #
    # # If car is half the width of the track away from the racing line = negative factor
    # raceline_factor = 1 - (distance_from_racingline / (track_width * 0.5))
    # raceline_factor = float(max(raceline_factor,0)) # gets rid of negative factors
    #
    # # ------------ Progress ------------
    # # Based on other evaluation logs, it takes 192-199 steps to finish 100%
    # # progress is never greater than steps
    # progress_factor = (progress/steps) # The amount of progress per 100 steps
    #
    # # ------------ Steering ------------
    # # Penalize if car steers too much to prevent zigzag
    # ABS_STEERING_THRESHOLD = 15.0
    # if steering > ABS_STEERING_THRESHOLD:
    #     steering_factor = 0.8
    # else:
    #     steering_factor = 1.0
    #
    # # ------------ Reward ------------
    # if all_wheels_on_track:
    #     # racing line
    #     reward *= raceline_factor
    #     # progress
    #     reward *= progress_factor
    #     # steering
    #     reward *= steering_factor
    #
    # else:
    #     reward = 1e-3

    # # -------------------------------------------------------------
    # # Version 6 - Racing Line, Faster Progress, Steering, Throttle
    # # -------------------------------------------------------------
    #
    # # Reward formula:
    # # f(r,p,s,t) = r * p * s * t
    # # r: racing line factor
    # # p: progress factor
    # # s: steering factor
    # # t: throttle factor (speed and steering)
    #
    # # ------------ Racing Line ------------
    # # Reward if the car is close to the racing line
    # # Distance Formula: d = sqrt((x2-x1)**2 + (y2-y1)**2)
    # # The distance formula is calculated in the shapely package
    # current_position = Point(x,y)
    # race_line = LineString(RACING_LINE) # ordered sequence of tuples
    # distance_from_racingline = current_position.distance(race_line) # distance formula
    #
    # # If car is half the width of the track away from the racing line = negative factor
    # raceline_factor = 1 - (distance_from_racingline / (track_width * 0.5))
    # raceline_factor = float(max(raceline_factor,0)) # gets rid of negative factors
    #
    # # ------------ Progress ------------
    # # Based on other evaluation logs, it takes 192-199 steps to finish 100%
    # # progress is never greater than steps
    # progress_factor = (progress/steps) # The amount of progress per 100 steps
    #
    # # ------------ Steering ------------
    # # Penalize if car steers too much to prevent zigzag
    # ABS_STEERING_THRESHOLD = 15.0
    # if steering > ABS_STEERING_THRESHOLD:
    #     steering_factor = 0.8
    # else:
    #     steering_factor = 1.0
    #
    # # ------------ Throttle ------------
    # # Penalize if car steers too much to prevent zigzag
    # SPEED_THRESHOLD = 0.5 # threshold for low speed
    # if speed < SPEED_THRESHOLD:
    #     throttle_factor = 0.5
    # elif speed > 3.0 - steering/15.0: # Decrease throttle (1,2,3) while steering (0,15,30)
    #     throttle_factor = 0.8
    # else:
    #     throttle_factor = 1.0
    #
    # # ------------ Reward ------------
    # if all_wheels_on_track:
    #     # racing line
    #     reward *= raceline_factor
    #     # progress
    #     reward *= progress_factor
    #     # steering
    #     reward *= steering_factor
    #     # throttle
    #     reward *= throttle_factor
    #
    # else:
    #     reward = 1e-3
    #


    # # -------------------------------------------------------------
    # # Version 7 - Racing Line, Faster Progress, Steering
    # # -------------------------------------------------------------
    # # made the racing line stricter
    # # This didn't work - the car wasn't making progress
    #
    # # Reward formula:
    # # f(r,p,s,t) = r * p * s * t
    # # r: racing line factor
    # # p: progress factor
    # # s: steering factor
    # # t: throttle factor (speed and steering)
    #
    # # ------------ Racing Line ------------
    # # Reward if the car is close to the racing line
    # # Distance Formula: d = sqrt((x2-x1)**2 + (y2-y1)**2)
    # # The distance formula is calculated in the shapely package
    # current_position = Point(x,y)
    # race_line = LineString(RACING_LINE) # ordered sequence of tuples
    # distance_from_racingline = current_position.distance(race_line) # distance formula
    #
    # # If car is half the width of the track away from the racing line = negative factor
    # raceline_factor = 1 - (distance_from_racingline / (track_width * 0.25)) # changed to 0.35
    # raceline_factor = float(max(raceline_factor,0)) # gets rid of negative factors
    #
    # # ------------ Progress ------------
    # # Based on other evaluation logs, it takes 192-199 steps to finish 100%
    # # progress is never greater than steps
    # progress_factor = (progress/steps)
    #
    # # ------------ Steering ------------
    # # Penalize if car steers too much to prevent zigzag
    # ABS_STEERING_THRESHOLD = 15.0
    # if steering > ABS_STEERING_THRESHOLD:
    #     steering_factor = 0.8
    # else:
    #     steering_factor = 1.0
    #
    # # ------------ Reward ------------
    # if all_wheels_on_track:
    #     # racing line
    #     reward *= raceline_factor
    #     # progress
    #     reward *= progress_factor
    #     # steering
    #     reward *= steering_factor
    #
    # else:
    #     reward = 1e-3

    # # -------------------------------------------------------------
    # # Version 8 - Faster Progress, Steering
    # # -------------------------------------------------------------
    # # removed the racing line
    #
    # # Reward formula:
    # # f(r,p,s,t) = r * p * s * t
    # # r: racing line factor
    # # p: progress factor
    # # s: steering factor
    # # t: throttle factor (speed and steering)
    #
    # # ------------ Progress ------------
    # # Based on other evaluation logs, it takes 192-199 steps to finish 100%
    # # progress is never greater than steps
    # progress_factor = (progress/steps)
    # TOTAL_NUM_STEPS = 200
    # if (steps % 50) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100 :
    #     progress_factor = 1.5
    # else:
    #     progress_factor = 1
    #
    # # ------------ Steering ------------
    # # Penalize if car steers too much to prevent zigzag
    # ABS_STEERING_THRESHOLD = 15.0
    # if steering > ABS_STEERING_THRESHOLD:
    #     steering_factor = 0.8
    # else:
    #     steering_factor = 1.0
    #
    # # ------------ Reward ------------
    # if all_wheels_on_track:
    #     # progress
    #     reward *= progress_factor
    #     # steering
    #     reward *= steering_factor
    #
    # else:
    #     reward = 1e-3

    return float(reward)
