from enum import Enum

class ExerciseGroup(str, Enum):
    PUSH = "Push"
    PULL = "Pull"
    QUADS = "Quads"
    HAMS = "Hams"
    FULL_BODY = "Full Body"
    UPPER = "Upper"
    LOWER = "Lower"
    CUSTOM = "Custom"