#!/usr/bin/env python
# coding: utf-8
import random
import operator


class BayesNode(object):
    def __init__(self, var, parents, cpt):
        self.var = var
        self.parents = parents
        self.cpt = cpt
        self.children = []

    def prob_given_parents(self, value, event):
        """Return the conditional probability, the parent values are in event.

        :param value:
        :param event: {}
        :return:
        """
        parent_values = []
        for parent in self.parents:
            parent_values.append(event[parent.var])
        prob = self.cpt[tuple(parent_values)]
        return prob if value else 1 - prob


class BayesNet(object):
    def __init__(self, nodes):
        self.vars = {}
        for var, parent_vars, cpt in nodes:
            parents = [self.vars[parent_var] for parent_var in parent_vars]
            node = BayesNode(var, parents, cpt)
            for parent in parents:
                parent.children.append(node)
            self.vars[node.var] = node

    def __getitem__(self, var):
        return self.vars[var]

T = True
F = False
VAR_VALUES = [T, F]


def zero_prob_distribution():
    return {T: .0, F: .0}


def random_choice(seq):
    return random.choice(seq)


def sample_given_prob_distribution(prob_distribution):
    """Return sample value given probability distribution.

    :param prob_distribution: {}
    :return:
    """
    return prob_distribution[T] > random.uniform(0., 1.)


def gibbs_ask(query_var, event, bayes_net, sample_num):
    """Return conditional probability distribution of query_var using Gibbs sampling.

    :param query_var:
    :param event:
    :param bayes_net:
    :param sample_num:
    :return:
    """
    prob_distribution = zero_prob_distribution()
    non_evidence_vars = [var for var in bayes_net.vars if var not in event]
    # initialize state, values of evidence variables are in event
    state = dict(event)
    # initialize state, values of non-evidence variables are set randomly
    for non_evidence_var in non_evidence_vars:
        state[non_evidence_var] = random_choice(VAR_VALUES)
    for j in xrange(sample_num):
        for non_evidence_var in non_evidence_vars:
            # flip the value of non_evidence_var
            state[non_evidence_var] = sample_given_prob_distribution(
                prob_distribution_given_markov_blanket(
                    non_evidence_var, state, bayes_net))
            prob_distribution[state[query_var]] += 1.
    return normalize(prob_distribution)


def normalize(prob_distribution):
    """Return normalized probability distribution.

    >>> normalize({T: 90, F: 10})
    {False: 0.1, True: 0.9}

    :param prob_distribution:
    :return:
    """
    total = sum(prob_distribution.values())
    result = zero_prob_distribution()
    for value, prob in prob_distribution.iteritems():
        result[value] = float(prob) / total
    return result


def product(numbers):
    """Return the product of numbers.

    >>> product(range(1, 6))
    120

    :param numbers: sequence
    :return:
    """
    return reduce(operator.mul, numbers, 1)


def prob_distribution_given_markov_blanket(var, event, bayes_net):
    """Return the probability of var given its Markov blanket.

    :param var:
    :param event:
    :param bayes_net:
    :return:
    """
    prob_distribution = zero_prob_distribution()
    var_node = bayes_net[var]
    state = dict(event)
    for var_value in VAR_VALUES:
        state[var] = var_value
        # the probability of a variable given its Markov blanket is proportional
        # to the probability of the variable given its parents times the
        # probability of each child given its respective parents
        prob_distribution[var_value] = var_node.prob_given_parents(var_value, event) * product(
            [child.prob_given_parents(state[child.var], state)
             for child in var_node.children])
    return normalize(prob_distribution)


def generate_wet_grass_net():
    wet_grass_net = BayesNet([
            ('Cloudy', (), {(): .5}),
            ('Sprinkler', ('Cloudy',), {(T,): .1, (F,): .5}),
            ('Rain', ('Cloudy',), {(T,): .8, (F,): .2}),
            ('WetGrass', ('Sprinkler', 'Rain'), {
                (T, T): .99, (T, F): .9, (F, T): .9, (F, F): .0})])
    return wet_grass_net


def main():
    wet_grass_net = generate_wet_grass_net()
    print gibbs_ask('Rain', {'Sprinkler': T, 'WetGrass': T}, wet_grass_net, 50000)

if __name__ == '__main__':
    main()
