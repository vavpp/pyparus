from uml import UmlParser
from uml.exporters import JsonExporter, MarkdownExporter, SqlExporter, PlantUmlExporter, SqlAlchemyExporter

model = UmlParser().parse("../Flydataforvaltning.uml")
#print(JsonExporter().export(model))

with open('export.json', 'w', encoding='utf-8') as f:
    f.write(JsonExporter().export(model))

markdown = MarkdownExporter().export(model)
with open('model.md', 'wb') as f:
    f.write(markdown.encode())

with open('model.sql', 'w', encoding='utf-8') as f:
    f.write(SqlExporter().export(model))

with open('model.puml', 'w', encoding='utf-8') as f:
    f.write(PlantUmlExporter().export(model))

with open('models.py', 'w', encoding='utf-8') as f:
    f.write(SqlAlchemyExporter().export(model))




