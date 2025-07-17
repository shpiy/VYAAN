'''
Pose detection module using MediaPipe.
Handles pose estimation and landmark extraction.
'''

import cv2
import mediapipe
import numpy
import logging
from typing import List, Optional, Tuple, Any

from config import ExerciseConfig, CameraConfig



logger = logging.getLogger(__name__)

class PoseDetector:
    '''Handles poses detection and landmark extraction.'''
    def __init__(self, cameraConfig: CameraConfig):
        '''
        Initialize pose detector.

        Args:
            cameraConfig: Camera configuration
        '''
        self.cameraConfig = cameraConfig
        self.mpDrawing = mediapipe.solutions.drawing_utils
        self.mpPose = mediapipe.solutions.pose

        self.pose = self.mpPose.Pose(min_detection_confidence=cameraConfig.minDetectionConfidence, min_tracking_confidence=cameraConfig.minTrackingConfidence)

    def detectPose(self, frame: numpy.ndarray) -> Optional[Any]:
        '''
        Detect pose in frame.

        Args:
            frame: Input frame

        Returns:
            MediaPipe pose results or None
        '''
        try:
            # Convert color space
            rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgbFrame.flags.writeable = False

            # Process pose
            results = self.pose.process(rgbFrame)
            return results
        except Exception as err:
            logger.error(f'Pose detection error: {err}')
            return None

    def extractLandmarks(self, landMarks, exerciseConfig: ExerciseConfig) -> Optional[Tuple[List[float], List[float], List[float]]]:
        '''
        Extract landmark positions based on exercise configuration.

        Args:
            landMarks: MediaPipe pose landmarks
        
        Returns:
            Tuple of three landmark positions or None if extraction fails
        '''
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
            logger.warning(f'Failed to extract landmarks: {err}')
            return None
    
    def drawLandmarks(self, frame: numpy.ndarray, poseResults, landMarkColor: tuple, connectionColor: tuple) -> None:
        '''
        Draw pose landmarks on frame.
        
        Args:
            frame: Frame to draw on
            poseResults: MediaPipe pose results
            landMarkColor: Color for landmarks
            connectionColor: Color for connections
        '''
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
        '''Clean up pose detector resources'''
        if hasattr(self, 'pose'):
            self.pose.close()
