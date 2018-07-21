# -*- coding: utf-8 -*-
import re


class GildedRose(object):

    def _get_specialised_item_for(self, item):
        item_type = re.match(r'\w+', item.name)
        if item_type is None:
            return item
        klass = globals().get('{}Item'.format(item_type.group()), Item)
        return klass(item.name, item.sell_in, item.quality)

    def __init__(self, items):
        self.items = [self._get_specialised_item_for(item) for item in items]

    def update_quality(self):
        for item in self.items:
            item.update_quality()
            # if item.name != "Aged Brie" and item.name != "Backstage passes to a TAFKAL80ETC concert":
            #     if item.quality > 0:
            #         if item.name != "Sulfuras, Hand of Ragnaros":
            #             item.quality = item.quality - 1
            # else:
            #     if item.quality < 50:
            #         item.quality = item.quality + 1
            #         if item.name == "Backstage passes to a TAFKAL80ETC concert":
            #             if item.sell_in < 11:
            #                 if item.quality < 50:
            #                     item.quality = item.quality + 1
            #             if item.sell_in < 6:
            #                 if item.quality < 50:
            #                     item.quality = item.quality + 1
            # if item.name != "Sulfuras, Hand of Ragnaros":
            #     item.sell_in = item.sell_in - 1
            # if item.sell_in < 0:
            #     if item.name != "Aged Brie":
            #         if item.name != "Backstage passes to a TAFKAL80ETC concert":
            #             if item.quality > 0:
            #                 if item.name != "Sulfuras, Hand of Ragnaros":
            #                     item.quality = item.quality - 1
            #         else:
            #             item.quality = item.quality - item.quality
            #     else:
            #         if item.quality < 50:
            #             item.quality = item.quality + 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

    decrement = 1

    @property
    def rate(self):
        if self.sell_in < 0:
            return 2
        return 1

    def update_quality(self):
        self.sell_in -= 1
        self.quality -= self.decrement * self.rate

        if self.quality < 0:
            self.quality = 0


class AgedItem(Item):
    decrement = -1
