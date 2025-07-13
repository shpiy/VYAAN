import cv2
import mediapipe
import numpy
from typing import List, Optional, Tuple, Any

from config import ExerciseConfig, CameraConfig



class PoseDetector:
    def __init__(self, cameraConfig: CameraConfig):
        self.cameraConfig = cameraConfig
        self.mpDrawing = mediapipe.solutions.drawing_utils
        self.mpPose = mediapipe.solutions.pose

        self.pose = self.mpPose.Pose(min_detection_confidence=cameraConfig.minDetectionConfidence, min_tracking_confidence=cameraConfig.minTrackingConfidence)

    def detectPose(self, frame: numpy.ndarray) -> Optional[Any]:
        try:
            rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgbFrame.flags.writeable = False

            results = self.pose.process(rgbFrame)
            return results
        except Exception as err:
            print(f'Pose detection error: {err}')
            return None

    def extractLandmarks(self, landMarks, exerciseConfig: ExerciseConfig) -> Optional[Tuple[List[float], List[float], List[float]]]:
        try:
            side = exerciseConfig.side
            landMarkNames = exerciseConfig.landMarks

            positions = []
            for landMarkName in landMarkNames:
                fullLandmarkName = f'{side}_{landMarkName}'
                landMarkEnum = getattr(self.mpPose.PoseLandmark, fullLandmarkName)
                landMark = landMarks[landMarkEnum.value]
                positions.append([landMark.x, landMark.y])

            return tuple(positions)
        except (AttributeError, IndexError) as err:
            print(f'Failed to extract landmarks: {err}')
            return None
    
    def drawLandmarks(self, frame: numpy.ndarray, poseResults, landMarkColor: tuple, connectionColor: tuple) -> None:
        if poseResults.pose_landmarks:
            self.mpDrawing.draw_landmarks(
                frame,
                poseResults.pose_landmarks,
                self.mpPose.POSE_CONNECTIONS,
                self.mpDrawing.DrawingSpec(
                    color=landMarkColor,
                    thickness=2,
                    circle_radius=2
                ),
                self.mpDrawing.DrawingSpec(
                    color=connectionColor,
                    thickness=2,
                    circle_radius=2
                )
            )

    def cleanup(self) -> None:
        if hasattr(self, 'pose'):
            self.pose.close()
