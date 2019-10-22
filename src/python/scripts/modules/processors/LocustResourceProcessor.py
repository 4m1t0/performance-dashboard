import logging
import pandas as pd
import os
import sys


class LocustResourceProcessor:
    def __init__(
            self,
            distribution_filename='distribution.csv',
            requests_filename='requests.csv'):
        self.reports = dict(
            distribution=distribution_filename,
            requests=requests_filename
        )

    def process(self, report_dir):
        reports = os.listdir(report_dir)
        self._validateDir(reports)

        distribution_df = pd.read_csv(os.path.join(
            report_dir, './' + self.reports['distribution']))
        requests_df = pd.read_csv(os.path.join(
            report_dir, './' + self.reports['requests']))

        # format Name for merging
        for index, row in requests_df.iterrows():
            if row['Name'] == 'Total':
                requests_df.at[index, 'tmp_name'] = row['Name']
            else:
                requests_df.at[index, 'tmp_name'] = row['Method'] + \
                    ' ' + row['Name']

        return pd.merge(
            distribution_df,
            # Because distribution_df has Name and # requests.
            requests_df.drop(['Name', '# requests'], axis=1),
            how='inner', left_on=['Name'], right_on=['tmp_name']
        ).drop('tmp_name', axis=1)  # Drop the tmp name

    def _validateDir(self, reports):
        if self.reports['distribution'] not in reports or \
                self.reports['requests'] not in reports:
            logging.critical(
                'Invalid Usage: locust generates 2 csv files, distribution.csv \
                    and requests.csv. Please set the files in the report_dir.')
            sys.exit(1)
