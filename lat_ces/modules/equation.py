"""
LAT-CES Module 011: Physical Equation & Formula Engine
Dokument: LAT-SCI-MOD-0011
"""
from typing import Callable

from lat_ces.core.dimensions import Dimension
from lat_ces.modules.quantity import PhysicalQuantity
from lat_ces.scientific.quantity.equation import Equation


class PhysicalEquation:
    """
    Predstavlja fizikalnu jednačinu koja prihvata ulazne fizikalne veličine,
    izvršava proračun i verifikuje da dobijena dimenzija odgovara očekivanoj.

    ``equation`` is the canonical immutable equation identity. ``name`` is
    retained as a compatibility alias to the same expression string.
    """

    def __init__(
        self,
        name: str,
        expected_dimension: Dimension,
        formula: Callable[..., PhysicalQuantity],
    ):
        self.equation = Equation(name)
        self.name = self.equation.expression
        self.expected_dimension = expected_dimension
        self.formula = formula

    def compute(self, **kwargs: PhysicalQuantity) -> PhysicalQuantity:
        result = self.formula(**kwargs)

        if result.dimension != self.expected_dimension:
            raise ValueError(
                f"Greška u jednačini '{self.equation.expression}': Očekivana dimenzija {self.expected_dimension}, "
                f"ali je dobijena {result.dimension}!"
            )
        return result
