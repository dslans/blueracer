
# ==========================================================
# ==========================================================
# Racing line, Progress, Sterring Reward Function
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

    # Get the previous and next waypoints.
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]


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
    reward = 1e-6

    # ------------------------------------------------------
    # Racing Line
    #
    # Reward is beween 0 and 1
    # Reward if the car is close to the racing line
    # Distance Formula: d = sqrt((x2-x1)**2 + (y2-y1)**2)
    # The distance formula is calculated in the shapely package
    # ------------------------------------------------------

    current_position = Point(x,y)
    race_line = LineString(RACING_LINE) # ordered sequence of tuples
    distance_from_racingline = current_position.distance(race_line) # distance formula

    # If car is half the width of the track away from the racing line = negative factor
    racingline_reward = 1 - (distance_from_racingline / (track_width * 0.3))
    racingline_reward = float(max(racingline_reward,0)) # gets rid of negative factors

    # ------------------------------------------------------
    # Steering
    # ------------------------------------------------------
    # Penalize if car steers too much to prevent zigzag
    ABS_STEERING_THRESHOLD = 15.0
    if steering > ABS_STEERING_THRESHOLD:
        steering_factor = 0.8
    else:
        steering_factor = 1.0

    # ------------------------------------------------------
    # Direction
    # ------------------------------------------------------

    # Need to find closest waypoints in racing line
    raceline_distances = [get_distance(x,y,point[0],point[1]) for point in RACING_LINE]
    closest_raceline_index = raceline_distances.index(min(raceline_distances))
    if closest_raceline_index < len(RACING_LINE):
        next_point = RACING_LINE[closest_raceline_index+1]
    else:
        next_point = RACING_LINE[0] # avoid errors with last index

    DIRECTION_THRESHOLD = 5.0
    PENALTY_FACTOR = 1e-6
    SLOPE = ( PENALTY_FACTOR - 1 ) / ( DIRECTION_THRESHOLD - 0 )

    # Compute direction difference between car's current heading
    # and the next waypoint.
    direction_diff = get_direction_diff(heading, x, y, next_point[0], next_point[1])

    # Initialize the reward with typical value.
    direction_reward = 1.0

    # Adjust the reward by the direction.
    if direction_diff > DIRECTION_THRESHOLD:
        direction_reward *= PENALTY_FACTOR
    else:
        direction_reward *= ( (SLOPE*direction_diff) + 1 )

    # ------------------------------------------------------
    # Reward Totals
    # ------------------------------------------------------
    if all_wheels_on_track:
        reward += (racingline_reward + direction_reward)*steering_factor
    else:
        reward = 1e-6

    return float(reward)


# ===============================
# Helper Functions
# ===============================
# Function for direction of waypoints
def get_direction(x1, y1, x2, y2):
    # Calculate the direction in radians, arctan2(dy, dx), the result is (-pi, pi) in radians.
    track_direction = math.atan2(y2 - y1, x2 - x1)

    # Convert from radians to degrees
    track_direction = math.degrees(track_direction)

    return(track_direction)

# Distance between waypoints
def get_distance(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    track_distance = math.sqrt(dx*dx+dy*dy)
    return(track_distance)

# Define a function that computes the direction indicated by
# x_prev, y_prev, x_next, y_next. Then computes the
# difference between some reference direction (e.g., the car's
# current heading) and this direction, and returns this difference.
def get_direction_diff(reference_direction, x1, y1, x2, y2):
    # Calculate the direction in radians, arctan2(dy, dx), the result is (-pi, pi) in radians.
    track_direction = get_direction(x1, y1, x2, y2)

    # Calculate the absolute difference between the track direction
    # and the reference direction.
    direction_diff = abs(track_direction - reference_direction)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    return(direction_diff)
