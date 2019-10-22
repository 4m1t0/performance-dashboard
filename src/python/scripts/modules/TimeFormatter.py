import logging
import sys


class TimeFormatter:
    TIME_STYLE = dict(
        YYYYMMDD_HHMMSS1='YYYYMMDD-HHMMSS'
    )

    def __init__(self, style):
        if style not in TimeFormatter.TIME_STYLE:
            logging.critical(
                'Invalid Usage: Please assign a style defined in'
                + 'TimeFormatter.TIME_STYLE.')
            sys.exit(1)
        if style == 'YYYYMMDD_HHMMSS1':
            self._style = TimeFormatter.TIME_STYLE[style]

    def format(self, s):
        if self._style == TimeFormatter.TIME_STYLE['YYYYMMDD_HHMMSS1']:
            tmp = s.split('-')
            _date, _time = tmp[0], tmp[1]
            year, month, day = int(_date[:4]), int(_date[4:6]), int(_date[6:])
            hour, minute, second = int(_time[:2]), int(
                _time[2:4]), int(_time[4:])
            return year, month, day, hour, minute, second
