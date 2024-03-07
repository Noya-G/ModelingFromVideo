# ModelingFromVideo
# using Optical Flow Estimation


This Python script analyzes frames extracted from a video to detect camera movements. It utilizes optical flow estimation techniques to compare consecutive frames and identify translation and rotation movements of the camera.

to read more abot Optical Flow Estimation https://en.wikipedia.org/wiki/Optical_flow

## Requirements

- Python 3.x
- OpenCV (cv2) library
- NumPy library

You can install the required Python libraries using pip:

```
pip install opencv-python numpy
```

## Usage

1. Clone or download the repository to your local machine.
2. Place your video file (in .mp4 format) in the same directory as the script.
3. Modify the `video_path` variable in the script to point to your video file.
4. Run the script:

```
python frame_analysis.py
```

5. The script will extract frames from the video, estimate camera movements, select frames with significant movements, and save them as images in a specified output folder.

## Parameters

- `SKIP`: Number of frames to skip for estimating camera movement.
- `THRESHOLD`: Threshold values for translation distance and rotation angle to select frames with significant movement.

## Output

- The script will print the total number of frames extracted, the camera movement estimation for each frame pair, and the number of selected frames with significant movement.
- Selected frames with significant movement will be saved as individual image files in the specified output folder.

Example

Below are examples of selected frames with significant movement:

![Screenshot 2024-03-07 at 15 41 22](https://github.com/Noya-G/ModelingFromVideo/assets/73538626/d75df5b6-dd5d-4240-a25b-942f23721e3c)

linke to the video [video](https://www.youtube.com/watch?v=DszOxc3r-WM)


Output

The script will print the total number of frames extracted, the camera movement estimation for each frame pair, and the number of selected frames with significant movement.
Selected frames with significant movement will be saved as individual image files in the specified output folder.

![Screenshot 2024-03-07 at 15 41 49](https://github.com/Noya-G/ModelingFromVideo/assets/73538626/4e71c81d-4ab2-4843-8824-d6952d8d80d7)


## Author

- [Noya Gendelman](https://github.com/Noya-G)
- [Bat-Ya Ashkenazi](https://github.com/Noya-G)

## License

This project is licensed under the [MIT License](LICENSE).
