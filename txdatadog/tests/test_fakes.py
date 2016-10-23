from unittest import TestCase

from hypothesis import given, strategies

from txdatadog.tests import fakes
from txdatadog.tests.strategies import metric


class TestFakeStatxD(TestCase):
    @given(metrics=strategies.lists(metric()))
    def test_it_has_what_was_sent(self, metrics):
        server = fakes.Server()
        statsd = server.dogstatxd()

        for each in metrics:
            statsd.send(each)

        self.assertEqual(list(server.metrics), metrics)
