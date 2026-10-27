from .base import Exporter

from uml.elements import (
    UmlPackage,
    UmlPrimitive,
    UmlEnumeration,
    UmlClass
)


class MarkdownExporter(Exporter):

    def __init__(self):

        self.model = None
        self.md = []

    def export(self, model):

        self.model = model
        self.md = []

        self._title()
        self._packages()
        self._classes()
        self._enumerations()

        return "\n".join(self.md)

    def _add(self, text=""):

        self.md.append(text)

    def _title(self):

        self._add("# UML Modell")
        self._add()

    def _packages(self):

        self._add("## Pakker")
        self._add()

        for package in self.model.packages.values():

            self._add(f"- {package.name}")

        self._add()

    def _classes(self):

        self._add("## Klasser")
        self._add()

        for cls in self.model.classes.values():

            self._class(cls)

    def _class(self, cls):

        self._add(f"## {cls.name}")
        self._add()

        self._abstract(cls)
        self._generalization(cls)
        self._owner(cls)

        self._primitive_attributes(cls)
        self._enumeration_attributes(cls)
        self._relations(cls)

        self._add("---")
        self._add()

    def _abstract(self, cls):

        if cls.abstract:

            self._add("*Abstrakt klasse*")
            self._add()

    def _generalization(self, cls):

        if cls.generalization and cls.generalization.parent:

            self._add(
                f"Arver fra: **{cls.generalization.parent.name}**"
            )

            self._add()

    def _owner(self, cls):

        if not cls.owner:
            return

        if isinstance(cls.owner, UmlPackage):

            self._add(
                f"Pakke: **{cls.owner.name}**"
            )

        else:

            self._add(
                f"Owner: **{cls.owner.name}**"
            )

        self._add()

    def _attribute_table(self, title, attributes):

        self._add(f"### {title}")
        self._add()

        if not attributes:

            self._add("_Ingen_")
            self._add()
            return

        self._add("| Navn | Type |")
        self._add("|------|------|")

        for attribute in attributes:

            self._add(
                f"| {attribute.name} | {attribute.type.name} |"
            )

        self._add()

    def _primitive_attributes(self, cls):

        attributes = [

            a for a in cls.all_attributes()

            if isinstance(a.type, UmlPrimitive)
        ]

        self._attribute_table(
            "Primitive attributter",
            attributes
        )

    def _enumeration_attributes(self, cls):

        attributes = [

            a for a in cls.all_attributes()

            if isinstance(a.type, UmlEnumeration)
        ]

        self._attribute_table(
            "Enumerasjoner",
            attributes
        )

    def _relations(self, cls):

        relations = [

            a for a in cls.all_attributes()

            if isinstance(a.type, UmlClass)
        ]

        self._add("### Relasjoner")
        self._add()

        if not relations:

            self._add("_Ingen relasjoner_")
            self._add()
            return

        for relation in relations:

            self._add(
                f"- {relation.name} → {relation.type.name}"
            )

        self._add()

    def _enumerations(self):

        self._add("## Enumerasjoner")
        self._add()

        for enum in self.model.enumerations.values():

            self._add(f"### {enum.name}")
            self._add()

            for literal in enum.literals:

                self._add(
                    f"- {literal.name}"
                )

            self._add()