# -*- coding: utf-8 -*-
#
from __future__ import division, print_function

import numpy


def hist(a, orientation='vertical', max_width=40, bins=20):
    if orientation == 'vertical':
        hist_vertical(a)
    else:
        assert orientation == 'horizontal', \
            'Unknown orientation \'{}\''.format(orientation)
        hist_horizontal(a, max_width=40, bins=20)
    return


def hist_horizontal(a, max_width=40, bins=20, bar_width=1,
                    show_bin_edges=True, show_counts=True):
    # ax2.hist(a, bins=30, orientation="horizontal")
    counts, bin_edges = numpy.histogram(a, bins=bins)
    averages = (bin_edges[:-1] + bin_edges[1:]) / 2

    matrix = _get_matrix_of_eighths(counts, max_width, bar_width)

    chars = [
        ' ',
        '\u258f', '\u258e', '\u258d', '\u258c', '\u258b', '\u258a', '\u2589',
        '\u2588'
        ]

    fmt = []
    if show_bin_edges:
        efmt = '{:+.2e}'
        fmt.append(efmt + ' - ' + efmt)
    if show_counts:
        cfmt = '{{:{}d}}'.format(numpy.max([len(str(c)) for c in counts]))
        fmt.append('[' + cfmt + ']')
    fmt.append('{}')
    fmt = '  '.join(fmt)

    for k, (counts, row) in enumerate(zip(counts, matrix)):
        data = []
        if show_bin_edges:
            data.append(bin_edges[k])
            data.append(bin_edges[k+1])
        if show_counts:
            data.append(counts)
        data.append(''.join(chars[item] for item in row))
        print(fmt.format(*data))

    return


def hist_vertical(a, bins=30, max_height=10, bar_width=2):
    # ax2.hist(a, bins=30, orientation="horizontal")
    counts, bin_edges = numpy.histogram(a, bins=bins)

    matrix = _get_matrix_of_eighths(counts, max_height, bar_width)

    chars = [
        ' ',
        '\u2581', '\u2582', '\u2583', '\u2584', '\u2585', '\u2586', '\u2587',
        '\u2588'
        ]

    # print text matrix
    for row in matrix:
        print(''.join(chars[item] for item in row))

    return


def _get_matrix_of_eighths(counts, max_size, bar_width):
    max_count = numpy.max(counts)

    # translate to eighths of a textbox
    eighths = numpy.array([
        int(round(count / max_count * max_size * 8))
        for count in counts
        ])

    # prepare matrix
    matrix = numpy.zeros((len(eighths), max_size), dtype=int)
    for k, eighth in enumerate(eighths):
        num_full_blocks = eighth // 8
        remainder = eighth % 8
        matrix[k, :num_full_blocks] = 8
        if remainder > 0:
            matrix[k, num_full_blocks] = remainder

    # Account for bar width
    matrix = numpy.repeat(
            matrix, numpy.full(matrix.shape[0], bar_width), axis=0
            )
    return matrix
