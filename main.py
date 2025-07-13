import cv2
from typing import Optional, Any

from config import ExerciseType, ExerciseConfigs, CameraConfig, DisplaySettings
from util import AngleCalculator
from poseDetector import PoseDetector
from exerciseTracker import ExerciseTracker
from uiRenderer import UIRenderer



class ExerciseApp:
    def __init__(self, exerciseType: ExerciseType):
        self.exerciseType = exerciseType
        self.exerciseConfig = ExerciseConfigs.CONFIGS[exerciseType]
        self.cameraConfig = CameraConfig()
        self.displaySettings = DisplaySettings()

        self.poseDetector = PoseDetector(self.cameraConfig)
        self.exerciseTracker = ExerciseTracker(self.exerciseConfig)
        self.uiRenderer = UIRenderer(self.displaySettings, self.cameraConfig.width, self.cameraConfig.height)

        self.videoCapture: Optional[cv2.VideoCapture] = None
        self.running = True

        print(f'Initialized {self.exerciseConfig.name} application')

    def setupCamera(self) -> bool:
        try:
            self.videoCapture = cv2.VideoCapture(self.cameraConfig.index)
            if not self.videoCapture.isOpened():
                print(f'Failed to open camera {self.cameraConfig.index}')
                return False

            self.videoCapture.set(cv2.CAP_PROP_FRAME_WIDTH, self.cameraConfig.width)
            self.videoCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cameraConfig.height)

            print('Camera setup successful')
            return True
        except Exception as err:
            print(f'Camera setup failed: {err}')
            return False
        
    def processFrame(self, frame) -> Optional[Any]:
        try:
            poseResults = self.poseDetector.detectPose(frame)
            if not poseResults or not poseResults.pose_landmarks:
                return frame
            
            landMarkPositions = self.poseDetector.extractLandmarks(poseResults.pose_landmarks.landmark, self.exerciseConfig)

            if landMarkPositions:
                pointA, pointB, pointC = landMarkPositions
                angle = AngleCalculator.calculateAngle(pointA=pointA, pointB=pointB, pointC=pointC)

                self.exerciseTracker.updateState(angle=angle)
                self.uiRenderer.drawAngleAtJoint(frame, angle, pointB)

            self.poseDetector.drawLandmarks(frame, poseResults, self.displaySettings.landmarkColor, self.displaySettings.connectionColor)

            stats = self.exerciseTracker.getStats()
            self.uiRenderer.drawInfoBox(frame, stats)
            self.uiRenderer.drawInstructions(frame)
            self.uiRenderer.drawThresholds(frame, stats)

            return frame
        except Exception as err:
            print(f'Frame processing error: {err}')
            return frame
        
    def handleKeyPress(self, key: int) -> bool:
        if key == ord('q'):
            print('Quit requested')
            return False
        elif key == ord('r'):
            self.exerciseTracker.resetCounter()
        elif key == ord('s'):
            stats = self.exerciseTracker.getStats()
            print(f'Current stats: {stats}')

        return True

    def run(self) -> None:
        if not self.setupCamera():
            return
        
        self.running = True
        print(f'Starting {self.exerciseConfig.name} tracking')
        print(f'Controls: \'q\' to quit, \'r\' to reset, \'s\' to show stats')

        try:
            while self.running and self.videoCapture.isOpened():
                returnVar, frame = self.videoCapture.read()
                if not returnVar:
                    print('Failed to read frame')
                    break

                processedFrame = self.processFrame(frame)
                if processedFrame is not None:
                    cv2.imshow(f'{self.exerciseConfig.name} Tracker', processedFrame) 

                key = cv2.waitKey(1) & 0xFF
                if not self.handleKeyPress(key):
                    break
        except KeyboardInterrupt:
            print('Interrupted by user')
        finally:
            self.cleanup()

    def cleanup(self) -> None:
        self.running = False

        if self.videoCapture:
            self.videoCapture.release()

        cv2.destroyAllWindows()
        self.poseDetector.cleanup()

        print('Cleanup completed')


def main():
    exerciseType = ExerciseType.KNEE_FLEXION

    try:
        App = ExerciseApp(exerciseType=exerciseType)
        App.run()
    except Exception as err:
        print(f'Application error: {err}')
        return 1

    return 0


if __name__ == '__main__':
    exit(main())