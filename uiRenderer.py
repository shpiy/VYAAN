'''
User interface rendering module.
Handles drawing UI elements on video frames.
'''
import cv2
import numpy
from typing import List, Dict, Any

from config import DisplaySettings



class UIRenderer:
    '''Handles rendering of UI elements on video frames.'''

    def __init__(self, displaySettings: DisplaySettings, frameWidth: int = 640, frameHeight: int = 480):
        '''
        Initialize UI renderer.

        Args:
            displaySettings: Display configuration
            frameWidth: Frame width for coordinate conversion
            frameHeight: Frame height for coordinate conversion
        '''
        self.settings = displaySettings
        self.frameWidth = frameWidth
        self.frameHeight = frameHeight

    def drawInfoBox(self, frame: numpy.ndarray, stats: Dict[str, Any]) -> None:
        '''
        Draw information box with exercise stats.

        Args:
            frame: Frame to draw on
            stats: Exercise statistics
        '''
        cv2.rectangle(frame, (0, 0), (280, 120), self.settings.infoBoxColor, -1280)

        cv2.putText(frame, stats['exerciseName'].upper(), (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.settings.textColorDark, 2)
        cv2.putText(frame, 'REPS', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.settings.textColorDark, 1)
        cv2.putText(frame, str(stats['counter']), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.4, self.settings.textColorDark, 2)
        cv2.putText(frame, 'STAGE', (120, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.settings.textColorDark, 1)
        cv2.putText(frame, stats['stage'], (120, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.9, self.settings.textColor, 2)

        cv2.putText(frame, f'ANGLE: {int(stats['currentAngle'])}deg', (10, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.settings.textColorDark, 1)

    def drawAngleAtJoint(self, frame: numpy.ndarray, angle: float, jointPosition: List[float]) -> None:
        '''
        Draw angle value at joint position.

        Args:
            frame: Frame to draw on
            angle: Angle value
            jointPosition: Joint position [x, y] in normalized coordinates
        '''
        # Convert normalized coordinates to pixel coordinates
        pixelPos = tuple(numpy.multiply(jointPosition, [self.frameWidth, self.frameHeight]).astype(int))

        cv2.putText(frame, f'{int(angle)}deg', pixelPos, cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.settings.textColor, 2) # Draw angle text
        cv2.circle(frame, pixelPos, 5, self.settings.landmarkColor, -1) # Draw small circle at joint

    def drawInstructions(self, frame: numpy.ndarray) -> None:
        '''
        Draw instruction text.

        Args:
            frame: Frame to draw on
        '''
        instructions = ['Press \'q\' to quit', 'Press \'r\' to reset counter']

        yStart = self.frameHeight - 60
        for i, instruction in enumerate(instructions):
            cv2.putText(frame, instruction, (10, yStart + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.settings.textColor, 1)

    def drawThresholds(self, frame: numpy.ndarray, stats: Dict[str, Any]) -> None:
        '''
        Draw threshold indicators.

        Args:
            frame: Frame to draw on
            stats: Exercise statistics
        '''
        xStart = self.frameHeight - 200
        cv2.putText(frame, f'Extended: {int(stats['extendedThreshold'])}deg', (xStart, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.settings.textColor, 1)
        cv2.putText(frame, f'Flexed: {int(stats['flexedThreshold'])}deg', (xStart, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.settings.textColor, 1)