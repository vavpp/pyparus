from .elements import (
    UmlClass,
    UmlEnumeration,
    UmlAssociation,
    UmlPackage,
    UmlPrimitive
)


class UmlModel:

    def __init__(self):

        self.packages = {}

        self.classes = {}

        self.enumerations = {}

        self.associations = {}

        self.primitives = {}

        self.attributes = {}

        self.types = {}

    def add_attribute(self, attribute):

        self.attributes[attribute.id] = attribute

    def add_package(self, package: UmlPackage):

        self.packages[package.id] = package

    def add_class(self, cls: UmlClass):

        self.classes[cls.id] = cls

        self.types[cls.id] = cls

    def add_enumeration(self, enum: UmlEnumeration):

        self.enumerations[enum.id] = enum

        self.types[enum.id] = enum

    def add_association(self, association: UmlAssociation):

        self.associations[association.id] = association

    def add_primitive(self, primitive: UmlPrimitive):

        self.primitives[primitive.id] = primitive

        self.types[primitive.id] = primitive

    def find(self, id):

        return self.types.get(id)
    
    

