# -*- coding: utf-8 -*-
import re


class GildedRose(object):

    def _get_specialised_item_for(self, item):
        item_type = re.match(r'\w+', item.name)
        klass = ItemProxy if item_type is None else \
            globals().get('{}ItemProxy'.format(item_type.group()), ItemProxy)
        return klass(item)

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


class ItemProxy(object):
    decrement = 1
    max_quality = 50

    def __init__(self, item):
        self.item = item

    def __getattr__(self, key):
        if key in ('quality', 'sell_in'):
            return getattr(self.item, key)
        return super(ItemProxy, self).__getattr__(key)

    def __setattr__(self, key, value):
        if key in ('quality', 'sell_in'):
            return setattr(self.item, key, value)
        return super(ItemProxy, self).__setattr__(key, value)

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
        if self.quality > self.max_quality:
            self.quality = 50


class AgedItemProxy(ItemProxy):
    decrement = -1


class SulfurasItemProxy(ItemProxy):

    def update_quality(self):
        pass


class BackstageItemProxy(AgedItemProxy):

    @property
    def rate(self):
        if self.sell_in < 10 and self.sell_in >= 5:
            return 2
        if self.sell_in < 5:
            return 3
        return 1

    def update_quality(self):
        if self.sell_in <= 0:
            self.sell_in -= 1
            self.quality = 0
        else:
            super(BackstageItemProxy, self).update_quality()


class ConjuredItemProxy(ItemProxy):
    decrement = 2
