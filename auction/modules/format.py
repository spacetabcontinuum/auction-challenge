class PrintLog:
    def error(message):
        return print('\x1b[97m' + '\x1b[41m' + 'ERROR: ' + message + '\x1b[0m')
    def warning(message):
        return print('\x1b[97m' + '\x1b[43m' + 'WARNING: ' + message + '\x1b[0m')
    def message(message):
        return print('\x1b[37m' + 'DEBUG MESSAGE: ' + message + '\x1b[0m')
    def announcement(message):
        return print('\x1b[30m' + '\x1b[102m' + 'Announcement: ' + message + '\x1b[0m')
