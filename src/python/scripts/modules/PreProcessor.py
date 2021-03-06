import datetime
import logging
import pandas as pd
import os
import sys
from .processors import LocustResourceProcessor


class PreProcessor:
    RESOURCES = ['LOCUST']

    def __init__(self, resource, time_formatter, *args, **kwargs):
        if resource not in PreProcessor.RESOURCES:
            logging.critical(
                'Invalid Usage: Please assign a resource defined in '
                + 'PreProcessor.RESOURCES.')
            sys.exit(1)
        if resource == 'LOCUST':
            if 'distribution_filename' in kwargs \
                    and 'requests_filename' in kwargs:
                self.resource_processor = LocustResourceProcessor. \
                    LocustResourceProcessor(
                        distribution_filename=kwargs['distribution_filename'],
                        requests_filename=kwargs['requests_filename'])
            elif 'distribution_filename' in kwargs:
                self.resource_processor = LocustResourceProcessor. \
                    LocustResourceProcessor(
                        distribution_filename=kwargs['distribution_filename'])
            elif 'requests_filename' in kwargs:
                self.resource_processor = LocustResourceProcessor. \
                    LocustResourceProcessor(
                        requests_filename=kwargs['requests_filename'])
            else:
                self.resource_processor = LocustResourceProcessor. \
                    LocustResourceProcessor()
        self.time_formatter = time_formatter

    def process(self, reports_path):
        """Performance Report as pandas DataFrame.

        Args:
            reports_dir: directory having directory \
                which includes locust reports.

        Returns:
            reports [pandas.DataFrame]: Having performance test reports and \
                following columns.
                    1.  Name: test target.
                    2.  # requests: number of requests.
                    3.  99%: 99%tile Latency. any %tile Latency is available \
                          because you have to assign key when plotting charts.
                    4.  Median response time: 50%tile Latency.
                    5.  Average response time: ditto.
                    6.  Min response time: ditto.
                    8.  Max response time: ditto.
                    4.  # failures: number of failures.
                    9.  Requests/s: requests per second.
                    10: DateTime [pandas.TimeStamp]: date executed test.
        """
        report_dirs = [f for f in os.listdir(reports_path) if os.path.isdir(
            os.path.join(reports_path, f))]

        reports_df = None
        for report_dir in report_dirs:
            tmp_df = self._process(reports_path, report_dir)
            if reports_df is None:
                reports_df = tmp_df
            else:
                reports_df = pd.concat([reports_df, tmp_df], ignore_index=True)

        return reports_df

    def _process(self, reports_path, report_dir):
        year, month, day, hour, minute, second = self.time_formatter.format(
            report_dir)
        report_df = self.resource_processor.process(reports_path + report_dir)
        report_df['DateTime'] = datetime.datetime(
            year=year, month=month, day=day,
            hour=hour, minute=minute, second=second)
        report_df.sort_values('DateTime', ascending=True, inplace=True)

        return report_df
