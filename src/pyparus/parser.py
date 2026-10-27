from lxml import etree as ET

from .model import UmlModel
from .elements import (
    UmlPackage,
    UmlClass,
    UmlAttribute,
    UmlEnumeration,
    UmlEnumerationLiteral,
    UmlAssociation,
    UmlGeneralization
)
from .resolver import Resolver

XMI = "{http://www.omg.org/spec/XMI/20131001}"


class UmlParser:

    def parse(self, filename):

        tree = ET.parse(filename)
        root = tree.getroot()

        model = UmlModel()

        for child in root:
            self._read_elements(
                child,
                model,
                owner=None
            )

        Resolver(model).resolve()

        return model

    def _read_elements(self, elem, model, owner):

        current_owner = owner

        xmi_type = elem.attrib.get(f"{XMI}type")

        #
        # Containere
        #
        if xmi_type == "uml:Package":

            current_owner = self._read_package(
                elem,
                model,
                owner
            )

        elif xmi_type == "uml:Class":

            current_owner = self._read_class(
                elem,
                model,
                owner
            )

        #
        # Ikke-containere
        #
        elif xmi_type == "uml:Enumeration":

            self._read_enumeration(
                elem,
                model,
                owner
            )

        elif xmi_type == "uml:Association":

            self._read_association(
                elem,
                model,
                owner
            )

        #
        # Rekursiv traversering
        #
        for child in elem:
            self._read_elements(
                child,
                model,
                current_owner
            )

    def _read_package(self, elem, model, owner):
        
        package = UmlPackage(
            id=elem.attrib[f"{XMI}id"],
            name=elem.attrib.get("name")
        )

        package.set_owner(owner)

        model.add_package(package)

        return package
      
    def _read_class(self, elem, model, owner):

        cls = UmlClass(
            id=elem.attrib[f"{XMI}id"],
            name=elem.attrib.get("name"),
            abstract=elem.attrib.get("isAbstract") == "true"
        )

        cls.set_owner(owner)

        model.add_class(cls)

        #
        # attributter
        #
        for attr in elem.findall("ownedAttribute"):

            type_id = attr.attrib.get("type")

            #
            # Primitive types
            #
            if type_id is None:

                type_elem = attr.find("type")

                if type_elem is not None:

                    href = type_elem.attrib.get("href")

                    if href:
                        type_id = href

            attribute = UmlAttribute(
                id=attr.attrib.get(f"{XMI}id"),
                name=attr.attrib.get("name"),
                type_id=type_id,
                association=attr.attrib.get("association")
            )

            attribute.set_owner(cls)

            cls.attributes.append(attribute)
            model.add_attribute(attribute)

            #
            # dersom du senere legger inn:
            #
            # model.add_attribute(attribute)
            #
            # så kan denne linjen aktiveres:
            #
            # model.add_attribute(attribute)

        #
        # generalisering
        #
        generalization = elem.find("generalization")

        if generalization is not None:

            cls.generalization = UmlGeneralization(
                parent_id=generalization.attrib["general"]
            )

        return cls

    def _read_enumeration(self, elem, model, owner):

        enum = UmlEnumeration(
            id=elem.attrib[f"{XMI}id"],
            name=elem.attrib.get("name")
        )

        enum.set_owner(owner)

        model.add_enumeration(enum)

        for literal in elem.findall("ownedLiteral"):

            enum_literal = UmlEnumerationLiteral(
                id=literal.attrib[f"{XMI}id"],
                name=literal.attrib.get("name")
            )

            enum_literal.set_owner(enum)

            enum.literals.append(enum_literal)

    def _read_association(self, elem, model, owner):

        member_end = elem.attrib.get(
            "memberEnd",
            ""
        )

        association = UmlAssociation(
            id=elem.attrib[f"{XMI}id"],
            name=elem.attrib.get("name"),
            member_end_ids=member_end.split()
        )

        model.add_association(association)
        association.owned_ends = []

        #
        # ownedEnd
        #
        for child in elem.findall("ownedEnd"):

            attribute = UmlAttribute(
                id=child.attrib.get(f"{XMI}id"),
                name=child.attrib.get("name"),
                type_id=child.attrib.get("type"),
                association=association.id,
                is_association_end=True
            )
            
            association.owned_ends.append(attribute)
            model.add_attribute(attribute)