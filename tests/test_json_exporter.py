from pyparus.exporters import JsonExporter

def test_json_exporter_exists():
    assert JsonExporter() is not None
