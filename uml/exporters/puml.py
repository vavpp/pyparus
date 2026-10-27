from pathlib import Path


class PlantUmlExporter:
    def export(self, model):


        lines = ["@startuml", ""]

        # Klasser
        for cls in sorted(model.classes.values(), key=lambda c: c.name):
            lines.append(f"class {self._safe_name(cls.name)} {{")

            for attr in getattr(cls, "attributes", []):
                attr_type = getattr(attr.type, "name", "Unknown")
                lines.append(f"  {attr.name} : {attr_type}")

            lines.append("}")
            lines.append("")

        # Enumerasjoner
        for enum in sorted(model.enumerations.values(), key=lambda e: e.name):
            lines.append(f"enum {self._safe_name(enum.name)} {{")

            for literal in getattr(enum, "literals", []):
                if hasattr(literal, "name"):
                    lines.append(f"  {literal.name}")
                else:
                    lines.append(f"  {literal}")

            lines.append("}")
            lines.append("")

        # Generaliseringer (arv)
        for cls in model.classes.values():
            parent = getattr(cls, "superclass", None)

            if parent:
                lines.append(
                    f"{self._safe_name(parent.name)} <|-- "
                    f"{self._safe_name(cls.name)}"
                )
        assoc = next(iter(model.associations.values()))



        # Assosiasjoner
        for assoc in model.associations.values():

            if len(assoc.member_ends) < 2:
                continue

            end1 = assoc.member_ends[0]
            end2 = assoc.member_ends[1]

            if end1.type is None or end2.type is None:
                continue

            source = end1.type.name
            target = end2.type.name

            lines.append(
                f"{self._safe_name(source)} -- {self._safe_name(target)}"
            )

        lines.append("")
        lines.append("@enduml")


        return "\n".join(lines)


    def _safe_name(self, name: str) -> str:
        return name.replace(" ", "_")