from .base import Exporter

class GeoJsonExporter(Exporter):

    def export(self, model):
        return ''.join(model)