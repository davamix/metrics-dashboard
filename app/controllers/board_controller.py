import base64
from io import BytesIO
from flask import render_template
from flask.views import MethodView
from matplotlib.figure import Figure
from flask import request
from flask_socketio import emit
from models.metrics.metric import Metric

class BoardController(MethodView):
    def __init__(self, metrics, merged, socket):
        self.metrics = metrics
        self.merged_metrics = merged
        self.socket = socket

        self.socket.on_event("merge", self.create_merge)

    def create_figure(self, metrics):
        """
        Create a new matplotlib figure based on the metrics

        :param array metrics: Array of Metric entities to be draw
        :return: image encoded in base64 and the figure name
        :rtype: string, string
        """
        # Sort the metrics by name in order to draw the same figure in case there are more than one
        metrics = sorted(metrics, key=lambda x: x.name)

        fig = Figure(figsize=(7,3))
        ax = fig.subplots()

        # Figure title
        figure_name = " & ".join([m.name for m in metrics])
        ax.set_title(figure_name)

        # Plot metrics
        for m in metrics:
            ax.plot(m.get_values(), label=m.name)

        ax.legend()

        buf = BytesIO()
        fig.savefig(buf, format="png")

        return base64.b64encode(buf.getbuffer()).decode("ascii")

    def get(self):
        return render_template('dashboard.html', title="Metrics")

    def post(self):
        # data is a dictionary {"metric_name": value}
        data = request.get_json()
        storage_key = None

        if data:
            # Clean the key names
            parsed_data = self.clean_data(data)

            updated_metrics = self.update_metric_values(parsed_data)

            # Merge metrics if there are more than one
            if len(updated_metrics) > 1:
                storage_key = self.merge_metrics(updated_metrics)
            else:
                storage_key = next(iter(parsed_data))

            # Get the merged metrics if any
            merged_metrics = set()
            for m in updated_metrics:
                metric_names = self.get_merges(m.name)
                merged_metrics.update([self.get_metric(x) for x in metric_names])

            # Add the current metrics
            merged_metrics.update(updated_metrics)
            storage_key = "__".join(m.name for m in sorted(merged_metrics, key=lambda x: x.name))

            figure = self.create_figure(merged_metrics)
            
            self.socket.emit("draw_metrics", {"name":storage_key, "value":figure})

        return "", 204

    def clean_data(self, data):
        """ 
        Parse the keys to escape invalid characters
        """
        parsed_data = {}
        # Clean the key names
        for d in data.keys():
            parsed_data[self.parse_name(d)] = data[d]

        return parsed_data

    def update_metric_values(self, data):
        """
        Update the values of the metric entities if exist, otherwise, create a new entity.
        :param dictionary: Dictionary with the metrics and values to be updated
        :return: List of metric entities updated
        :rtype: Metric[]
        """
        updated_metrics = []

        for metric in data:
            # Get the metric entity by name or create a new entity
            m = self.get_metric(metric)
            if m is None:
                m = self.create_metric(metric)

            # Add the value to the corresponding metric entity
            m.add_value(data[metric])

            updated_metrics.append(m)

        return updated_metrics


    def get_metric(self, metric_name):
        """
        Get the metric entity by name
        :param string metric_name: metric name
        :return: A metric entity
        :rtype: Metric
        """
        for m in self.metrics:
            if m.name == metric_name:
                return m

        return None

    def create_metric(self, metric_name):
        """
        Create a new Metric entity
        :param string metric_name: Name of the metric
        :return: A new metric entity
        :rtype: Metric
        """
        m = Metric(metric_name)
        self.metrics.append(m)

        return m

    def create_merge(self, metric_names):
        """
        Merge the metrics and draw the result
        :param array metric_names: list of metric names to be merged
        """
        parsed_names = []
        metric_entities = []

        for name in metric_names:
            parsed_name = self.parse_name(name)
            parsed_names.append(parsed_name)
            metric_entities.append(self.get_metric(parsed_name))

        storage_key = self.merge_metrics(metric_entities)
        
        figure = self.create_figure(metric_entities)

        self.socket.emit("draw_metrics", {"name":storage_key, "value":figure})
        self.socket.emit("merged", parsed_names)

        
    def get_merges(self, metric_name):
        """
        Get the metric names merged with metric_name
        :param string metric_name: Name of the metric from get the merged metrics
        :return: List of metrics names
        :rtype: array
        """
        if metric_name in self.merged_metrics:
            return self.merged_metrics[metric_name]

        for k in self.merged_metrics.keys():
            if metric_name in self.merged_metrics[k]:
                return self.merged_metrics[k]

        return []

    '''
    metrics: Metric[]
    '''
    def merge_metrics(self, metrics):
        """
        Add the metrics in the list of merged metrics
        :param Metric[] metrics: List of metric entities to be merged
        :return: Key generated from mergin the names of all entities
        :rtype: string
        """
        metric_entities = []

        storage_key = "__".join(m.name for m in sorted(metrics, key=lambda x: x.name))

        self.merged_metrics[storage_key] = [m.name for m in metrics]

        return storage_key

    def parse_name(self, name):
        """
        Escape invalid characters
        :param string name: String to be parsed
        :return: parsed string
        :rtype: string
        """
        return name.replace("&", "__").replace("/", "_")