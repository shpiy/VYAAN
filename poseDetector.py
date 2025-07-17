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
            positions = []
            for landMarkName in exerciseConfig.landMarks:
                # Handle bilateral tracking
                if exerciseConfig.side == 'BOTH':
                    # Use average of both sides
                    leftLandmark = getattr(self.mpPose.PoseLandmark, f'LEFT_{landMarkName}')
                    rightLandmark = getattr(self.mpPose.PoseLandmark, f'RIGHT_{landMarkName}')

                    x = (landMarks[leftLandmark.value].x + landMarks[rightLandmark.value].x) / 2
                    y = (landMarks[leftLandmark.value].y + landMarks[rightLandmark.value].y) / 2
                    positions.append([x, y])
                else:
                    # Single side tracking
                    fullLandmarkName = f'{exerciseConfig.side}_{landMarkName}'
                    landMark = landMarks[getattr(self.mpPose.PoseLandmark, fullLandmarkName).value]
                    positions.append([landMark.x, landMark.y])

            return tuple(positions)
        except (AttributeError, IndexError) as err:
            logger.warning(f'Failed to extract landmarks: {err}. Using fallback method')
            
            # Fallback to simple averaging if specific landmarks missing
            return self.getFallbackLandmarks(landMarks, exerciseConfig)
    
    def getFallbackLandmarks(self, landmarks, config: ExerciseConfig):
        '''
        Fallback landmark detection using body proportions when standard landmarks are obscured.

        Args:
            landmarks: MediaPipe pose landmarks
            config: Exercise configuration

        Returns:
            Tuple of estimated landmark positions or None if fallback fails
        '''
        try:
            # Get visible landmarks for body proportions calculations
            nose = landmarks[self.mpPose.PoseLandmark.NOSE.value]

            leftHip = landmarks[self.mpPose.PoseLandmark.LEFT_HIP.value]
            rightHip = landmarks[self.mpPose.PoseLandmark.RIGHT_HIP.value]

            leftAnkle = landmarks[self.mpPose.PoseLandmark.LEFT_ANKLE.value]
            rightAnkle = landmarks[self.mpPose.PoseLandmark.RIGHT_ANKLE.value]

            # Calculate body proportions
            hipCenterX = (leftHip.x + rightHip.x) / 2
            hipCenterY = (leftHip.y + rightHip.y) / 2

            # Estimate knee positions based on body proportions
            if 'KNEE' in config.landMarks:
                if config.side == 'LEFT':
                    hip = leftHip
                    ankle = leftAnkle
                elif config.side == 'RIGHT':
                    hip = rightHip
                    ankle = rightAnkle
                else:
                    hip = [hipCenterX, hipCenterY]
                    ankle = [(leftAnkle.x + rightAnkle.x) / 2, (leftAnkle.y + rightAnkle.y) / 2]

                kneeX = (hip.x + ankle.x) / 2
                kneeY = (hip.y + ankle.y) / 2

                # Adjust for squat - knees move forward
                if config.name == 'Partial Squat':
                    forwardOffset = 0.15 * abs(hip.y - ankle.y)
                    kneeX += forwardOffset

            # Estimaate hip position
            if 'HIP' in config.landMarks:
                hipX = hipCenterX
                hipY = hipCenterY

                # Adjust based on exercise type
                if config.name == 'Partial Squat':
                    hipY += 0.05 * abs(nose.y - hipCenterY)

            # Estimate ankle positions
            if 'ANKLE' in config.landMarks:
                if config.side == 'LEFT':
                    ankleX = leftAnkle.x
                    ankleY = leftAnkle.y
                elif config.landMarks == 'RIGHT':
                    ankleX = rightAnkle.x
                    ankleY = rightAnkle.y
                else:
                    ankleX = (leftAnkle.x + rightAnkle.x) / 2
                    ankleY = (leftAnkle.y + rightAnkle.y) / 2

            # Build positions list based on required landmarks
            positions = []
            for landmark in config.landMarks:
                if landmark == 'HIP':
                    positions.append([hipX, hipY])
                elif landmark == 'KNEE':
                    positions.append([kneeX, kneeY])
                elif landmark == 'ANKLE':
                    positions.append([ankleX, ankleY])
            
            logger.info(f'Using fallback landmarks for {config.name}')
            return tuple(positions)
        except (AttributeError, IndexError) as err:
            logger.info(f'Fallback landmark estimation failed: {err}')
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
