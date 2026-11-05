import unittest

from compare import compare, ADD, UPDATE, DELETE


class CompareTests(unittest.TestCase):
    def test_add_simple(self):
        self.assertEqual(compare(ADD, {"a": 1, "b": 2}, {"a": 1}), {"b": 2})

    def test_add_nested(self):
        source = {"a": 1, "b": {"x": 1, "y": 2}}
        target = {"a": 1, "b": {"x": 1}}
        self.assertEqual(compare(ADD, source, target), {"b": {"y": 2}})

    def test_add_nothing(self):
        self.assertEqual(compare(ADD, {"a": 1}, {"a": 1}), {})

    def test_add_list(self):
        self.assertEqual(compare(ADD, [1, 2, 3], [1, 3]), [2])

    def test_update_simple(self):
        self.assertEqual(
            compare(UPDATE, {"a": 1, "b": 5}, {"a": 1, "b": 2}),
            {"b": {"from": 2, "to": 5}},
        )

    def test_update_nested(self):
        source = {"a": {"x": 1, "y": 9}}
        target = {"a": {"x": 1, "y": 2}}
        self.assertEqual(compare(UPDATE, source, target), {"a": {"y": {"from": 2, "to": 9}}})

    def test_update_nothing(self):
        self.assertEqual(compare(UPDATE, {"a": 1}, {"a": 1}), {})

    def test_update_ignores_missing_keys(self):
        self.assertEqual(compare(UPDATE, {"a": 1, "b": 2}, {"a": 1}), {})

    def test_delete_simple(self):
        self.assertEqual(compare(DELETE, {"a": 1}, {"a": 1, "b": 2}), {"b": 2})

    def test_delete_nested(self):
        source = {"a": {"x": 1}}
        target = {"a": {"x": 1, "y": 2}}
        self.assertEqual(compare(DELETE, source, target), {"a": {"y": 2}})

    def test_delete_list(self):
        self.assertEqual(compare(DELETE, [1, 3], [1, 2, 3]), [2])

    def test_invalid_mode(self):
        with self.assertRaises(ValueError):
            compare("unknown", {}, {})


if __name__ == "__main__":
    unittest.main()
