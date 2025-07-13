# VYAAN
___

## Requirements

- Python 3.7 or higher
- Webcam or camera device
- Operating System: Windows, macOS, Linux

## Installation

### 1. Clone the repository

```bash
git clone git@github.com:shpiy/VYAAN
cd VYAAN
```

### 2. Create Virtual Environment

#### Windows

```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

#### macOS/Linux

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 3. Install Dependencies

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

Test that the dependencies are correctly installed:

```bash
python -c "import cv2, mediapipe, numpy; print('All dependencies installed successfully!')"
```

## Running the application

### Start the Exercise Tracker

With the virtual environment activated:

#### Windows

```cmd
python main.py
```

#### macOS/Linux

```bash
python3 main.py
```

### Controls

Once the application is running:
- **`q`** - Quit the application
- **`r`** - Reset the rep counter
- **`s`** - Show current statistics in console

### Camera Setup

The application will automatically attempt to connect to default camera (index 0). If multiple cameras are present, or need to use a different camera, modify the `index` value in the `CameraConfig` class in `config.py`.

## Usage Instructions

1. **Position yourself** so your right leg is visible to the camera
2. **Stand with your leg extended** ()

## Configuration

### Exercise Settings

Modify `config.py` to adjust exercise parameters:

```python
KNEE_FLEXION: ExerciseConfig(
    name='Knee Flexion',
    landMarks=['HIP', 'KNEE', 'ANKLE'],
    extendedThreshold=172.0, # Angle for extended position
    flexedThreshold=108.0, # Angle for flexed position
    side='RIGHT'
)
```

### Camera Settings
Adjust camera parameters in `config.py`:

```python
CameraConfig(
    index=0,                    # Camera index (0 for default)
    width=640,                  # Frame width
    height=480,                 # Frame height
    minDetectionConfidence=0.5, # Pose detection confidence
    minTrackingConfidence=0.5   # Pose tracking confidence
)
```

## Troubleshooting

### Common Issues

#### Camera Not Found

```
Failed to open camera 0
```
**Solution:** Check if camera is connected and not being used by another application. Try changing the camera index in `config.py`.

#### Import Errors
```
ModuleNotFoundError: No module named 'cv2'
```
**Solution:** Ensure the virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

#### Poor Detection Performance
**Solution:**
- Ensure good lighting conditions
- Position yourself at appropriate distance from camera
- Adjust `minDetectionConfidence` and `minTrackingConfidence` in `config.py`

#### Permission Errors (macOS)
**Solution:** Grant camera permissions to Terminal or IDE in System Prefrences > Security & Privacy > Privacy > Camera.

### Platform-Specific Issues

#### Windows
- If you encounter DLL errors, try installing Microsoft Visual C++ Redistribulate
- For permission issues, run command prompt as Administrator

#### macOS
- Intall Xcode command line tools: `xcode-select --install`
- If using Apple Silicon Mac, ensure you're using compatible Python version

#### Linux
- Instal required system packages:
```bash
sudo apt update
sudo apt install python3-pip python3-venv
sudo apt install libgl1-mesa-glx libglib2.0-0
```

## Development

### Project Structure

```
VYAAN/
├── main.py              # Main application entry point
├── config.py            # Configuration settings
├── exerciseTracker.py   # Exercise tracking logic
├── poseDetector.py      # Pose detection using MediaPipe
├── uiRenderer.py        # UI rendering and overlays
├── util.py              # Utility functions
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Adding New Exercises

1. Add new exercise type to `ExerciseType` enum in `config.py`
2. Create configuration in `ExerciseConfigs.CONFIGS`
3. Update the exercise type in `main.py`

### Virtual Environment Management

#### Deactivate Virtual Environment
```bash
deactivate
```

#### Remove Virtual Environment
```bash
# Windows
rmdir /s venv

# macOS/Linux
rm -rf venv
```

## License
___

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.