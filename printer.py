import builtins
import time
import inspect

import os

log_file = open("logs" + os.path.sep + "log_" + time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime()) + ".txt", "w")


class DebugLevels:
    ALL = 999
    ERROR = -1
    DEFAULT = 0
    NETWORK = 1
    TIMER = 2
    INTERACTION = 3
    RESULT = 4
    ITERATION_COUNTER = 5
    PARAMETER = 6
    EVENT = 7
    INITIALIZATION = 8
    STATUS = 9
    FILE_EVENT = 10


active_debug_levels = {DebugLevels.ERROR, DebugLevels.RESULT, DebugLevels.TIMER, DebugLevels.DEFAULT}


def print(*args, label=None, color="", marker_color=None, debug_level=DebugLevels.DEFAULT, plain=False, **kwargs):
    if (debug_level not in active_debug_levels) and (DebugLevels.ALL not in active_debug_levels):
        return

    if plain:
        builtins.print(*args)
         
    prefix = '\x1b[0;'
    end_char = '\x1b[0m'

    print_string_clean = ""
    print_string = ""

    caller_name = inspect.getfile(inspect.stack()[1][0])
    caller_name = caller_name[caller_name.rfind("/") + 1:]

    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print_string_clean += "[" + current_time + "]"
    if marker_color:
        marker_color = ";" + str(marker_color + 10)
    else:
        marker_color = ""
    print_string += "\x1b[" + marker_color + "m" + "[" + current_time + "]" + "<" + caller_name + ">" + end_char

    if label:
        print_string_clean += "{" + label + "}"
        print_string += prefix + str(color) + "m" + "{" + label + "}" + end_char

    print_string_clean += " >> "
    print_string += " >> "
    text = (', '.join(map(str, args)))
    print_string_clean += text
    print_string += text

    builtins.print(print_string)
    log_file.write(print_string_clean + '\n')
    log_file.flush()


class print_colors:
    HEADER = 95
    WARNING = 93
    FAIL = 91

    BLACK = 30
    WHITE = 37

    BLUE = 34
    GREEN = 32
    PURPLE = 35
    RED = 31
    YELLOW = 33
    CYAN = 36

    GRAY = 38


class timer:
    timer_name = ""
    timer_start = 0
    sleep_start = 0
    color = print_colors.PURPLE

    def __init__(self, name="TIMER", color=print_colors.PURPLE):
        self.timer_name = name
        self.color = color

    def start(self):
        self.timer_start = time.time()
        print("Starting...", color=self.color, label=self.timer_name, debug_level=DebugLevels.TIMER)

    def pause(self):
        self.sleep_start = time.time()
        print("Pausing...", color=self.color, label=self.timer_name, debug_level=DebugLevels.TIMER)

    def resume(self):
        if self.sleep_start == 0 or self.timer_start == 0:
            return
        self.timer_start += time.time() - self.sleep_start
        self.sleep_start = 0
        print("Resuming...", color=self.color, label=self.timer_name, debug_level=DebugLevels.TIMER)

    def now(self):
        timer_result = time.time() - self.timer_start
        if self.sleep_start != 0:
            timer_result -= time.time() - self.sleep_start

        print(timer_result, color=self.color, label=self.timer_name, debug_level=DebugLevels.TIMER)

    def stop(self):
        if self.timer_start == 0:
            return
        timer_result = time.time() - self.timer_start

        self.timer_start = 0
        self.sleep_start = 0

        print("Stopping...", color=self.color, label=self.timer_name, debug_level=DebugLevels.TIMER)
        print(timer_result, color=self.color, label=self.timer_name, debug_level=DebugLevels.TIMER)