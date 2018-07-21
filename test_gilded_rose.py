# -*- coding: utf-8 -*-
from copy import deepcopy

import unittest

from gilded_rose import Item, GildedRose
from data import items


class GildedRoseTest(unittest.TestCase):

    @property
    def all_items(self):
        return items

    @property
    def regular_items(self):
        return [item
                for item in items
                if item.name.split(' ')[0].lower() not in (
                    'aged', 'conjured', 'backstage', 'sulfuras,'
                )]

    @property
    def aged_items(self):
        return [item
                for item in items
                if item.name.split(' ')[0].lower() == 'aged']

    @property
    def sulfuras_items(self):
        return [item
                for item in items
                if item.name.split(' ')[0].lower() == 'sulfuras,']

    @property
    def conjured_items(self):
        return [item
                for item in items
                if item.name.split(' ')[0].lower() == 'conjured']

    @property
    def non_sulfuras_items(self):
        return [item
                for item in items
                if item not in self.sulfuras_items]

    def get_attr_diff(self, items, attr='quality', count=1):
        original = [getattr(item, attr)
                    for item in items]

        gr = GildedRose(items)
        for i in range(count):
            gr.update_quality()

        result = [getattr(item, attr)
                  for item in items]

        return zip(original, result, items)

    def _perform_update_test(self, items_prop, attr='quality', count=1, expected_decrease=1):
        item_set = deepcopy(getattr(self, items_prop))
        results = self.get_attr_diff(item_set, attr=attr, count=count)
        for item in results:
            # result should be original - expected_decrease
            computed_expected = item[0] - expected_decrease

            # quality is never negative
            if (attr == 'quality'):
                computed_expected = max(0, computed_expected)

            self.assertEqual(computed_expected, item[1],
                             '{} != {} => Failing for {} ({}): {}'.format(computed_expected, item[1],
                                                                          attr, count, item[2]))

    def test_quality_regular(self):
        self._perform_update_test('regular_items')

    def test_sell_in_decreases_for_non_sulfuras(self):
        self._perform_update_test('non_sulfuras_items', 'sell_in')


if __name__ == '__main__':
    unittest.main()
