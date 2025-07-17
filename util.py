'''
Utility functions for exercise tracking system.
Contains angle calculations and other helper functions.
'''

import numpy
from typing import List



class AngleCalculator:
    '''Utility class for angle calculations.'''

    @staticmethod
    def calculateAngle(pointA: List[float], pointB: List[float], pointC: List[float]) -> float:
        '''
        Calculate angle between three points.

        Args:
            pointA: First point coordinated [x, y]
            pointB: Vertex point coordinated [x, y]
            pointC: Third point coordinated [x, y]

        Returns:
            Angle in degrees
        '''
        try:
            startPoint = numpy.array(pointA)
            midPoint = numpy.array(pointB)
            endPoint = numpy.array(pointC)

            radians = numpy.arctan2(endPoint[1] - midPoint[1], endPoint[0] - midPoint[0]) - numpy.arctan2(startPoint[1] - midPoint[1], startPoint[0] - midPoint[0])
            angle = numpy.abs(radians * 180.0 / numpy.pi)

            if angle > 180.0:
                angle = 360.0 - angle

            return angle
        except Exception as err:
            print(f'Error calculating angle: {err}')
            return 0.0

    @staticmethod
    def smoothAngles(angleHistory: List[float], newAngle: float, maxHistory: int = 10) -> float:
        '''
        Apply smoothing to angle measurements.
        
        Args:
            angleHistory; History of angle measurements
            newAngle: New angle measurement
            maxHistory: Maximum number of angles to keep in history

        Returns:
            Smoothed angle
        '''
        angleHistory.append(newAngle)
        if len(angleHistory) > maxHistory:
            angleHistory.pop(0)

        return float(numpy.mean(angleHistory))


class ValidateUtils:
    '''Utility class for validation functions.'''

    @staticmethod
    def validateLandmarks(landMarks, requiredLandmarks: List[str]) -> bool:
        '''
        Validate that required landmarks are present

        Args:
            landMarks: MediaPipe pose landmarks
            requiredLandmarks: List of required landmark name

        Returns:
            True if all landmarks are present and valid
        '''
        if not landMarks:
            return False
        
        try:
            for landMarkName in requiredLandmarks:
                # Check if landmark exists and has valid coordinates
                if not hasattr(landMarkName, landMarkName.lower()):
                    return False
                
            return True
        except Exception as err:
            print(f'Landmark validation error: {err}')
            return False