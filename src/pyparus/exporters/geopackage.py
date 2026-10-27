from .base import Exporter

class GeoPackageExporter(Exporter):

    def export(self, model):
        return ''.join(model)