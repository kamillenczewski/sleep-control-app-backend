from pathlib import Path
from os.path import join


USERS_TABLE = 'users'
SLEEPING = 'sleeping'
USER_OPTIONS_TABLE = 'user_options'
DEFAULT_OPTIONS_TABLE = 'default_options'


DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

SLEEPTIME_DATE = 'sleeptime'
WAKEUP_DATE = 'wakeup'

MAIN_PATH = Path(__file__).parent.resolve()
LOG_PATH = 'log.txt'
SECRET_PATH = join(Path(__file__).parent.parent.resolve(), 'secret.env')