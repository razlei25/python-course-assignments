"""
Calculation-only module for shape areas.

Provides:
- polygon_area(n, s): area of a regular (equilateral) polygon with n sides of length s
- circle_area(r): area of a circle with radius r

This file contains only calculation logic and validation via exceptions.
"""
from typing import Union
from circle_area import area
import math


def polygon_area(n: int, s: Union[int, float]) -> float:
    """
    Calculate area of a regular polygon.
    Args:
        n: number of sides (must be integer > 2)
        s: side length (must be positive)
    Returns:
        area as float
    Raises:
        ValueError on invalid input
    """
    if not isinstance(n, int):
        raise ValueError("Number of sides must be an integer.")
    if n <= 2:
        raise ValueError("Number of sides must be greater than 2.")
    if s <= 0:
        raise ValueError("Side length must be positive.")
    return (n * (s ** 2)) / (4 * math.tan(math.pi / n))


def circle_area(r: Union[int, float]) -> float:
    """
    Calculate area of a circle.
    Args:
        r: radius (must be positive)
    Returns:
        area as float
    Raises:
        ValueError on invalid input
    """
    if r <= 0:
        raise ValueError("Radius must be positive.")
    return math.pi * (r ** 2)