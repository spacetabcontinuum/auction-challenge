import sys

class LogSettings:
    def __init__(self):
        self.DEBUG = False
    def debug_enabled(self):
        if '--debug' in sys.argv:
            self.DEBUG = True
    def error(self,message):
        return print('\x1b[97m' + '\x1b[41m' + 'ERROR: ' + message + '\x1b[0m')
    def warning(self,message):
        if self.DEBUG:
            return print('\x1b[97m' + '\x1b[43m' + 'WARNING: ' + message + '\x1b[0m')
    def message(self,message):
        if self.DEBUG:
            return print('\x1b[37m' + 'DEBUG MESSAGE: ' + message + '\x1b[0m')
    def announcement(self,message):
        return print('\x1b[30m' + '\x1b[102m' + 'Announcement: ' + message + '\x1b[0m')
