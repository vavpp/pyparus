# PyParus

PyParus is a Python library for parsing Papyrus UML models and generating code, documentation and diagrams.

## Features

- Parse Papyrus UML models
- SQL generation
- SQLAlchemy generation
- JSON export
- Markdown export
- PlantUML export

## Installation

```bash
pip install pyparus
## Example
from pyparus import UmlParser
from pyparus.exporters import SqlAlchemyExporter

model = UmlParser().parse_file("model.uml")

code = SqlAlchemyExporter().export(model)
print(code)