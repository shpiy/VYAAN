'''
Main application module.
Coordinates all components and handles the main application loop.
'''
import cv2
import logging
from typing import Optional, Any

from config import ExerciseType, ExerciseConfigs, CameraConfig, DisplaySettings
from util import AngleCalculator
from poseDetector import PoseDetector
from exerciseTracker import ExerciseTracker
from uiRenderer import UIRenderer



# COnfigure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ExerciseApp:
    '''Main application class that coordinates all components.'''

    def __init__(self, exerciseType: ExerciseType):
        '''
        Initialize the exercise application.

        Args:
            exerciseType: Type of exercise to track
        '''
        self.exerciseType = exerciseType
        self.exerciseConfig = ExerciseConfigs.CONFIGS[exerciseType]
        self.cameraConfig = CameraConfig()
        self.displaySettings = DisplaySettings()

        # Initialize components
        self.poseDetector = PoseDetector(self.cameraConfig)
        self.exerciseTracker = ExerciseTracker(self.exerciseConfig)
        self.uiRenderer = UIRenderer(self.displaySettings, self.cameraConfig.width, self.cameraConfig.height)

        # Video capture
        self.videoCapture: Optional[cv2.VideoCapture] = None
        self.running = True

        logger.info(f'Initialized {self.exerciseConfig.name} application')

    def setupCamera(self) -> bool:
        '''
        Setup camera capture.

        Returns:
            True if camera setup successful
        '''
        try:
            self.videoCapture = cv2.VideoCapture(self.cameraConfig.index)
            if not self.videoCapture.isOpened():
                logger.error(f'Failed to open camera {self.cameraConfig.index}')
                return False

            # Set camera properties
            self.videoCapture.set(cv2.CAP_PROP_FRAME_WIDTH, self.cameraConfig.width)
            self.videoCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cameraConfig.height)

            logger.info('Camera setup successful')
            return True
        except Exception as err:
            logger.error(f'Camera setup failed: {err}')
            return False
        
    def processFrame(self, frame) -> Optional[Any]:
        '''
        Process a single frame.

        Args:
            frame: Input frame

        Returns:
            Processed frame or None if processing failed
        '''
        try:
            # Detect pose
            poseResults = self.poseDetector.detectPose(frame)
            if not poseResults or not poseResults.pose_landmarks:
                return frame
            
            # Extract landmarks
            landMarkPositions = self.poseDetector.extractLandmarks(poseResults.pose_landmarks.landmark, self.exerciseConfig)

            if landMarkPositions:
                pointA, pointB, pointC = landMarkPositions
                angle = AngleCalculator.calculateAngle(pointA=pointA, pointB=pointB, pointC=pointC) # Calculate angle

                self.exerciseTracker.updateState(angle=angle) # Update exercise state
                self.uiRenderer.drawAngleAtJoint(frame, angle, pointB) # Draw angle at joint

            # Draw pose landmarks
            self.poseDetector.drawLandmarks(frame, poseResults, self.displaySettings.landmarkColor, self.displaySettings.connectionColor)

            # Draw UI
            stats = self.exerciseTracker.getStats()
            self.uiRenderer.drawInfoBox(frame, stats)
            self.uiRenderer.drawInstructions(frame)
            self.uiRenderer.drawThresholds(frame, stats)

            return frame
        except Exception as err:
            logger.error(f'Frame processing error: {err}')
            return frame
        
    def handleKeyPress(self, key: int) -> bool:
        '''
        Handle keyboard input.

        Args;
            key: Key code

        Returns:
            True to continue, False to exit
        '''
        if key == ord('q'):
            logger.info('Quit requested')
            return False
        elif key == ord('r'):
            self.exerciseTracker.resetCounter()
        elif key == ord('s'):
            # Save current stats
            stats = self.exerciseTracker.getStats()
            logger.info(f'Current stats: {stats}')

        return True

    def run(self) -> None:
        '''Run the main application loop.'''
        if not self.setupCamera():
            return
        
        self.running = True
        logger.info(f'Starting {self.exerciseConfig.name} tracking')
        logger.info('Controls: \'q\' to quit, \'r\' to reset, \'s\' to show stats')

        try:
            while self.running and self.videoCapture.isOpened():
                returnVar, frame = self.videoCapture.read()
                if not returnVar:
                    logger.error('Failed to read frame')
                    break

                # Process frame
                processedFrame = self.processFrame(frame)
                if processedFrame is not None:
                    cv2.imshow(f'{self.exerciseConfig.name} Tracker', processedFrame) # Display frame

                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if not self.handleKeyPress(key):
                    break
        except KeyboardInterrupt:
            logger.info('Interrupted by user')
        finally:
            self.cleanup()

    def cleanup(self) -> None:
        # Clean up resources.
        self.running = False

        if self.videoCapture:
            self.videoCapture.release()

        cv2.destroyAllWindows()
        self.poseDetector.cleanup()

        logger.info('Cleanup completed')


def main():
    '''Main function.'''
    exerciseType = ExerciseType.KNEE_FLEXION

    try:
        App = ExerciseApp(exerciseType=exerciseType)
        App.run()
    except Exception as err:
        logger.error(f'Application error: {err}')
        return 1

    return 0


if __name__ == '__main__':
    exit(main())