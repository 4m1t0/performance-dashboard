from modules import PerformanceReport, PreProcessor, TimeFormatter
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

        performance_report = PerformanceReport.PerformanceReport(reports)

        performance_report.percentilePlot(
            key='99%',
            filename=static_dir +
                '/shared/99percentiles.html')
        performance_report.rpsTimelineChart(
            filename=static_dir
            + '/shared/rps-timeline-chart.html')
        performance_report.requestsTimelineChart(
            key='# requests',
            title='# of requests',
            filename=static_dir +
                '/shared/num-of-requests.html')
        performance_report.requestsTimelineChart(
            key='# failures',
            title='# of failures',
            filename=static_dir +
                '/shared/num-of-errors.html')
        performance_report.activityChart(
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

            performance_report.distributedDotPlot(
                name=uniq_report,
                filename=plot_path
                + 'distributed-dot-plot.html')

            performance_report.rpsTimelineChart(
                name=uniq_report,
                filename=plot_path
                + 'rps-timeline-chart.html')

            for key in self.keys:
                prefix = key.split(' ')[0].lower(
                ) if 'time' in key else key[:2] + 'percentile'

                performance_report.percentilePlot(
                    name=uniq_report,
                    key=key,
                    filename=plot_path
                    + prefix + '-timeline-chart.html')
                performance_report.degradationPlot(
                    name=uniq_report,
                    key=key,
                    filename=plot_path
                    + prefix + '-degradation-timeline-chart.html')


time_formatter = TimeFormatter.TimeFormatter('YYYYMMDD_HHMMSS1')
visualizer = PerformanceVisualizer(
    PreProcessor.PreProcessor('LOCUST', time_formatter))
visualizer.visualize(
    os.path.join(os.path.dirname(__file__), '../resources/reports/'))
