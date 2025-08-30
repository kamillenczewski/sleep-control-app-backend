from pathlib import Path
from os.path import join

DATES_TABLE = 'dates'
USERS_TABLE = 'users'
SLEEP_SATISFACTION_TABLE = 'sleep_satisfaction'
USER_OPTIONS_TABLE = 'user_options'
DEFAULT_OPTIONS_TABLE = 'default_options'


DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"

SLEEPTIME_DATE = 'sleeptime'
WAKEUP_DATE = 'wakeup'

MAIN_PATH = Path(__file__).parent.resolve()
LOG_PATH = 'log.txt'
SECRET_PATH = join(Path(__file__).parent.parent.resolve(), 'secret.env')