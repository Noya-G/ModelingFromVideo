import os

import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor

SKIP = 20 # Number of frames to skip
THRESHOLD = 10
def extract_frames(video_path):
    # Open the video file
    video_capture = cv2.VideoCapture(video_path)

    frames = []

    # Loop through each frame in the video
    while True:
        # Read the next frame
        success, frame = video_capture.read()

        # If there are no more frames, break the loop
        if not success:
            break

        # Append the frame to the list
        frames.append(frame)

    # Release the video capture object
    video_capture.release()

    return frames


def estimate_camera_movement(frame1, frame2):
    # Convert frames to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Feature detection and matching (using SIFT)
    sift = cv2.SIFT_create()
    keypoints1, descriptors1 = sift.detectAndCompute(gray1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(gray2, None)

    # Match keypoints between the frames
    matcher = cv2.BFMatcher()
    matches = matcher.knnMatch(descriptors1, descriptors2, k=2)

    # Apply ratio test to select good matches
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    # Estimate transformation (homography)
    src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    H, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    # Decompose transformation
    dx = H[0, 2]  # Translation in x direction
    dy = H[1, 2]  # Translation in y direction
    theta = np.arctan2(H[1, 0], H[0, 0]) * 180 / np.pi  # Rotation angle (in degrees)

    # Calculate camera movement
    translation_distance = np.sqrt(dx ** 2 + dy ** 2)

    return translation_distance, theta


def movement_estimator(frames):
    estimator = []
    with ThreadPoolExecutor() as executor:
        futures = []
        for i in range(0, len(frames) - SKIP, SKIP):
            frame1 = frames[i]
            frame2 = frames[i + SKIP]
            future = executor.submit(estimate_camera_movement, frame1, frame2)
            futures.append((i, i + SKIP, future))  # Store the frame indexes along with the future object

        # Retrieve results
        for start_index, end_index, future in futures:
            translation_distance, theta = future.result()
            estimator.append((start_index, end_index, translation_distance, theta))  # Include the frame indexes in the results
    return estimator


def select_frames(movement):
    selected_frames = []
    for start_index, end_index, translation_distance, theta in movement:
        if (translation_distance >THRESHOLD
                or abs(theta) > THRESHOLD):
            selected_frames.append(start_index)

    return selected_frames


def get_selected_frames(selected_frame_indexes, frames):
    selected_frames = []
    for index in selected_frame_indexes:
        selected_frames.append(frames[index])
    return selected_frames


def save_frames_as_photos(frames, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save each frame as an image file
    for i, frame in enumerate(frames):
        filename = os.path.join(output_folder, f"frame_{i}.jpg")
        cv2.imwrite(filename, frame)

if __name__ == "__main__":
    video_path = "            "  ###Enter here thr mp4 file path
    all_frames = extract_frames(video_path)
    print(f"Total frames extracted: {len(all_frames)}")
    estimator = movement_estimator(all_frames)
    print(estimator)
    print(len(estimator))
    selectFrames = select_frames(estimator)
    print(selectFrames)
    print(len(selectFrames))
    choosen = get_selected_frames(selectFrames,all_frames)
    print(len(choosen))
    save_frames_as_photos(choosen,
                          "        ") ###Enter folder path you the frames to be sved on.

    #print(choosen)


