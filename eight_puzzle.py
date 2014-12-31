#!/usr/bin/env python
# coding: utf-8
from collections import deque
import heapq


class Board(object):
    def __init__(self, numbers):
        self.numbers = numbers

    def extend(self):
        boards = []
        current_zero_position = self.numbers.index(0)
        next_zero_positions = map(lambda x: x+current_zero_position, [1, 3, -1, -3])
        for i, next_zero_position in enumerate(next_zero_positions):
            if (i == 0 and current_zero_position % 3 != 2) or \
                    (i == 1 and current_zero_position < 6) or \
                    (i == 2 and current_zero_position % 3 != 0) or \
                    (i == 3 and current_zero_position > 2):
                next_numbers = list(self.numbers)
                next_numbers[current_zero_position], next_numbers[next_zero_position] = \
                    next_numbers[next_zero_position], next_numbers[current_zero_position]
                boards.append(Board(next_numbers))
        return boards

    def __eq__(self, other):
        return self.numbers == other.numbers

    def __lt__(self, other):
        return f_score[self] < f_score[other]

    def __hash__(self):
        """Required for operations on hashed collections."""
        return reduce(lambda x, y: 10 * x + y, self.numbers)

    def __str__(self):
        return '\n'.join(['{} {} {}'.format(self.numbers[i], self.numbers[i+1], self.numbers[i+2]) for i in [0, 3, 6]])

    def __repr__(self):
        return '<Board({})>'.format(self.numbers)


def distance(a, b):
    distance_ = 0
    for number in range(9):
        x_distance = abs(a.numbers.index(number) % 3 - b.numbers.index(number) % 3)
        y_distance = abs(a.numbers.index(number) / 3 - b.numbers.index(number) / 3)
        distance_ += x_distance + y_distance
    return distance_


def heuristic(current, target):
    return distance(current, target)


class MinHeap(object):
    def __init__(self):
        self.elements = []

    def put(self, item):
        heapq.heappush(self.elements, item)

    def get(self):
        return heapq.heappop(self.elements)

    def __len__(self):
        return len(self.elements)

    def __contains__(self, item):
        return item in self.elements


g_score = {}
f_score = {}


def a_star_search(initial_node, target_node):
    came_from = {}
    open_set = MinHeap()
    open_set.put(initial_node)
    came_from[initial_node] = None
    closed_set = set()

    g_score[initial_node] = 0
    f_score[initial_node] = g_score[initial_node] + heuristic(initial_node, target_node)

    while open_set:
        current = open_set.get()
        if current == target_node:
            break
        closed_set.add(current)
        for next_ in current.extend():
            if next_ in closed_set:
                continue
            tentative_g_score = g_score[current] + 1
            if next_ not in open_set or tentative_g_score < g_score[next_]:
                came_from[next_] = current
                g_score[next_] = tentative_g_score
                f_score[next_] = g_score[next_] + heuristic(next_, target_node)
                if next_ not in open_set:
                    open_set.put(next_)
    return came_from, g_score


def main():
    # source_ = Board([2, 8, 3, 1, 0, 4, 7, 6, 5])
    source_ = Board([0, 1, 2, 3, 4, 5, 6, 7, 8])
    target_ = Board([1, 2, 3, 8, 0, 4, 7, 6, 5])
    came_from, cost_so_far_ = a_star_search(source_, target_)
    if target_ not in came_from:
        print 'No solution'
    else:
        stack = deque()
        current = target_
        while current:
            stack.append(current)
            current = came_from[current]
        print stack.pop()
        while stack:
            print '  ↓'
            print stack.pop()


if __name__ == '__main__':
    main()