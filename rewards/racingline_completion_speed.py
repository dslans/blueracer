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


    car_params = {
        'all_wheels_on_track': True,
        'track_width': 17,
        'distance_from_center': 0,
        'speed': 1,
        'steps': 2,
        'progress': 50,
        'steering_angle': 0
    }


import numpy as np
track = np.load('/Users/DanLans/Documents/GitHub/blueracer/tracks/reinvent_base.npy')
track.shape
waypoints = track[:, 0:2]
len(waypoints)

waypoints[0][0]

# Convert waypoints to radians
import math
rad_list = []
len_list = []

for i in range(1,len(waypoints)):
    previous = waypoints[i-1]
    next = waypoints[i]
    dx = next[0] - previous[0]
    dy = next[1] - previous[1]
    rad = math.atan2(dy, dx)
    rad_list.append(rad)

    # save the distance between points
    len_list.append(np.sqrt(dx*dx + dy*dy))



import matplotlib.pyplot as plt
plt.plot([i for i in range(len(rad_list))],rad_list)

# track differencing
rad_diff = [rad_list[i] - rad_list[i-1] for i in range(1,len(rad_list)-1)]
plt.plot([i for i in range(len(rad_diff))], rad_diff)

# Low pass filter
from scipy.signal import butter, lfilter, freqz
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Filter requirements.
order = 10
fs = 30.0       # sample rate, Hz
cutoff = 3.667  # desired cutoff frequency of the filter, Hz

rad_filter = butter_lowpass_filter(rad_diff, cutoff, fs, order)
plt.plot([i for i in range(len(rad_filter))], rad_filter)



dx = len_list[55] * math.cos(rad_filter[55])
dy = len_list[55] * math.sin(rad_filter[55])

waypoints[0]

dx_points = [len_list[i] * math.cos(rad_filter[i]) for i in range(len(rad_filter))]
dy_points = [len_list[i] * math.sin(rad_filter[i]) for i in range(len(rad_filter))]
len(rad_filter)
dx_points[0]
dy_points[0]
waypoints[0]
dx

dy

list(waypoints[0])
new_coordinates= []
for i in range(len(waypoints)):
    if (i > 1) & (i < len(waypoints)-1):
        coordinates = [
            waypoints[i][0] + dx_points[i-2],
            waypoints[i][0] + dy_points[i-2]
        ]
    else:
        coordinates = list(waypoints[i])
    new_coordinates.append(coordinates)

waypoints[0]

waypoints[0] * [1,0]


def plot_tracknumbers(trackpoints, show=True):
    import matplotlib.pyplot as plt
    for i in range(len(trackpoints)):
        plt.scatter(trackpoints[i][0], trackpoints[i][1], c='blue', s=8)
        plt.scatter(trackpoints[i][2], trackpoints[i][3], c='black', s=8)
        plt.scatter(trackpoints[i][4], trackpoints[i][5], c='black', s=8)

        plt.scatter(new_coordinates[i][0], new_coordinates[i][1], c='red', s=35, marker="^")

        plt.annotate(f'{i}', # this is the text
             (trackpoints[i][0],trackpoints[i][1]), # this is the point to label
             textcoords="offset points", # how to position the text
             xytext=(0,10), # distance from text to points (x,y)
             ha='center') # horizontal alignment can be left, right or center

        plt.annotate(f'{i}', # this is the text
             (trackpoints[i][2],trackpoints[i][3]), # this is the point to label
             textcoords="offset points", # how to position the text
             xytext=(0,10), # distance from text to points (x,y)
             ha='center') # horizontal alignment can be left, right or center

        plt.annotate(f'{i}', # this is the text
             (trackpoints[i][4],trackpoints[i][5]), # this is the point to label
             textcoords="offset points", # how to position the text
             xytext=(0,10), # distance from text to points (x,y)
             ha='center') # horizontal alignment can be left, right or center
    if show:
        plt.show()

import pandas as pd
track = np.load('/Users/DanLans/Documents/GitHub/blueracer/tracks/reinvent_base.npy')
waypoint_changes = pd.read_csv('/Users/DanLans/Documents/GitHub/blueracer/tracks/reinvent_base_changes.csv')

x_change = np.array(waypoint_changes['x_change'])
y_change = np.array(waypoint_changes['y_change'])


new_coordinates = []
for i in range(len(waypoints)):
    coordinates = waypoints[i] * [1+x_change[i], 1+y_change[i]]
    new_coordinates.append(coordinates)
plt.figure(figsize=(15,10))
plot_tracknumbers(track)


slope = (waypoints[28][1] - waypoints[39][1]) / (waypoints[28][0] - waypoints[39][0])
slope
newpoints_list = []
for i in range(len(waypoints[28:39])):
    newy = waypoints[i][0]*slope
    newpoints = [waypoints[i][0], newy]
    newpoints_list.append(newpoints)

waypoints[28:39]
newpoints_list

import matplotlib.pyplot as plt
def plot_points(ax, points):
    ax.scatter(points[:-1,0], points[:-1,1], s=1)
    for i,p in enumerate(points):
        ax.annotate(i, (p[0], p[1]))
    plt.show()

fig, ax = plt.subplots(figsize=(20,10))
plot_points(ax, waypoints)
plt.show()

# Plot the results
fig, ax = plt.subplots(figsize=(20,10))
plot_points(ax, track[:-1,0:2])
plot_points(ax, track[:-1,2:4])
plot_points(ax, track[:-1,4:6])
ax.axis('equal')
plt.show()


reward_function(car_params)

for progress in range(0,100):
    car_params.update({'progress': progress})
    print(progress, ':', reward_function(car_params))


for center_distance in range(0,9):
    car_params.update({'distance_from_center': center_distance})
    print(center_distance, ':', reward_function(car_params))

    # ------------------------------------------------------
    # Version 2 - Progress + Staying within the track
    # ------------------------------------------------------

    # The most simple reward function: reward for making progress on the track
    if all_wheels_on_track and (0.5*track_width - distance_from_center) >= 0.05:
        reward = 1 # Gives a new default reward if car is on the track
        reward += progress / 100 # Value 0-1
    else:
        reward = 1e-3
