import cv2
import numpy
from typing import List, Dict, Any

from config import DisplaySettings



class UIRenderer:
    def __init__(self, displaySettings: DisplaySettings, frameWidth: int = 640, frameHeight: int = 480):
        self.settings = displaySettings
        self.frameWidth = frameWidth
        self.frameHeight = frameHeight

    def drawInfoBox(self, frame: numpy.ndarray, stats: Dict[str, Any]) -> None:
        cv2.rectangle(frame, (0, 0), (280, 120), self.settings.infoBoxColor, -1280)

        cv2.putText(frame, stats['exerciseName'].upper(), (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.settings.textColorDark, 2)
        cv2.putText(frame, 'REPS', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.settings.textColorDark, 1)
        cv2.putText(frame, str(stats['counter']), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.4, self.settings.textColorDark, 2)
        cv2.putText(frame, 'STAGE', (120, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.settings.textColorDark, 1)
        cv2.putText(frame, stats['stage'], (120, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.9, self.settings.textColor, 2)

        cv2.putText(frame, f'ANGLE: {int(stats['currentAngle'])}deg', (10, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.settings.textColorDark, 1)

    def drawAngleAtJoint(self, frame: numpy.ndarray, angle: float, jointPosition: List[float]) -> None:
        pixelPos = tuple(numpy.multiply(jointPosition, [self.frameWidth, self.frameHeight]).astype(int))

        cv2.putText(frame, f'{int(angle)}deg', pixelPos, cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.settings.textColor, 2)
        cv2.circle(frame, pixelPos, 5, self.settings.landmarkColor, -1)

    def drawInstructions(self, frame: numpy.ndarray) -> None:
        instructions = ['Press \'q\' to quit', 'Press \'r\' to reset counter']

        yStart = self.frameHeight - 60
        for i, instruction in enumerate(instructions):
            cv2.putText(frame, instruction, (10, yStart + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.settings.textColor, 1)

    def drawThresholds(self, frame: numpy.ndarray, stats: Dict[str, Any]) -> None:
        xStart = self.frameHeight - 200
        cv2.putText(frame, f'Extended: {int(stats['extendedThreshold'])}deg', (xStart, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.settings.textColor, 1)
        cv2.putText(frame, f'Flexed: {int(stats['flexedThreshold'])}deg', (xStart, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.settings.textColor, 1)