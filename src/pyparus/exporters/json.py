import json

from .base import Exporter


class JsonExporter(Exporter):

    def export(self, model):

        data = {
            "packages": [],
            "classes": [],
            "enumerations": [],
            "associations": []
        }

        #
        # packages
        #
        for package in model.packages.values():

            data["packages"].append({
                "id": package.id,
                "name": package.name,
                "owner": (
                    package.owner.id
                    if package.owner else None
                )
            })

        #
        # classes
        #
        for cls in model.classes.values():

            class_data = {
                "id": cls.id,
                "name": cls.name,
                "abstract": cls.abstract,
                "owner": (
                    cls.owner.id
                    if cls.owner else None
                ),
                "generalization": None,
                "attributes": []
            }

            if cls.generalization:
                class_data["generalization"] = \
                    cls.generalization.parent_id

            for attr in cls.attributes:

                class_data["attributes"].append({
                    "id": attr.id,
                    "name": attr.name,
                    "type": (
                        attr.type.name
                        if attr.type else None
                    ),
                    "type_id": attr.type_id,
                    "association": attr.association
                })

            data["classes"].append(class_data)

        #
        # enums
        #
        for enum in model.enumerations.values():

            data["enumerations"].append({
                "id": enum.id,
                "name": enum.name,
                "literals": [
                    literal.name
                    for literal in enum.literals
                ]
            })

        #
        # associations
        #
        for association in model.associations.values():

            data["associations"].append({
                "id": association.id,
                "name": association.name,
                "member_end_ids":
                    association.member_end_ids
            })

        return json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        )