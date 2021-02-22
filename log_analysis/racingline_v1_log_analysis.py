# ===================================
# Log analysis for racing line
# ===================================
import numpy as np
import pandas as pd
import sys
sys.path.append('/Users/DanLans/Google Drive/DeepRacerDrive')

# Import AWS log analysis files
import log_analysis as la
import track_utils as tu
import cw_utils as cw

# Import training files
logfolder = '/Users/DanLans/Google Drive/DeepRacerDrive/logs/DL-eagle5-racingline/logs'
logfile = 'training/training-20210215211722-lvei4EZzQxS9hl0wCQe-SQ-robomaker.log'
training = la.load_data(f'{logfolder}/{logfile}')
training_df = la.convert_to_pandas(training)
training_df.head()

progsteps = training_df.progress / training_df.steps


track = np.load('/Users/DanLans/Documents/GitHub/blueracer/tracks/reinvent_base.npy')
track[:, 0:2]


df = training_df[(training_df.iteration == 9)]
car_path = np.array(df[['x','y']])
reward = df.reward

df.head()

# car distance to racing line
from shapely.geometry import Point, Polygon
from shapely.geometry.polygon import LinearRing, LineString

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


race_line = LineString(RACING_LINE) # ordered sequence of tuples


car_distance = []
raceline_factor = []
for i in range(len(car_path)):
    current_position = Point(car_path[i][0], car_path[i][1])
    distance_from_racingline = current_position.distance(race_line) # distance formula
    # If half the width of the track away from the racing line = negative factor
    factor = 1 - (distance_from_racingline / (17.71 * 0.5))
    factor = float(max(factor,0.0))
    car_distance.append(distance_from_racingline)
    raceline_factor.append(factor)

reward_df = pd.DataFrame({
    'DISTANCE_FROM_RACINGLINE': car_distance,
    'RACELINE_FACTOR': raceline_factor,
    'REWARD': reward,
    'X':df.x,
    'Y':df.y,
    'ON_TRACK': df.on_track,
    'PROGRESS': df.progress
})

import matplotlib.pyplot as plt
plt.figure(figsize=(10,6))
plt.scatter(reward_df[reward_df.ON_TRACK=='True'].DISTANCE_FROM_RACINGLINE,
            reward_df[reward_df.ON_TRACK=='True'].REWARD)
plt.xlabel('Distance From Racing Line')
plt.ylabel('Reward')

reward_df.REWARD.max()

reward_df


## ---------------------------------------------------
## Racingline2
## ---------------------------------------------------
# Import training files
logfolder = '/Users/DanLans/Google Drive/DeepRacerDrive/logs/DL-eagle5-racingline2/logs'
logfile = 'training/training-20210216003130-pLHJ0rlrT0SdeY050k5p9Q-robomaker.log'
training = la.load_data(f'{logfolder}/{logfile}')
training_df = la.convert_to_pandas(training)
training_df.head()

df = training_df[(training_df.iteration == 15)]
car_path = np.array(df[['x','y']])
reward = df.reward

car_distance = []
raceline_factor = []
for i in range(len(car_path)):
    current_position = Point(car_path[i][0], car_path[i][1])
    distance_from_racingline = current_position.distance(race_line) # distance formula
    # If half the width of the track away from the racing line = negative factor
    factor = 1 - (distance_from_racingline / (17.71 * 0.5))
    factor = float(max(factor,0.0))
    car_distance.append(distance_from_racingline)
    raceline_factor.append(factor)

reward_df = pd.DataFrame({
    'DISTANCE_FROM_RACINGLINE': car_distance,
    'RACELINE_FACTOR': raceline_factor,
    'REWARD': reward,
    'X':df.x,
    'Y':df.y,
    'ON_TRACK': df.on_track,
    'PROGRESS': df.progress
})

import matplotlib.pyplot as plt
plt.figure(figsize=(10,6))
plt.scatter(reward_df[reward_df.ON_TRACK=='True'].PROGRESS,
            reward_df[reward_df.ON_TRACK=='True'].REWARD,
            c=reward_df[reward_df.ON_TRACK=='True'].DISTANCE_FROM_RACINGLINE)
