import cv2 as cv
import numpy as np
import os
import matplotlib.pyplot as plt

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Can use IMREAD flags to do different pre-processing of image files,
# like making them grayscale or reducing the size.
# https://docs.opencv.org/4.2.0/d4/da8/group__imgcodecs.html
range_img = cv.imread('valo_bots.png', cv.IMREAD_UNCHANGED)
bot_img = cv.imread('valo_bot_crop.png', cv.IMREAD_UNCHANGED)

# There are 6 comparison methods to choose from:
# TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
# You can see the differences at a glance here:
# https://docs.opencv.org/master/d4/dc6/tutorial_py_template_matching.html
# Note that the values are inverted for TM_SQDIFF and TM_SQDIFF_NORMED
result = cv.matchTemplate(range_img, bot_img, cv.TM_CCOEFF_NORMED)

# # use matplotlib to plot the images side by side
# fig, ax = plt.subplots(1,2)
# ax[0].imshow(range_img)
# ax[1].imshow(bot_img)
# plt.show()
#
# # use matplotlib to visualize the range_img and result output side by side
# fig, ax = plt.subplots(1,2)
# ax[0].imshow(range_img)
# ax[1].imshow(result)
# plt.show()

# You can view the result of matchTemplate() like this:
#cv.imshow('Result', result)
#cv.waitKey()
# If you want to save this result to a file, you'll need to normalize the result array
# from 0..1 to 0..255, see:
# https://stackoverflow.com/questions/35719480/opencv-black-image-after-matchtemplate
#cv.imwrite('result_CCOEFF_NORMED.jpg', result * 255)

# Get the best match position from the match result.
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
# The max location will contain the upper left corner pixel position for the area
# that most closely matches our bot image. The max value gives an indication
# of how similar that find is to the original bot, where 1 is perfect and -1
# is exact opposite.
print('Best match top left position: %s' % str(max_loc))
print('Best match confidence: %s' % max_val)

# If the best match value is greater than 0.8, we'll trust that we found a match
threshold = 0.8
if max_val >= threshold:
    print('Found bot.')

    # Get the size of the bot image. With OpenCV images, you can get the dimensions
    # via the shape property. It returns a tuple of the number of rows, columns, and 
    # channels (if the image is color):
    bot_w = bot_img.shape[1]
    bot_h = bot_img.shape[0]

    # Calculate the bottom right corner of the rectangle to draw
    top_left = max_loc
    bottom_right = (top_left[0] + bot_w, top_left[1] + bot_h)

    # Draw a rectangle on our screenshot to highlight where we found the bot.
    # The line color can be set as an RGB tuple
    cv.rectangle(range_img, top_left, bottom_right,
                    color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

    # use matplotlib to visualize the range_img and result output side by side
    # fig, ax = plt.subplots(1,2)
    # ax[0].imshow(range_img)
    # ax[1].imshow(result)
    # plt.show()

    # You can view the processed screenshot like this:
    #cv.imshow('Result', range_img)
    #cv.waitKey()
    # Or you can save the results to a file.
    # imwrite() will smartly format our output image based on the extension we give it
    # https://docs.opencv.org/3.4/d4/da8/group__imgcodecs.html#gabbc7ef1aa2edfaa87772f1202d67e0ce
    cv.imwrite('result.jpg', range_img)

else:
    print('Bot not found.')

# now we iterate through our result np array and find ALL of the cases where confidence is greater than 0.8
# then we draw a rectangle around each of those cases
# then we save the image to a file

range_img = cv.imread('valo_bots.png', cv.IMREAD_UNCHANGED)
match_h, match_w = np.where(result >= 0.6)

for mt_h, mt_w in zip(match_h, match_w):
    top_left = (mt_w, mt_h)
    bottom_right = (top_left[0] + bot_w, top_left[1] + bot_h)
    cv.rectangle(range_img, top_left, bottom_right,
                    color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

cv.imwrite('result_all_boxes.jpg', range_img)