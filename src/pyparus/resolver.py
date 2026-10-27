from .elements import UmlPrimitive

class Resolver:

    def __init__(self, model):

        self.model = model

    def resolve(self):

        self._resolve_attributes()

        self._resolve_generalizations()

        self._resolve_associations()

    def _resolve_attributes(self):

        for attribute in self.model.attributes.values():

            if not attribute.type_id:
                continue

            #
            # Primitive types
            #
            if "#" in attribute.type_id:

                href = attribute.type_id

                attribute.type = UmlPrimitive(
                    id=href,
                    name=href.split("#")[-1],
                    href=href
                )

                continue

            #
            # Vanlig UML type
            #
            attribute.type = self.model.find(
                attribute.type_id
            )

    def _resolve_generalizations(self):

        for cls in self.model.classes.values():

            if cls.generalization is None:
                continue

            parent = self.model.classes.get(

                cls.generalization.parent_id

            )

            cls.generalization.parent = parent

            if parent is not None:

                parent.children.append(cls)
    
    def _resolve_associations(self):

        for association in self.model.associations.values():

            association.member_ends = []

            for end_id in association.member_end_ids:

                attribute = self.model.attributes.get(
                    end_id
                )

                if attribute:
                    association.member_ends.append(
                        attribute
                    )