from dataclasses import dataclass, field


@dataclass
class UmlElement:
    id: str
    name: str | None = None
    owner: str |None = None
    children: list = field(default_factory=list)
    def set_owner(self, owner):
        self.owner = owner
        if owner is not None:
            owner.children.append(self)


@dataclass
class UmlPackage(UmlElement):
    packages: list = field(default_factory=list)
    classes: list = field(default_factory=list)
    enumerations: list = field(default_factory=list)


@dataclass
class UmlType(UmlElement):
    pass


@dataclass
class UmlPrimitive(UmlType):
    href: str | None = None


@dataclass
class UmlEnumerationLiteral(UmlElement):
    pass


@dataclass
class UmlEnumeration(UmlType):
    literals: list = field(default_factory=list)


@dataclass
class UmlAttribute(UmlElement):

    type_id: str | None = None

    type: UmlType | None = None

    lower: int | None = None

    upper: str | None = None

    association: str | None = None

    is_association_end: bool = False


@dataclass
class UmlGeneralization:

    parent_id: str

    parent = None


@dataclass
class UmlAssociation(UmlElement):

    member_end_ids: list = field(default_factory=list)

    member_ends: list = field(default_factory=list)


@dataclass
class UmlClass(UmlType):

    abstract: bool = False

    attributes: list = field(default_factory=list)

    associations: list = field(default_factory=list)

    generalization: UmlGeneralization | None = None

    children: list = field(default_factory=list)

    nested_classes: list = field(default_factory=list)

    owner = None

    def all_attributes(self):

        attributes = []

        if self.generalization is not None:
            parent = self.generalization.parent

            if parent is not None:
                yield from parent.all_attributes()

        yield from self.attributes

@dataclass
class UmlAssociationEnd:
    attribute_id: str | None = None
    attribute = None
    owner = None
    role_name: str | None = None
    lower: int | None = None
    upper: str | None = None

@dataclass
class UmlAssociation(UmlElement):
    member_end_ids: list = field(default_factory=list)
    member_ends: list = field(default_factory=list)