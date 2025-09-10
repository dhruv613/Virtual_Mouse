# Virtual Mouse Project

## Project Overview
The **Virtual Mouse Project** is a computer vision-based system that allows users to control their computer’s mouse using **hand gestures** detected through a webcam. By leveraging **OpenCV**, **Mediapipe**, and **PyAutoGUI**, the project tracks hand landmarks in real-time and translates gestures into mouse movements, clicks, and scroll actions.  

This eliminates the need for a physical mouse, offering a touch-free and interactive human-computer interface.

## Features
- **Cursor Movement**: Move the mouse cursor by raising the index finger.  
- **Clicking**: Simulate mouse clicks by bringing the index and middle fingers close together.  
- **Scrolling**: Scroll up or down when both index and middle fingers are raised.  
- **Fist Gesture (Optional)**: Detects a closed fist gesture to minimize all windows (commented in code).  
- **Frame Reduction**: Limits movement to a certain area of the camera for smoother mapping.  
- **Smoothing**: Adds smoothing to reduce jitter and provide stable cursor movement.  
- **FPS Counter**: Displays real-time FPS to monitor system performance.  

## Technologies Used
- **Python** – Core programming language.  
- **OpenCV** – For video capture, drawing shapes, and frame processing.  
- **Mediapipe** – For robust and accurate hand tracking and landmark detection.  
- **NumPy** – For numerical operations like interpolation.  
- **PyAutoGUI** – For simulating mouse and keyboard actions.  
- **Math & Time** – For distance calculation, timing, and performance tracking.  

## Project Structure
- **AiVirtualMouseProject.py**  
  Main driver script that captures video input, detects hand landmarks, interprets gestures, and controls mouse functions.  

- **HandTrackingModule.py**  
  Custom module built on top of Mediapipe for hand detection, landmark position extraction, finger status detection, and distance measurement.  

## How It Works
1. **Video Capture**  
   - Webcam captures real-time video frames using OpenCV.  

2. **Hand Detection**  
   - Mediapipe identifies hand landmarks (like index fingertip, thumb, middle fingertip).  
   - The `HandTrackingModule` processes and returns the coordinates.  

3. **Gesture Recognition**  
   - **Index Finger Up** → Move cursor.  
   - **Index + Middle Fingers Close** → Mouse click.  
   - **Index + Middle Fingers Up** → Scroll.  
   - **Fist (all fingers down)** → Minimize windows (optional).  

4. **Coordinate Mapping**  
   - Finger positions are mapped from camera frame to screen resolution.  
   - Uses interpolation and smoothing to reduce jitter.  

5. **Mouse Control**  
   - PyAutoGUI executes mouse movement, clicking, and scrolling.  

## Example Run
```
Running Virtual Mouse Project...
- Raise index finger → Move cursor
- Pinch index + middle finger → Click
- Raise index + middle finger → Scroll
Press 'q' to exit.
```

## What I Learned
- **Computer Vision Basics**: Using OpenCV for real-time frame processing.  
- **Gesture Recognition**: Leveraging Mediapipe for hand tracking and gesture detection.  
- **Human-Computer Interaction**: Designing touch-free interfaces.  
- **Mouse Automation**: Using PyAutoGUI to simulate hardware controls.  
- **Code Modularity**: Separating core logic into reusable modules (`HandTrackingModule`).  
- **Error Handling**: Gracefully handling cases like missing camera input.  

## Future Enhancements
- Add **multi-hand support** for advanced gestures.  
- Introduce **drag-and-drop functionality** (thumb + index pinch hold).  
- Implement **custom gesture shortcuts** (e.g., 3 fingers for volume control).  
- Build a **GUI overlay** for real-time gesture hints.  
- Optimize for **low-light performance**.  
