# %%
import dash
import dash_html_components as html
import dash_core_components as dcc
import numpy as np
import datetime
import logging
import os
import pandas as pd
import plotly.offline as offline
import plotly.graph_objs as go
import sys

# %%
offline.init_notebook_mode(connected=False)
df = pd.read_csv(os.path.join(
    os.path.dirname(__file__), 'debug.csv'))
df.sort_values('DateTime', ascending=True, inplace=True)
result = []
for dt in df['DateTime'].tolist():
    tmp = dt.split(' ')
    _date, _time = tmp[0].split('-'), tmp[1].split(':')

    year, month, day = int(_date[0]), int(_date[1]), int(_date[2])
    hour, minute, second = int(_time[0]), int(_time[1]), int(_time[2])
    result.append(datetime.datetime(
        year=year, month=month, day=day,
        hour=hour, minute=minute, second=second))
df['DateTime'] = result
df

# %%
# static_dir = os.path.join(
#     os.path.dirname(__file__),
#     '../../javascript/static')
# os.mkdir(static_dir + '/shared')
# uniq_reports = df['Name'].unique()
# for uniq_report in uniq_reports:
#     additional_path = 'total' if uniq_report == 'Total' \
#         else ''.join(uniq_report.split(' ')).lower() + '/'
#     os.makedirs(static_dir + '/' + additional_path)
# %%
# uniq_reports
# %%


def percentilePlot(reports, name=None, key=None, filename=None):
    if key is None or filename is None:
        logging.critical('Invalid Usage: Please assign both key and filename.')
        sys.exit(1)

    data = []
    if name is None:
        names = sorted(reports['Name'].unique(), reverse=False)
        for name in names:
            data.append(_percentileScatter(reports, name, key))
    else:
        data.append(_percentileScatter(reports, name, key))

    layout = go.Layout(
        title=key + 'tile Latency Timeline Chart',
        xaxis=dict(gridcolor='#2B3D59', zeroline=False),
        yaxis=dict(title='Latency (ms)',
                   gridcolor='#2B3D59', zeroline=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F2F2F2", size=11),
        legend=dict(x=1, y=0.5))

    fig = go.Figure(data=data, layout=layout)
    offline.plot(fig, filename=filename)


def _percentileScatter(reports, name, key):
    text = [
        'DateTime: ' +
        d.astype('M8[ms]').astype('O').isoformat().replace('T', ' ')
        + '<br>Latency: ' + str(l)
        for d, l in zip(
            reports[reports['Name'] == name]['DateTime'].values,
            reports[reports['Name'] == name][key].values)]
    return go.Scatter(
        x=reports[reports['Name'] == name]['DateTime'],
        y=reports[reports['Name'] == name][key],
        name=name,
        text=text,
        hoverinfo='text+name'
    )


percentilePlot(
    df,
    key='99%',
    filename=os.path.join(
        os.path.dirname(__file__),
        '../../javascript/static/shared/99percentile-timeline-chart.html'))


# %%
def requestsTimeChart(reports, key=None, title=None, filename=None):
    if key is None or title is None or filename is None:
        logging.critical('Invalid Usage: Please assign both key and filename.')
        sys.exit(1)

    names = sorted(reports['Name'].unique(), reverse=False)
    data = []
    for name in names:
        data.append(go.Scatter(
            x=reports[reports['Name'] == name]['DateTime'],
            y=reports[reports['Name'] == name][key],
            name=name
        ))
    layout = go.Layout(
        title=title,
        xaxis=dict(title='DateTime', gridcolor='#2B3D59', zeroline=False),
        yaxis=dict(gridcolor='#2B3D59', zeroline=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F2F2F2", size=11),
        legend=dict(x=1, y=0.5))

    fig = go.Figure(data=data, layout=layout)
    offline.plot(fig, filename=filename)


requestsTimeChart(
    df,
    key='# requests',
    title='# of requests',
    filename=os.path.join(
        os.path.dirname(__file__),
        '../../javascript/static/shared/num-of-requests.html'))

requestsTimeChart(
    df,
    key='# failures',
    title='# of errors',
    filename=os.path.join(
        os.path.dirname(__file__),
        '../../javascript/static/shared/num-of-errors.html'))
# %%


def activityChart(reports, filename=None):
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
    for report in reports['DateTime'].unique():
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
                [0, '#1D2A3D'],
                [0.5, '#2dce89'],
                [1, '#68FF17']]
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
    offline.plot(fig, filename=filename)


activityChart(df, filename=os.path.join(
    os.path.dirname(__file__),
    '../../javascript/static/shared/activity-chart.html'))

# %%


def distributedDotPlot(reports, name=None, filename=None):
    if name is None or filename is None:
        logging.critical(
            'Invalid Usage: Please assign both key and filename.')
        sys.exit(1)

    df = reports[reports['Name'] == name]

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
    offline.plot(fig, filename=filename)


distributedDotPlot(
    df,
    name='GET /',
    filename=os.path.join(
         os.path.dirname(__file__),
        '../../javascript/static/get/distributed-dot-plot.html'))

# %%
percentilePlot(
    df,
    name='GET /',
    key='99%',
    filename=os.path.join(
        os.path.dirname(__file__),
        '../../javascript/static/get/99percentile-timeline-chart.html'))


# %%
def degradationPlot(reports, name=None, key=None, filename=None):
    if name is None or key is None or filename is None:
        logging.critical(
            'Invalid Usage: Please assign name, key and filename.')
        sys.exit(1)

    df = reports[reports['Name'] == name]
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
        font=dict(color="#F2F2F2", size=11),
        legend=dict(x=1, y=0.5))

    fig = go.Figure(data=data, layout=layout)
    offline.plot(fig, filename=filename, auto_open=False)


degradationPlot(
    df,
    name='GET /',
    key='99%',
    filename=os.path.join(
        os.path.dirname(__file__),
        '../../javascript/static/get/99percentile-degradation-timeline-chart.html'))

# %%
sorted(df['Name'].unique())


#%%
