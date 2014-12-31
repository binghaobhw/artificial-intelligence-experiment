#!/usr/bin/env python
# coding: utf-8
from unittest import TestCase

from eight_puzzle import Board, distance


class TestBoard(TestCase):
    def test_extend(self):
        expected = [Board([1, 0, 2, 3, 4, 5, 6, 7, 8]),
                    Board([3, 1, 2, 0, 4, 5, 6, 7, 8])]
        board = Board(range(9))
        result = board.extend()
        self.assertTrue(result == expected)


class TestCost(TestCase):
    def test_cost(self):
        expected = 1
        result = distance(Board(range(9)), Board([4, 1, 2, 3, 0, 5, 6, 7, 8]))
        self.assertTrue(result == expected)


class TestDistance(TestCase):
    a = Board([2, 0, 3,
               1, 8, 4,
               7, 6, 5])
    b = Board([2, 8, 3,
               0, 1, 4,
               7, 6, 5])

    def test_distance(self):
        expected = 4
        result = distance(self.a, self.b)
        self.assertTrue(result == expected)