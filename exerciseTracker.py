'''
Exercise tracking logic and state management.
Handles exercise counting, state transitions, and statistics.
'''
import logging
from typing import Dict, Any, List
from dataclasses import dataclass

from config import ExerciseConfig 
from util import AngleCalculator



logger = logging.getLogger(__name_)

@dataclass
class ExerciseState:
    '''Represents the current state of exercise tracking.'''
    counter: int = 0
    stage: str = None
    angleHistory: List[float] = None
    currentAngle: float = 0.0

    def __post_init__(self):
        if self.angleHistory is None:
            self.angleHistory = []


class ExerciseTracker:
    '''Handles exercise counting logic and state management.'''

    def __init__(self, exerciseConfig: ExerciseConfig):
        '''
        Initialize exercise tracker.

        Args:
            exerciseConfig: Configuration for the exercise
        '''
        self.config = exerciseConfig
        self.state = ExerciseState()
        self.maxHistoryLength = 10

        logger.info(f'Initialized tracker for {self.config.name}')
    
    def updateState(self, angle: float) -> bool:
        '''
        Update exercise state based on angle and thresholds.

        Args:
            angle: Current joint angle
        
        Returns:
            True if a new repetition was completed
        '''
        # Smooth the angle
        smoothedAngle = AngleCalculator.smoothAngles(self.state.angleHistory, angle, self.maxHistoryLength)

        self.state.currentAngle = smoothedAngle
        previousCounter = self.state.counter

        # Update stage based on angle thresholds
        if smoothedAngle > self.config.extendedThreshold:
            self.state.stage = 'extended'
        elif smoothedAngle < self.config.flexedThreshold and self.state.stage == 'extended':
            self.state.stage = 'flexed'
            self.state.counter += 1

            logger.info(f'{self.config.name} Rep: {self.state.counter}')

        # Return True if a new rep was completed
        return self.state.counter > previousCounter

    def resetCounter(self) -> None:
        '''Reset exercise counter and state.'''
        self.state.counter = 0
        self.state.stage =  None
        self.state.angleHistory = []

        logger.info(f'{self.config.name} counter reset')

    def getStats(self) -> Dict[str, Any]:
        '''Get current exercise statistics.'''
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
        '''Get stage text for display.'''
        return self.state.stage.upper() if self.state.stage else 'READY'