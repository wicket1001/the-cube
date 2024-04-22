from enum import Enum, IntFlag


class DebugLevel(IntFlag):
    EMERGENCY = 0
    ALERT = 1
    CRITICAL = 2
    ERROR = 3
    WARNING = 4
    NOTIFICATION = 5
    INFORMATIONAL = 6
    DEBUGGING = 7
