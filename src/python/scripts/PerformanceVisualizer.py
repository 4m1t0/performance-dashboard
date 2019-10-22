from modules import Plot, PreProcessor, TimeFormatter
import os


class PerformanceVisualizer:
    def __init__(self, preprocessor):
        self.preprocessor = preprocessor
        self.keys = [
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

    def visualize(self, path):
        reports = self.preprocessor.process(path)

        static_dir = os.path.join(
            os.path.dirname(__file__),
            '../../javascript/static')
        if not os.path.isdir(static_dir + '/shared'):
            os.makedirs(static_dir + '/shared')

        plot = Plot.Plot(reports)

        plot.percentilePlot(
            key='99%',
            filename=static_dir +
                '/shared/99percentiles.html')
        plot.rpsTimelineChart(
            filename=static_dir
            + '/shared/rps-timeline-chart.html')
        plot.requestsTimelineChart(
            key='# requests',
            title='# of requests',
            filename=static_dir +
                '/shared/num-of-requests.html')
        plot.requestsTimelineChart(
            key='# failures',
            title='# of failures',
            filename=static_dir +
                '/shared/num-of-errors.html')
        plot.activityChart(
            filename=static_dir +
            '/shared/activity-chart.html')

        uniq_reports = sorted(reports['Name'].unique())
        for uniq_report in uniq_reports:
            additional_path = 'total/' if uniq_report == 'Total' \
                else ''.join(
                    uniq_report.split(' ')).lower() + '/'

            plot_path = static_dir + '/' + additional_path
            if not os.path.isdir(plot_path):
                os.makedirs(plot_path)

            plot.distributedDotPlot(
                name=uniq_report,
                filename=plot_path
                + 'distributed-dot-plot.html')

            plot.rpsTimelineChart(
                name=uniq_report,
                filename=plot_path
                + 'rps-timeline-chart.html')

            for key in self.keys:
                prefix = key.split(' ')[0].lower(
                ) if 'time' in key else key[:2] + 'percentile'

                plot.percentilePlot(
                    name=uniq_report,
                    key=key,
                    filename=plot_path
                    + prefix + '-timeline-chart.html')
                plot.degradationPlot(
                    name=uniq_report,
                    key=key,
                    filename=plot_path
                    + prefix + '-degradation-timeline-chart.html')

    def debug(self):
        df = self.preprocessor.process(
            os.path.join(os.path.dirname(__file__), '../resources/reports/')
        )
        df.to_csv('debug.csv', index=False)


time_formatter = TimeFormatter.TimeFormatter('YYYYMMDD_HHMMSS1')
visualizer = PerformanceVisualizer(
    PreProcessor.PreProcessor('LOCUST', time_formatter))
visualizer.visualize(
    os.path.join(os.path.dirname(__file__), '../resources/reports/')


)
# visualizer.debug()
