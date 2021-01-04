#!/usr/bin/python

import csv
import cairo

INCHES_TO_POINTS = 72

FROM_ADDR = ('Evan + Meena',
             '[elided]',
             'San Francisco, CA 94110')
FONT_SIZE_FROM = 15
FONT_SIZE_TO = 25
MARGIN = 0.25


def write_envelopes(out, from_addr, to_addrs):
    """Write the Enveolope PDF File"""
    surface = cairo.PDFSurface(out,
                               7.25 * INCHES_TO_POINTS,
                               5.25 * INCHES_TO_POINTS)
    cr = cairo.Context(surface)
    cr.select_font_face('serif')

    for to_addr in to_addrs:
        cr.set_font_size(FONT_SIZE_FROM)
        for i, line in enumerate(from_addr):
            cr.move_to(MARGIN * INCHES_TO_POINTS,
                       (MARGIN * INCHES_TO_POINTS) + FONT_SIZE_FROM + (FONT_SIZE_FROM * i))
            cr.show_text(line)

        cr.set_font_size(FONT_SIZE_TO)
        for i, line in enumerate(to_addr):
            cr.move_to(2 * INCHES_TO_POINTS,
                       (2.25 * INCHES_TO_POINTS) + FONT_SIZE_TO + (FONT_SIZE_TO * i))
            cr.show_text(line)
        cr.show_page()

    surface.flush()
    surface.finish()


def load_csv(filename):
    """
    This logic is necessarily use case specific specific, but for
    our list we just have three columns of addresses and an optional
    fourth column that says "yes" for addresses we wanted printed.
    """
    with open(filename) as openfile:
        for i, row in enumerate(csv.reader(openfile)):
            if i == 0:
                continue
            should_print = ''
            if len(row) > 3:
                should_print = row[3].strip()[0]
            if should_print != 'y':
                continue
            yield row[0:3]


if __name__ == '__main__':
    INFILE = 'test.csv'
    OUTFILE = 'test.pdf'
    with open(OUTFILE, 'w') as f:
        write_envelopes(f, FROM_ADDR, list(load_csv(INFILE)))
    print('wrote %s.' % OUTFILE)
