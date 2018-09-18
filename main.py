from commander import Commander
from string_cfg import MAIN
import sys

__author__ = "Mikhail Gorobets"
__version__ = '0.1'


if __name__ == '__main__':
    if sys.argv[1]:
        commander = Commander(sys.argv[1])
        commander.loop()
    else:
        print(MAIN.ERROR_INPUT_PARAM)
