# -*- coding: utf-8 -*-
from copy import deepcopy

import unittest

from gilded_rose import Item, GildedRose
from data import items

class GildedRoseTest(unittest.TestCase):

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

    def get_attr_diff(self, items, attr='quality', count=1):
        original = [getattr(item, attr)
                    for item in items]

        gr = GildedRose(items)
        for i in range(count):
            gr.update_quality()

        result = [getattr(item, attr)
                  for item in items]

        return zip(original, result)

    def test_quality_regular(self):
        item_set = deepcopy(self.regular_items)
        results = self.get_attr_diff(item_set)
        for item in results:
            # result should be original - 1
            self.assertEqual(item[0], item[1] + 1)


if __name__ == '__main__':
    unittest.main()
