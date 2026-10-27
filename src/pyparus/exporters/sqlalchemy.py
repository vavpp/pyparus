
TYPE_MAP = {
    "String": ("str", "String"),
    "Integer": ("int", "Integer"),
    "Long": ("int", "BigInteger"),
    "Boolean": ("bool", "Boolean"),
    "Double": ("float", "Float"),
    "Float": ("float", "Float"),
    "Date": ("date", "Date"),
    "EDate": ("date", "Date"),
    "DateTime": ("datetime", "DateTime"),
    "UUID": ("uuid.UUID", "Uuid"),
}


class SqlAlchemyExporter:

    def __init__(self):
        self.model = None

    def export(
        self,
        model
    ):
        self.model = model
        self.enum_names = {
            enum.name
            for enum in model.enumerations.values()
        }
        self.class_names = {
            cls.name
            for cls in model.classes.values()
        }

        lines = []

        lines.extend(self._header())
        lines.extend(self._enums())
        lines.extend(self._tables())
        lines.extend(self._views())

        return "\n".join(lines)
    

    def _header(self):
        lines = [
            "from __future__ import annotations",
            "",
            "import uuid",
            "from datetime import date, datetime",
            "",
            "from sqlalchemy import (",
            "    String, Integer, Float, Boolean,",
            "    Date, DateTime, ForeignKey, Enum",
            ")",
            "from sqlalchemy.orm import (",
            "    DeclarativeBase,",
            "    Mapped,",
            "    mapped_column,",
            "    relationship,",
            ")",
            "",
            "",
            "class Base(DeclarativeBase):",
            "    pass",
            "",
        ]
        return lines
    def _tables(self):
        lines = []

        for cls in self.model.classes.values():
            lines.extend(self._table(cls))
            lines.append("")

        return lines
    
    def _views(self):
        return []
    
    def _enums(self):
        lines = []

        if not self.model.enumerations:
            return lines

        lines.append("import enum")
        lines.append("")

        for enum_obj in self.model.enumerations.values():

            lines.append(
                f"class {enum_obj.name}(enum.Enum):"
            )

            for value in enum_obj.literals:

                enum_name = (
                    value.name.upper()
                    .replace(" ", "_")
                    .replace("-", "_")
                )

                lines.append(
                    f'    {enum_name} = "{value.name}"'
                )

            lines.append("")
            lines.append("")

        return lines
    
    def _table(self, cls):

        lines = []

        lines.append(
            f"class {cls.name}(Base):"
        )

        lines.append(
            f'    __tablename__ = "{cls.name.lower()}"'
        )

        lines.append("")
        has_pk = any(
            attr.name.lower() == "id"
            for attr in cls.attributes
        )
        if not has_pk:
            lines.append(
                "    id: Mapped[int] = mapped_column(Integer, primary_key=True)"
            )
            lines.append("")

        for attribute in cls.attributes:
            column = self._column(attribute)

            if column:
                lines.append(
                    self._column(attribute)
             )


        lines.extend(self._relationships(cls))

        return lines
    def _column(self, attribute):
        """
        Generate a mapped_column() definition.
        """

        attr_type = getattr(attribute, "type", None)

        # Hvis type er UML-objekt
        if hasattr(attr_type, "name"):
            attr_type = attr_type.name

        attr_type = str(attr_type)
        # Klasse-referanser håndteres av _relationships()
        if attr_type in self.class_names:
            return f'    {attribute.name}_id: Mapped[int] = mapped_column(ForeignKey("{attr_type.lower()}.id"))'


        # Enum?
        if attr_type in self.enum_names:
            return (
                f"    {attribute.name}: "
                f"Mapped[{attr_type}] = "
                f"mapped_column(Enum({attr_type}))"
            )

        py_type, sa_type = TYPE_MAP.get(
            str(attr_type),
            ("str", "String")
        )

        args = [sa_type]

        if attribute.name.lower() == "id":
            args.append("primary_key=True")

        return (
            f"    {attribute.name}: Mapped[{py_type}] = "
            f"mapped_column({', '.join(args)})"
        )
    def _relationships(self, cls):
        lines = []

        for attribute in cls.attributes:

            attr_type = attribute.type

            if hasattr(attr_type, "name"):
                attr_type = attr_type.name

            if attr_type in self.class_names:

                lines.append(
                    f'    {attribute.name}: Mapped["{attr_type}"] = relationship()'
                )

        return lines