import numpy
from typing import List



class AngleCalculator:
    @staticmethod
    def calculateAngle(pointA: List[float], pointB: List[float], pointC: List[float]) -> float:
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
        angleHistory.append(newAngle)
        if len(angleHistory) > maxHistory:
            angleHistory.pop(0)

        return float(numpy.mean(angleHistory))


class ValidateUtils:
    @staticmethod
    def validateLandmarks(landMarks, requiredLandmarks: List[str]) -> bool:
        if not landMarks:
            return False
        
        try:
            for landMarkName in requiredLandmarks:
                if not hasattr(landMarkName, landMarkName.lower()):
                    return False
                
            return True
        except Exception as err:
            print(f'Landmark validation error: {err}')
            return False