# plt.xlabel('Distance From Racing Line')
plt.xlabel('Progress')
plt.ylabel('Reward')





## ---------------------------------------------------
## Blueracer Racingline1
## ---------------------------------------------------
# Import training files
logfolder = '/Users/DanLans/Google Drive/DeepRacerDrive/logs/DL-blueracer-racingline/logs'
logfile = 'training/training-20210216090724-hLNXSZE3R2KJf3pHKDtp7A-robomaker.log'
training = la.load_data(f'{logfolder}/{logfile}')
training_df = la.convert_to_pandas(training)
training_df.head()

training_df[training_df.iteration==25].groupby(["iteration"])['progress'].mean()

df = training_df[(training_df.iteration == 70)]
car_path = np.array(df[['x','y']])
reward = df.reward

car_distance = []
raceline_factor = []
for i in range(len(car_path)):
    current_position = Point(car_path[i][0], car_path[i][1])
    distance_from_racingline = current_position.distance(race_line) # distance formula
    # If half the width of the track away from the racing line = negative factor
    factor = 1 - (distance_from_racingline / (17.71 * 0.5))
    factor = float(max(factor,0.0))
    car_distance.append(distance_from_racingline)
    raceline_factor.append(factor)

reward_df = pd.DataFrame({
    'DISTANCE_FROM_RACINGLINE': car_distance,
    'RACELINE_FACTOR': raceline_factor,
    'REWARD': reward,
    'X':df.x,
    'Y':df.y,
    'ON_TRACK': df.on_track,
    'PROGRESS': df.progress
})

import matplotlib.pyplot as plt
plt.figure(figsize=(10,6))
plt.scatter(reward_df[reward_df.ON_TRACK=='True'].PROGRESS,
            reward_df[reward_df.ON_TRACK=='True'].REWARD,
            c=reward_df[reward_df.ON_TRACK=='True'].DISTANCE_FROM_RACINGLINE)
# plt.xlabel('Distance From Racing Line')
plt.xlabel('Progress')
plt.ylabel('Reward')




## ---------------------------------------------------
## Blueracer Racingline2
## ---------------------------------------------------
# Import training files
logfolder = '/Users/DanLans/Google Drive/DeepRacerDrive/logs/DL-blueracer-racingline2/logs'
logfile = 'training/training-20210216092821-4z25ywBzQNCNBABvtdgOzg-robomaker.log'
training = la.load_data(f'{logfolder}/{logfile}')
training_df = la.convert_to_pandas(training)
training_df.head()

training_df.groupby("iteration")['progress'].mean().max()

df = training_df[(training_df.iteration == 70)]
car_path = np.array(df[['x','y']])
reward = df.reward

car_distance = []
raceline_factor = []
for i in range(len(car_path)):
    current_position = Point(car_path[i][0], car_path[i][1])
    distance_from_racingline = current_position.distance(race_line) # distance formula
    # If half the width of the track away from the racing line = negative factor
    factor = 1 - (distance_from_racingline / (17.71 * 0.5))
    factor = float(max(factor,0.0))
    car_distance.append(distance_from_racingline)
    raceline_factor.append(factor)

reward_df = pd.DataFrame({
    'DISTANCE_FROM_RACINGLINE': car_distance,
    'RACELINE_FACTOR': raceline_factor,
    'REWARD': reward,
    'X':df.x,
    'Y':df.y,
    'ON_TRACK': df.on_track,
    'PROGRESS': df.progress
})

import matplotlib.pyplot as plt
plt.figure(figsize=(10,6))
plt.scatter(reward_df[reward_df.ON_TRACK=='True'].PROGRESS,
            reward_df[reward_df.ON_TRACK=='True'].REWARD,
            c=reward_df[reward_df.ON_TRACK=='True'].DISTANCE_FROM_RACINGLINE)
# plt.xlabel('Distance From Racing Line')
plt.xlabel('Progress')
plt.ylabel('Reward')
