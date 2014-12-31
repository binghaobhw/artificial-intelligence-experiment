#!/usr/bin/env python
# coding: utf-8
from unittest import TestCase
from wet_grass import BayesNet, T, F, normalize, zero_prob_distribution


class TestBayesNet(TestCase):
    def setUp(self):
        self.wet_grass_net = BayesNet([
            ('Cloudy', (), {(): .5}),
            ('Sprinkler', ('Cloudy',), {(T,): .1, (F,): .5}),
            ('Rain', ('Cloudy',), {(T,): .8, (F,): .2}),
            ('WetGrass', ('Sprinkler', 'Rain'), {
                (T, T): .99, (T, F): .9, (F, T): .9, (F, F): .0})])

    def test_getitem(self):
        sprinkler = self.wet_grass_net['Sprinkler']
        rain = self.wet_grass_net['Rain']
        wet_grass = self.wet_grass_net['WetGrass']
        self.assertTrue(wet_grass.parents == [sprinkler, rain])
        self.assertTrue(rain.children == [wet_grass])


class TestNormalize(TestCase):
    def setUp(self):
        self.prob_distribution = zero_prob_distribution()
        self.prob_distribution[T] = 90.
        self.prob_distribution[F] = 10.
    def test_normalize(self):
        result = normalize(self.prob_distribution)
        self.assertTrue(result[T] == .9 and result[F] == .1)
