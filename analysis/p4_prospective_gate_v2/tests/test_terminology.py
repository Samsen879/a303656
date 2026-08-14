#!/usr/bin/env python3
import unittest


class TerminologyTests(unittest.TestCase):
    def test_required_predicates_are_distinct(self):
        terms = {"design_novel_class", "design_novel_full_mask", "design_novel_live_projection", "historically_exposed_class", "integer_unseen_any_recorded_evaluation", "integer_unseen_exact_T", "selection_T_blind"}
        self.assertEqual(len(terms), 7)


if __name__ == "__main__": unittest.main()
