import datetime
import logging
import pandas as pd
import plotly.offline as offline
import plotly.graph_objs as go
import sys


class PerformanceReport:

    def __init__(self, reports):
        """Performance Report as pandas DataFrame.

        Args:
            reports [pandas.DataFrame]: Having performance test reports and \
                following columns.
                    1.  Name: test target.
                    2.  # requests: number of requests.
                    3.  99%: 99%tile Latency. any %tile Latency is available \
                          because you have to assign key when plotting charts.
                    4.  Median response time: 50%tile Latency.
                    5.  Average response time: ditto.
                    6.  Min response time: ditto.
                    7.  Max response time: ditto.
                    8.  # failures: number of failures.
                    9.  Requests/s: requests per second.
                    10: DateTime [pandas.TimeStamp]: date executed test.
        """
        self.fontsize = 11
        self.reports = reports
        self.reports.sort_values('DateTime', ascending=True, inplace=True)

    def percentilePlot(self, name=None, key=None, filename=None):
        if key is None or filename is None:
            logging.critical(
                'Invalid Usage: Please assign both key and filename.')
            sys.exit(1)

        data = []
        if name is None:
            names = sorted(self.reports['Name'].unique(), reverse=False)
            for name in names:
                data.append(self._Scatter(name, key, 'Latency'))
        else:
            data.append(self._Scatter(name, key, 'Latency'))

        key = key + 'tile' if '%' in key else key.split(' ')[0]

        layout = go.Layout(
            title=key + ' Latency Timeline Chart',
            xaxis=dict(gridcolor='#2B3D59', zeroline=False),
            yaxis=dict(title='Latency (ms)',
                       gridcolor='#2B3D59', zeroline=False),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F2F2F2", size=self.fontsize),
            legend=dict(x=1, y=0.5),
            margin=dict(pad=2))

        fig = go.Figure(data=data, layout=layout)
        offline.plot(fig, filename=filename, auto_open=False)

    def _Scatter(self, name, key, label):
        text = [
            'DateTime: ' +
            d.astype('M8[ms]').astype('O').isoformat().replace('T', ' ')
            + '<br>' + label + ': ' + str(l)
            for d, l in zip(
                self.reports[self.reports['Name'] == name]['DateTime'].values,
                self.reports[self.reports['Name'] == name][key].values)]
        return go.Scatter(
            x=self.reports[self.reports['Name'] == name]['DateTime'],
            y=self.reports[self.reports['Name'] == name][key],
            name=name,
            text=text,
            hoverinfo='text+name'
        )

    def rpsTimelineChart(self, name=None, filename=None):
        if filename is None:
            logging.critical(
                'Invalid Usage: Please assign both name and filename.')
            sys.exit(1)

        data = []
        if name is None:
            names = sorted(self.reports['Name'].unique(), reverse=False)
            for name in names:
                data.append(self._Scatter(name, 'Requests/s', 'Requests/s'))
        else:
            data.append(self._Scatter(name, 'Requests/s', 'Requests/s'))

        layout = go.Layout(
            title='Rps Timeline Chart',
            xaxis=dict(gridcolor='#2B3D59', zeroline=False),
            yaxis=dict(gridcolor='#2B3D59', zeroline=False),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F2F2F2", size=self.fontsize),
            legend=dict(x=1, y=0.5),
            margin=dict(pad=2))

        fig = go.Figure(data=data, layout=layout)
        offline.plot(fig, filename=filename, auto_open=False)

    def requestsTimelineChart(self, key=None, title=None, filename=None):
        if key is None or title is None or filename is None:
            logging.critical(
                'Invalid Usage: Please assign both key and filename.')
            sys.exit(1)

        names = sorted(self.reports['Name'].unique(), reverse=False)
        data = []
        for name in names:
            t = key.split(' ')
            text = [
                'DateTime: ' +
                d.astype('M8[ms]').astype('O').isoformat().replace('T', ' ')
                + '<br>' + t[0] + ' of ' + t[1] + ': ' + str(l)
                for d, l in zip(
                    self.reports[self.reports['Name']
                                 == name]['DateTime'].values,
                    self.reports[self.reports['Name'] == name][key].values)]
            data.append(go.Scatter(
                x=self.reports[self.reports['Name'] == name]['DateTime'],
                y=self.reports[self.reports['Name'] == name][key],
                name=name,
                text=text,
                hoverinfo='text+name'
            ))
        layout = go.Layout(
            title=title,
            xaxis=dict(gridcolor='#2B3D59', zeroline=False),
            yaxis=dict(gridcolor='#2B3D59', zeroline=False),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#F2F2F2', size=self.fontsize),
            legend=dict(x=1, y=0.5),
            margin=dict(pad=2))

        fig = go.Figure(data=data, layout=layout)
        offline.plot(fig, filename=filename, auto_open=False)

    def activityChart(self, filename=None):
        now = datetime.datetime.now()
        d_now = datetime.date(now.year, now.month, now.day)

        offset = 0
        delta = 365 + offset

        pre_d_last_year = d_now - datetime.timedelta(days=delta)
        if pre_d_last_year.weekday():
            offset = pre_d_last_year.weekday()

        d_last_year = d_now - datetime.timedelta(days=delta)

        # gives me a list with datetimes for each day a year
        dates_in_year = [d_last_year +
                         datetime.timedelta(i) for i in range(delta+1)]

        # gives [0,1,2,3,4,5,6,0,1,2,3,4,5,6,…] (ticktext in xaxis dict translates this to weekdays
        weekdays_in_year = [-1 * i.weekday() for i in dates_in_year]
        # gives [1,1,1,1,1,1,1,2,2,2,2,2,2,2,…] name is self-explanatory
        start_dates_of_week = [
            d - datetime.timedelta(days=d.weekday()) if d.weekday() else d
            for d in dates_in_year]
        # z = np.random.randint(3, size=(len(dates_in_year))) / 2

        df = pd.DataFrame({
            'start_date': start_dates_of_week,
            'weekday': weekdays_in_year,
            'z': 0,
            'commits': 0
        })

        # count contributions per a day
        for report in self.reports['DateTime'].unique():
            report_date = report.astype('M8[D]').astype('O')
            weekday = report_date.weekday()
            start_date_of_week = report_date - \
                datetime.timedelta(days=weekday)

            target_record = df[
                (df['start_date'] == start_date_of_week) &
                (df['weekday'] == -1 * weekday)]

            if not target_record.empty:
                df.loc[(df['start_date'] == start_date_of_week) &
                       (df['weekday'] == -1 * weekday), ['z']] \
                    = target_record['z'] + 1 \
                    if target_record['z'].values[0] < 2 else 2
                df.loc[(df['start_date'] == start_date_of_week) &
                       (df['weekday'] == -1 * weekday), ['commits']] \
                    = target_record['commits'] + 1

        # gives something like list of strings like '2018-01-25' for each date. Used in data trace to make good hovertext.
        text = []
        for date in dates_in_year:
            start_date_of_week = date - \
                datetime.timedelta(days=date.weekday())
            commit = df[
                (df['start_date'] == start_date_of_week) &
                (df['weekday'] == -1 * date.weekday())]['commits']
            s = 'date: ' + str(date) + '<br>commits: ' + str(commit.values[0])
            text.append(s)

        data = [
            go.Heatmap(
                x=df['start_date'],
                y=df['weekday'],
                z=df['z'],
                text=text,
                hoverinfo='text',
                xgap=3,  # this
                ygap=3,  # and this is used to make the grid-like apperance
                showscale=False,
                colorscale=[
                    [0, '#223147'],
                    [0.5, '#00CC69'],
                    [1, '#66FA16']]
            )
        ]

        layout = go.Layout(
            title='Activity Chart',
            height=380,
            yaxis=dict(
                showline=False, showgrid=False, zeroline=False,
                tickmode='array',
                ticktext=['Sun', 'Sat', 'Fri', 'Thu', 'Wed', 'Tue', 'Mon'],
                tickvals=[-6, -5, -4, -3, -2, -1, 0]
            ),
            xaxis=dict(
                showline=False, showgrid=False, zeroline=False,
                side='top'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#F2F2F2', size=11),
            margin=dict(t=150, b=0, pad=5)
        )

        fig = go.Figure(data=data, layout=layout)
        offline.plot(fig, filename=filename, auto_open=False)

    def distributedDotPlot(self, name=None, filename=None):
        if name is None or filename is None:
            logging.critical(
                'Invalid Usage: Please assign both key and filename.')
            sys.exit(1)

        df = self.reports[self.reports['Name'] == name].sort_values(
            'DateTime', ascending=True, inplace=False)

        keys = [
            '50%',
            '66%',
            '75%',
            '80%',
            '90%',
            '95%',
            '98%',
            '99%',
            'Average response time',
            'Min response time',
            'Max response time'
        ]
        data = []
        for d in df['DateTime'].values:
            date = d.astype('M8[ms]').astype('O')
            date_for_label = date.isoformat().replace('T', ' ')
            for key in keys:
                if 'time' in key:
                    df[key.split(' ')[0].lower()] = df[key]
                    key = key.split(' ')[0].lower()
                color = '#FF1744' if key == '99%' else '#7986CB'
                data.append(go.Scatter(
                    x=df[df['DateTime'] == d][key],
                    y=[date.isoformat().replace('T', '<br>')],
                    text=['DateTime: ' + date_for_label + '<br>Latency: ' + str(l)
                          for l in df[df['DateTime'] == d][key].values],
                    name=key,
                    hoverinfo='text+name',
                    marker=dict(color=color)
                ))

        layout = go.Layout(
            title='Distribution of Latency',
            xaxis=dict(title='Latency (ms)',
                       gridcolor='#2B3D59', zeroline=False),
            yaxis=dict(gridcolor='#2B3D59', zeroline=False),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#F2F2F2', size=11),
            showlegend=False,
            margin=dict(pad=3))

        fig = go.Figure(data=data, layout=layout)
        offline.plot(fig, filename=filename, auto_open=False)

    def degradationPlot(self, name=None, key=None, filename=None):
        if name is None or key is None or filename is None:
            logging.critical(
                'Invalid Usage: Please assign name, key and filename.')
            sys.exit(1)

        df = self.reports[self.reports['Name'] == name]
        df_new = df.assign(diff=df[key].diff().fillna(0))
        text = ['DateTime: ' +
                d.astype('M8[ms]').astype('O').isoformat().replace('T', ' ')
                + '<br>Degraded Latency: ' + str(r)
                for d, r in zip(
                    df_new['DateTime'].values, df_new['diff']
                )]
        data = [go.Scatter(
            x=df_new['DateTime'],
            y=df_new['diff'],
            name=name,
            mode='lines+markers',
            text=text,
            hoverinfo='text+name'
        )]

        layout = go.Layout(
            title=key + 'tile Latency Degradation Timeline Chart',
            xaxis=dict(gridcolor='#2B3D59', zeroline=False),
            yaxis=dict(title='Latency (ms)',
                       gridcolor='#2B3D59', zeroline=False),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F2F2F2", size=self.fontsize),
            legend=dict(x=1, y=0.5),
            margin=dict(pad=2))

        fig = go.Figure(data=data, layout=layout)
        offline.plot(fig, filename=filename, auto_open=False)
