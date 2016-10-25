from unittest import TestCase

from txdatadog import metrics


class TestMetric(TestCase):
    # http://docs.datadoghq.com/guides/dogstatsd/#metrics-1
    def test_counter(self):
        counter = metrics.Counter(name="page.views").with_value(value=12)
        self.assertEqual(bytes(counter), b"page.views:12|c")

    def test_counter_with_tags(self):
        counter = metrics.Counter(name="views").with_tags(
            ("a", "b"),
        ).with_value(value=12).with_tags(
            ("foo", "bar"), ("baz", "quux"),
        ).with_tags(("spam", "ביצים"))
        self.assertEqual(
            bytes(counter), b"views:12|c|#a:b,foo:bar,baz:quux,spam:ביצים",
        )

    def test_increment(self):
        increment = metrics.Increment(name="foo")
        self.assertEqual(increment, metrics.Counter(name="foo").with_value(1))

    def test_increment_with_tags(self):
        counter = metrics.Increment(name="views").with_tags(
            ("a", "b"),
        ).with_tags(("foo", "bar")).with_tags(("spam", "ביצים"))
        self.assertEqual(bytes(counter), b"views:1|c|#a:b,foo:bar,spam:ביצים")

    def test_gauge(self):
        gauge = metrics.Gauge(name="fuel.level").with_value(value=0.5)
        self.assertEqual(bytes(gauge), b"fuel.level:0.5|g")

    def test_gauge_with_tags(self):
        gauge = metrics.Gauge(name="fuel.level").with_tags(
            ("a", "b"),
        ).with_value(value=12.0).with_tags(
            ("foo", "bar"), ("baz", "quux"),
        ).with_tags(("spam", "ביצים"))
        self.assertEqual(
            bytes(gauge),
            b"fuel.level:12.0|g|#a:b,foo:bar,baz:quux,spam:ביצים",
        )

    def test_histogram(self):
        histogram = metrics.Histogram(name="song.length").with_value(value=240)
        self.assertEqual(bytes(histogram), b"song.length:240|h")

    def test_histogram_with_tags(self):
        histogram = metrics.Histogram(name="song.length").with_tags(
            ("a", "b"),
        ).with_value(value=240.0).with_tags(
            ("foo", "bar"), ("baz", "quux"),
        ).with_tags(("spam", "ביצים"))
        self.assertEqual(
            bytes(histogram),
            b"song.length:240.0|h|#a:b,foo:bar,baz:quux,spam:ביצים",
        )

    def test_set(self):
        # FIXME: I can't tell if this can be a string. If it can, this gets a
        #        bit more complicated (because of str(float) being stupid).
        #        The DD docs say that `value` is a number, but this kind of
        #        metric seems kind of useless unless it takes a str.
        set = metrics.Set(name="users.uniques").with_value(value=1234)
        self.assertEqual(bytes(set), b"users.uniques:1234|s")

    def test_set_with_tags(self):
        set = metrics.Set(name="users.uniques").with_tags(
            ("a", "b"),
        ).with_value(value=240.0).with_tags(
            ("foo", "bar"), ("baz", "quux"),
        ).with_tags(("spam", "ביצים"))
        self.assertEqual(
            bytes(set),
            b"users.uniques:240.0|s|#a:b,foo:bar,baz:quux,spam:ביצים",
        )

    def test_cannot_send_a_metric_without_a_value(self):
        metric = metrics.Histogram(name="song.length").with_tags(
            ("foo", "bar"),
        )
        with self.assertRaises(metrics.NoValueSpecified):
            bytes(metric)
