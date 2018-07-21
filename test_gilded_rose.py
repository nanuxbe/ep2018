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
    def non_expired_regular_items(self):
        return [item
                for item in self.regular_items
                if item.sell_in > 0]

    @property
    def expired_regular_items(self):
        return [item
                for item in self.regular_items
                if item.sell_in <= 0]

    @property
    def aged_items(self):
        return [item
                for item in items
                if item.name.split(' ')[0].lower() == 'aged']

    @property
    def backstage_items(self):
        return [item
                for item in items
                if item.name.split(' ')[0].lower() == 'backstage']

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

    def _perform_update_test(self, items_prop, attr='quality', count=1, expected_decrease=1,
                             perform_assert=True):
        item_set = deepcopy(getattr(self, items_prop))
        results = self.get_attr_diff(item_set, attr=attr, count=count)

        if not perform_assert:
            return results

        for item in results:
            computed_expected = item[0] - expected_decrease * count

            # quality is never negative
            if (attr == 'quality'):
                computed_expected = max(0, computed_expected)

            self.assertEqual(computed_expected, item[1],
                             '{} != {} => Failing for {} ({}): {}'.format(computed_expected, item[1],
                                                                          attr, count, item[2]))

    def test_quality_regular(self):
        self._perform_update_test('non_expired_regular_items')

    def test_sell_in_decreases_for_non_sulfuras(self):
        self._perform_update_test('non_sulfuras_items', 'sell_in')

    def test_expired_regulars_decrease_twice_as_fast(self):
        self._perform_update_test('expired_regular_items', expected_decrease=2)

    def test_quality_never_negative(self):
        # 1000 is WAY over the maximum sell_in from our data, so all qualities should be at 0
        results = self._perform_update_test('all_items', count=1000, perform_assert=False)
        for item in results:
            self.assertGreaterEqual(item[1], 0, '{} is negative: {}'.format(item[1], item[2]))

    def test_quality_increases_for_aged(self):
        self._perform_update_test('aged_items', expected_decrease=-1)

    def test_quality_never_over_50(self):
        results = self._perform_update_test('aged_items', count=1000, perform_assert=False)
        for item in results:
            self.assertLessEqual(item[1], 50, '{} is more than 50: {}'.format(item[1], item[2]))

        for i in (1, 5, 10, 15):
            results = self._perform_update_test('backstage_items', count=i, perform_assert=False)
            for item in results:
                self.assertLessEqual(item[1], 50, '{} is more than 50 ({}): {}'.format(item[1], i,
                                                                                       item[2]))

    def test_sulfuras_never_change(self):
        for attr in ('quality', 'sell_in'):
            self._perform_update_test('sulfuras_items', attr=attr, expected_decrease=0)


if __name__ == '__main__':
    unittest.main()
