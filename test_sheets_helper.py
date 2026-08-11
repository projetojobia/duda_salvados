import unittest

from sheets_helper import (
    FORMULA_COLUMNS,
    ProductRow,
    SheetsHelperError,
    normalize_code,
    resolve_column,
)


class SheetsHelperUnitTests(unittest.TestCase):
    def test_normalize_code(self):
        self.assertEqual(normalize_code("ds1"), "DS001")
        self.assertEqual(normalize_code("DS014"), "DS014")

    def test_normalize_code_rejects_invalid_value(self):
        with self.assertRaises(SheetsHelperError):
            normalize_code("ABC")

    def test_resolve_column_by_letter_and_label(self):
        self.assertEqual(resolve_column("T"), "T")
        self.assertEqual(resolve_column("Preco definido (R$)"), "T")
        self.assertEqual(resolve_column("Preço definido (R$)"), "T")

    def test_formula_columns_are_protected(self):
        self.assertEqual(FORMULA_COLUMNS, {"R", "U", "V", "AB"})

    def test_product_row_free_when_only_code_exists(self):
        row = ProductRow("DS005", 6, ["DS005"])
        self.assertTrue(row.is_free)

    def test_product_row_not_free_when_data_exists(self):
        row = ProductRow("DS001", 2, ["DS001", "8/8/2026"])
        self.assertFalse(row.is_free)


if __name__ == "__main__":
    unittest.main()
