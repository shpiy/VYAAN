from dataclasses import dataclass
from enum import Enum
from typing import List



class ExerciseType(Enum):
    KNEE_FLEXION = 'kneeFlexion'

@dataclass
class ExerciseConfig:
    name: str
    landMarks: List[str]
    extendedThreshold: float
    flexedThreshold: float
    side: str = 'RIGHT'

@dataclass
class CameraConfig:
    index: int = 0
    width: int = 640
    height: int = 480
    minDetectionConfidence: float = 0.5
    minTrackingConfidence: float = 0.5

@dataclass
class DisplaySettings:
    infoBoxColor: tuple = (245, 117, 16)
    textColor: tuple = (255, 255, 255)
    textColorDark: tuple = (0, 0, 0)
    landmarkColor: tuple = (245, 117, 66)
    connectionColor: tuple = (245, 66, 230)
    fontScale: float = 0.6
    fontThickness: int = 2

class ExerciseConfigs:

    CONFIGS = {
        ExerciseType.KNEE_FLEXION: ExerciseConfig(
            name='Knee Flexion',
            landMarks=['HIP', 'KNEE', 'ANKLE'],
            extendedThreshold=170.0,
            flexedThreshold=108.0,
            side='RIGHT'
        )
    }