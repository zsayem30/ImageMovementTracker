import imageio

import numpy        as np
import scipy.signal as sp

def correlate_adjacent_frames( previous_frame, current_frame ):
    ''' 
        This function takes in two NumPy arrays filled with uint8 (integers between 0 and 255 inclusive) of size 160 by 160 and returns a 
        NumPy array of uint8 that represents `previous_frame` being cross correlated with a convolutional kernel of size 110 by 110 created 
        by removing the first and last 25 pixels in each dimension from `current_frame`. 

        The array returned should be of size 110 by 110 but the elements that are dependent on values "outside" the provided pixels of 
        `previous_frame` should be set to zero.

        Before computing the cross-correlation, you should normalize the input arrays in the range 0 to 1 and then subtracting the mean pixel 
        value of both inputs (i.e. the mean value of the list created by concatenating all pixel intensities of `current_frame` and all pixel
        intensities of `previous_frame`)
    '''
    max_value = 255
    min_value = 0
    norm_input1 = previous_frame/max_value
    norm_input2 = current_frame/max_value
    avg_input1 = np.mean(norm_input1)
    avg_input2 = np.mean(norm_input2)
    adjustedInput1 = norm_input1-avg_input1
    adjustedInput2 = norm_input2-avg_input2
    inputsubArray2 = adjustedInput2[25:135,25:135]
    y = sp.correlate2d(adjustedInput1,inputsubArray2, mode='valid', boundary='fill', fillvalue=0)
    ymax = np.amax(y)
    ymin = np.amin(y)
    m = max_value/(ymax-ymin)
    c = max_value-m*ymax
    y_adj = m*y + c
    y_int = y_adj.astype('uint8')
    return y_int

def make_correlation_video( input_filename, output_filename=None ):
    '''
        This function takes in an input filename string of a GIF and an optional output filename string. It should read the video from the input filename 
        using the mimread function from imageio and then apply correlate_adjacent_frames to each pair of adjacent frames 
        (i.e. between frame 0 and frame 1 then frame 1 and frame 2, and so on) to create a video (list of frames) with one less frame than the number of
        frames in the input GIF.

        If the output_filename is present (i.e. is not None), it should then write the resulting frames into a GIF located at the output filename string 
        using the mimwrite function from imageio, then in either case the function should return the video as a three-dimensional NumPy array.

        You may assume the file located at input_filename is in a fact a GIF (you do not need to handle the error condition where it is some other file type)

        Note: In this context a 'video' is a three-dimensional NumPy array that can best be thought of as a list of two-dimensional 'frames' which are 
        NumPy arrays.

        While debugging the last function, you can view these GIF outputs using a web browser or image viewer, they are just regular GIFs.
    '''
    vid = imageio.mimread(input_filename)
    new_vid = []
    for index, frame in enumerate(vid):
        if index == 0:
            current_frame = frame
            previous_frame = frame

        else:
            previous_frame = current_frame
            current_frame = frame
            corr_frame = correlate_adjacent_frames(previous_frame,current_frame)
            new_vid.append(corr_frame)

    if output_filename is not None:
        imageio.mimwrite(output_filename, new_vid)

    return new_vid

def is_triangular_path( filename ):
    ''' 
        This function takes in an input filename string of a GIF. It should use the mimread function from imageio to load the GIF into a NumPy array.
        You may assume this video is sweeping over an image in either a triangular or square path. 

        The function should then use the make_correlation_video function to get a three-dimensional NumPy array and apply some heuristic to this video in
        order to disern a triangular path video from a square path video. It should return False if the video is a square path and True if the video is a 
        triangular path. If the path is neither a triangular or square path you can do whatever (you need not handle this case).
    '''
    #Reading the file and making an array of frames
    vid = make_correlation_video(filename)
    radius = 5 #pixels
    corners = [1]

    #finding the index of the brightest/largest value in matrix
    for index, frame in enumerate(vid):
        if index == 0:
             x_previous, y_previous = np.unravel_index(np.argmax(frame), frame.shape)

        x_current,y_current = np.unravel_index(np.argmax(frame), frame.shape)
        norm_1 = abs(x_previous-x_current)+abs(y_previous-y_current)

        if norm_1 > radius:
            corners.append(1)
            x_previous = x_current
            y_previous = y_current

    if len(corners) == 4:
        return False
    elif len(corners) == 3:
        return True
    else:
        return None
