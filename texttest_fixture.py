# -*- coding: utf-8 -*-
from __future__ import print_function

from gilded_rose import *
from data import items


if __name__ == "__main__":
    print ("OMGHAI!")

    days = 2
    import sys
    if len(sys.argv) > 1:
        days = int(sys.argv[1]) + 1
    gr = GildedRose(items)
    for day in range(days):
        print("-------- day %s --------" % day)
        print("name, sellIn, quality")
        for item in gr.items:
            print(item)
        print("")
        gr.update_quality()
