from typing import Dict, Any, List
from dataclasses import dataclass

from config import ExerciseConfig 
from util import AngleCalculator



@dataclass
class ExerciseState:
    counter: int = 0
    stage: str = None
    angleHistory: List[float] = None
    currentAngle: float = 0.0

    def __post_init__(self):
        if self.angleHistory is None:
            self.angleHistory = []


class ExerciseTracker:
    def __init__(self, exerciseConfig: ExerciseConfig):
        self.config = exerciseConfig
        self.state = ExerciseState()
        self.maxHistoryLength = 10

        print(f'Initialized tracker for {self.config.name}')
    
    def updateState(self, angle: float) -> bool:
        smoothedAngle = AngleCalculator.smoothAngles(self.state.angleHistory, angle, self.maxHistoryLength)

        self.state.currentAngle = smoothedAngle
        previousCounter = self.state.counter

        if smoothedAngle > self.config.extendedThreshold:
            self.state.stage = 'extended'
        elif smoothedAngle < self.config.flexedThreshold and self.state.stage == 'extended':
            self.state.stage = 'flexed'
            self.state.counter += 1

            print(f'{self.config.name} Rep: {self.state.counter}')

        return self.state.counter > previousCounter

    def resetCounter(self) -> None:
        self.state.counter = 0
        self.state.stage =  None
        self.state.angleHistory = []

        print(f'{self.config.name} counter reset')

    def getStats(self) -> Dict[str, Any]:
        return {
            'exerciseName': self.config.name,
            'counter': self.state.counter,
            'stage': self.state.stage or 'READY',
            'currentAngle': self.state.currentAngle,
            'averageAngle': sum(self.state.angleHistory) / len(self.state.angleHistory) if self.state.angleHistory else 0.0,
            'extendedThreshold': self.config.extendedThreshold,
            'flexedThreshold': self.config.flexedThreshold
        }

    def getDisplayStage(self) -> str:
        return self.state.stage.upper() if self.state.stage else 'READY'