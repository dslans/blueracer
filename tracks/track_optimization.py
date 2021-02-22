# =====================================
# DeepRacer Track Optimization
# =====================================

# Used the formula from the following github:
# https://github.com/cdthompson/deepracer-k1999-race-lines

# ----- Load track -----
import numpy as np
track = np.load('/Users/DanLans/Documents/GitHub/blueracer/tracks/reinvent_base.npy')
centertrack = track[:, 0:2] # The centerline is the first pair
innertrack = track[:,2:4] # inner track is middle pair
outertrack = track[:,4:] # outer track is last pair

# number of waypoints
len(track)


# ----- Plot Waypoints -----
import matplotlib.pyplot as plt
def plot_tracknumbers(centertrack, innertrack, outertrack, show=True):
    tracklines = [centertrack,innertrack,outertrack]
    trackcolors = ['blue','black','black']

    for t in range(len(tracklines)):
        plt.plot(tracklines[t][:,0], tracklines[t][:,1], c=trackcolors[t])

    for i in range(len(track)):
        for j in range(len(tracklines)):
            plt.scatter(tracklines[j][i][0], tracklines[j][i][1],
            c=trackcolors[j],
            s=10)

            plt.annotate(f'{i}', # this is the text
            (tracklines[j][i][0],tracklines[j][i][1]), # this is the point to label
            textcoords="offset points", # how to position the text
            xytext=(0,10), # distance from text to points (x,y)
            ha='center') # horizontal alignment can be left, right or center

    if show:
        plt.show()

plt.figure(figsize=(10,6))
plot_tracknumbers(centertrack, innertrack, outertrack)



# ----- Algorithm -----
def menger_curvature(pt1, pt2, pt3, atol=1e-3):

    vec21 = np.array([pt1[0]-pt2[0], pt1[1]-pt2[1]])
    vec23 = np.array([pt3[0]-pt2[0], pt3[1]-pt2[1]])

    norm21 = np.linalg.norm(vec21)
    norm23 = np.linalg.norm(vec23)

    theta = np.arccos(np.dot(vec21, vec23)/(norm21*norm23))
    if np.isclose(theta-np.pi, 0.0, atol=atol):
        theta = 0.0

    dist13 = np.linalg.norm(vec21-vec23)

    return 2*np.sin(theta) / dist13

import copy
from shapely.geometry import Point, Polygon
from shapely.geometry.polygon import LinearRing, LineString

# Number of times to iterate each new race line point
# keep this at 3-8 for best balance of performance and desired result
XI_ITERATIONS=4

# Number of times to scan the entire race track to iterate
# 500 will get a good start, 1500 will be closer to optimal result
LINE_ITERATIONS=1000

