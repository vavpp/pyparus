from .base import Exporter

from uml.elements import (
    UmlPrimitive,
    UmlEnumeration,
    UmlClass,
)


SQL_TYPES = {
    "String": "TEXT",
    "Integer": "INTEGER",
    "Real": "REAL",
    "Boolean": "BOOLEAN",
    "EDate": "DATE",
}


class SqlExporter(Exporter):

    def __init__(self):

        self.model = None
        self.sql = []

    def export(self, model):

        self.model = model
        self.sql = []

        self._header()
        self._tables()
        self._views()

        return "\n".join(self.sql)

    def _add(self, text=""):

        self.sql.append(text)

    #
    # Header
    #

    def _header(self):

        self._add("-- Generert fra UML-modell")
        self._add()

    #
    # Tables
    #

    def _tables(self):

        for cls in self.model.classes.values():

            self._table(cls)

    def _table(self, cls):

        self._add(
            f"CREATE TABLE {self._name(cls.name)} ("
        )

        columns = []

        #
        # ObjektID som PK
        #
        has_objektid = False

        for attribute in cls.attributes:

            if attribute.name.lower() == "objektid":

                has_objektid = True

                columns.append(
                    "objektid TEXT PRIMARY KEY"
                )

        if not has_objektid:

            columns.append(
                "objektid TEXT PRIMARY KEY"
            )

        #
        # Primitive attributter
        #
        for attribute in cls.attributes:

            if attribute.name.lower() == "objektid":
                continue

            if not isinstance(
                attribute.type,
                UmlPrimitive
            ):
                continue

            sql_type = SQL_TYPES.get(
                attribute.type.name,
                "TEXT"
            )

            columns.append(
                f"{self._name(attribute.name)} {sql_type}"
            )

        #
        # Enum-attributter
        #
        for attribute in cls.attributes:

            if not isinstance(
                attribute.type,
                UmlEnumeration
            ):
                continue

            columns.append(
                f"{self._name(attribute.name)} TEXT"
            )

        #
        # Relasjoner
        #
        for attribute in cls.attributes:

            if not isinstance(
                attribute.type,
                UmlClass
            ):
                continue

            columns.append(
                f"{self._name(attribute.name)}_id TEXT"
            )

        self._add(
            ",\n".join(
                f"    {column}"
                for column in columns
            )
        )

        self._add(");")
        self._add()

    #
    # Views
    #

    def _views(self):

        self._add("--")
        self._add("-- Inheritance Views")
        self._add("--")
        self._add()

        for cls in self.model.classes.values():

            if not cls.generalization:
                continue

            if not cls.generalization.parent:
                continue

            self._view(cls)

    def _view(self, cls):

        hierarchy = self._hierarchy(cls)

        self._add(
            f"CREATE VIEW vw_{self._name(cls.name)} AS"
        )

        self._add("SELECT")

        columns = []

        alias_no = 1

        for current in hierarchy:

            alias = f"t{alias_no}"

            for attribute in current.attributes:

                columns.append(
                    f"    {alias}.{self._name(attribute.name)}"
                )

            alias_no += 1

        self._add(",\n".join(columns))

        root = hierarchy[0]

        self._add(
            f"FROM {self._name(root.name)} t1"
        )

        alias_no = 2

        for current in hierarchy[1:]:

            alias = f"t{alias_no}"

            self._add(
                f"JOIN {self._name(current.name)} {alias}"
            )

            self._add(
                f"  ON t1.objektid = {alias}.objektid"
            )

            alias_no += 1

        self._add(";")
        self._add()

    #
    # Helpers
    #

    def _hierarchy(self, cls):

        hierarchy = []

        current = cls

        while current is not None:

            hierarchy.insert(0, current)

            if (
                current.generalization
                and current.generalization.parent
            ):
                current = current.generalization.parent
            else:
                current = None

        return hierarchy

    def _name(self, name):

        return (
            name
            .replace("Å", "A")
            .replace("Æ", "AE")
            .replace("Ø", "O")
            .replace("å", "a")
            .replace("æ", "ae")
            .replace("ø", "o")
            .lower()
        )