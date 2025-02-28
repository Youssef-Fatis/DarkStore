from typing import List
from API.modifier import Modifier


class Variant:
    def __init__(self, name) -> None:
        self.name = name
        self.modifiers: List[Modifier] = []

    def __str__(self) -> str:
        modifiers_str = ", ".join(str(modifier) for modifier in self.modifiers)
        return f"Variant(name='{self.name}', modifiers=[{modifiers_str}])"
