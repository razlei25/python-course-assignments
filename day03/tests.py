import sys
import types
import math
import unittest
from unittest import mock

# Ensure a minimal 'circle_area' module is present so importing the target module won't fail
# (some versions of shape_area_calculator_clean import from circle_area at module import time).
if 'circle_area' not in sys.modules:
    dummy = types.ModuleType('circle_area')
    dummy.area = lambda r: math.pi * r * r
    sys.modules['circle_area'] = dummy

import shape_area_calculator_clean as sac


class TestShapeCalculations(unittest.TestCase):
    # Polygon (regular equilateral polygon) tests
    def test_polygon_area_triangle_side1(self):
        expected = (3 * (1 ** 2)) / (4 * math.tan(math.pi / 3))
        self.assertAlmostEqual(sac.polygon_area(3, 1), expected, places=9)

    def test_polygon_area_square_side2(self):
        # square with side 2 -> area 4 (for regular polygon formula it should match)
        expected = (4 * (2 ** 2)) / (4 * math.tan(math.pi / 4))
        self.assertAlmostEqual(sac.polygon_area(4, 2), expected, places=9)

    def test_polygon_area_invalid_sides_not_int(self):
        with self.assertRaises(ValueError):
            sac.polygon_area(3.5, 1)

    def test_polygon_area_invalid_sides_too_small(self):
        with self.assertRaises(ValueError):
            sac.polygon_area(2, 1)

    def test_polygon_area_invalid_side_length_nonpositive(self):
        with self.assertRaises(ValueError):
            sac.polygon_area(3, 0)

    # Circle tests
    def test_circle_area_valid(self):
        r = 2.5
        expected = math.pi * (r ** 2)
        self.assertAlmostEqual(sac.circle_area(r), expected, places=9)

    def test_circle_area_zero_radius_raises(self):
        with self.assertRaises(ValueError):
            sac.circle_area(0)

    def test_circle_area_negative_radius_raises(self):
        with self.assertRaises(ValueError):
            sac.circle_area(-1.0)

    # If the module under test dynamically imports the third-party package (some versions do),
    # ensure behavior when import fails is sensible. We patch importlib.import_module to raise ImportError
    # and call the function only if the implementation performs a dynamic import.
    def test_circle_area_missing_dependency_behaviour(self):
        # If the implementation dynamically imports and raises RuntimeError on missing dep,
        # we assert that behavior. If not, the function should still compute area.
        import importlib

        # Patch importlib.import_module to raise ImportError for this test
        with mock.patch('importlib.import_module', side_effect=ImportError):
            # Call circle_area with a positive radius:
            try:
                result = sac.circle_area(1.0)
            except RuntimeError as exc:
                # Acceptable behavior when dependency is required but missing
                self.assertIn("Missing dependency", str(exc))
            except Exception as exc:
                # Any other exception is unexpected
                self.fail(f"Unexpected exception raised: {exc}")
            else:
                # If no exception, result should match math.pi * r^2
                self.assertAlmostEqual(result, math.pi * (1.0 ** 2), places=9)


if __name__ == "__main__":
    unittest.main()