def improve_race_line(old_line, inner_border, outer_border):
    '''Use gradient descent, inspired by K1999, to find the racing line'''
    # start with the center line
    new_line = copy.deepcopy(old_line)
    ls_inner_border = Polygon(inner_border)
    ls_outer_border = Polygon(outer_border)
    for i in range(0,len(new_line)):
        xi = new_line[i]
        npoints = len(new_line)
        prevprev = (i - 2 + npoints) % npoints
        prev = (i - 1 + npoints) % npoints
        nexxt = (i + 1 + npoints) % npoints
        nexxtnexxt = (i + 2 + npoints) % npoints
        #print("%d: %d %d %d %d %d" % (npoints, prevprev, prev, i, nexxt, nexxtnexxt))
        ci = menger_curvature(new_line[prev], xi, new_line[nexxt])
        c1 = menger_curvature(new_line[prevprev], new_line[prev], xi)
        c2 = menger_curvature(xi, new_line[nexxt], new_line[nexxtnexxt])
        target_ci = (c1 + c2) / 2
        #print("i %d ci %f target_ci %f c1 %f c2 %f" % (i, ci, target_ci, c1, c2))

        # Calculate prospective new track position, start at half-way (curvature zero)
        xi_bound1 = copy.deepcopy(xi)
        xi_bound2 = ((new_line[nexxt][0] + new_line[prev][0]) / 2.0, (new_line[nexxt][1] + new_line[prev][1]) / 2.0)
        p_xi = copy.deepcopy(xi)
        for j in range(0,XI_ITERATIONS):
            p_ci = menger_curvature(new_line[prev], p_xi, new_line[nexxt])
            #print("i: {} iter {} p_ci {} p_xi {} b1 {} b2 {}".format(i,j,p_ci,p_xi,xi_bound1, xi_bound2))
            if np.isclose(p_ci, target_ci):
                break
            if p_ci < target_ci:
                # too flat, shrinking track too much
                xi_bound2 = copy.deepcopy(p_xi)
                new_p_xi = ((xi_bound1[0] + p_xi[0]) / 2.0, (xi_bound1[1] + p_xi[1]) / 2.0)
                if Point(new_p_xi).within(ls_inner_border) or not Point(new_p_xi).within(ls_outer_border):
                    xi_bound1 = copy.deepcopy(new_p_xi)
                else:
                    p_xi = new_p_xi
            else:
                # too curved, flatten it out
                xi_bound1 = copy.deepcopy(p_xi)
                new_p_xi = ((xi_bound2[0] + p_xi[0]) / 2.0, (xi_bound2[1] + p_xi[1]) / 2.0)

                # If iteration pushes the point beyond the border of the track,
                # just abandon the refinement at this point.  As adjacent
                # points are adjusted within the track the point should gradually
                # make its way to a new position.  A better way would be to use
                # a projection of the point on the border as the new bound.  Later.
                if Point(new_p_xi).within(ls_inner_border) or not Point(new_p_xi).within(ls_outer_border):
                    xi_bound2 = copy.deepcopy(new_p_xi)
                else:
                    p_xi = new_p_xi
        new_xi = p_xi
        # New point which has mid-curvature of prev and next points but may be outside of track
        #print((new_line[i], new_xi))
        new_line[i] = new_xi
    return new_line


print(len(centertrack))
# start along centerline of track
race_line = copy.deepcopy(centertrack[:-1])  # Use this for centerline being outer bound
for i in range(LINE_ITERATIONS):
    race_line = improve_race_line(race_line, innertrack, outertrack)
    if i % 20 == 0: print("Iteration %d" % i)


# need to put duplicate point race_line[0] at race_line[-1] to make a closed loops
loop_race_line = np.append(race_line, [race_line[0]], axis=0)

# old lengths of tracks
l_center_line = LineString(centertrack)
l_inner_border = LineString(innertrack)
l_outer_border = LineString(outertrack)
print("These should be the same: ", (centertrack.shape, loop_race_line.shape))
print("Original centerline length: %0.2f" % l_center_line.length)
print("New race line length: %0.2f" % LineString(loop_race_line).length)

# New racing line
plt.figure(figsize=(10,6))
plot_tracknumbers(loop_race_line, innertrack, outertrack)

# Plot centerline with optimal racing line
def plot_racingline(centertrack, innertrack, outertrack, racing_line, annotate=True, show=True):
    tracklines = [centertrack,innertrack,outertrack, racing_line]
    trackcolors = ['blue','black','black', 'orange']

    for t in range(len(tracklines)):
        plt.plot(tracklines[t][:,0], tracklines[t][:,1], c=trackcolors[t])

    for i in range(len(track)):
        for j in range(len(tracklines)):
            plt.scatter(tracklines[j][i][0], tracklines[j][i][1],
            c=trackcolors[j],
            s=10)
            if annotate:
                plt.annotate(f'{i}', # this is the text
                (tracklines[j][i][0],tracklines[j][i][1]), # this is the point to label
                textcoords="offset points", # how to position the text
                xytext=(0,10), # distance from text to points (x,y)
                ha='center') # horizontal alignment can be left, right or center

    if show:
        plt.show()

plt.figure(figsize=(10,6))
plot_racingline(centertrack, innertrack, outertrack, loop_race_line, annotate=False)

loop_race_line


# Save the racing line
import pickle
pickle.dump(loop_race_line, open('tracks/reinvent_base_racingline.p', 'wb'))
