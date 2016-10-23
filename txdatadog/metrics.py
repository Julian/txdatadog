from cached_property import cached_property as calculated_once
from pyrsistent import pvector, v
import attr


class NoValueSpecified(Exception):
    """
    Cannot send a metric without a value.

    """


@attr.s
class _Metric(object):

    name = attr.ib()
    _type = attr.ib()
    tags = attr.ib(default=v())

    def __str__(self):
        """
        You shouldn't be trying to send me, I have no value.

        """

        raise NoValueSpecified(self)

    def with_tags(self, *tags):
        return _Metric(name=self.name, type=self._type, tags=pvector(tags))

    def with_value(self, value):
        return _ValuedMetric(
            name=self.name, type=self._type, tags=self.tags, value=value,
        )


@attr.s
class _ValuedMetric(object):

    name = attr.ib()
    value = attr.ib()
    _type = attr.ib()
    tags = attr.ib(default=v())

    def __str__(self):
        return self._bytes

    @calculated_once
    def _bytes(self):
        if self.tags:
            return "{self.name}:{self.value}|{self._type}|#{tags}".format(
                self=self, tags=",".join(
                    "{0}:{1}".format(name, tag) for name, tag in self.tags,
                ),
            )
        return "{self.name}:{self.value}|{self._type}".format(self=self)

    def with_tags(self, *tags):
        return attr.assoc(self, tags=self.tags.extend(tags))


def Counter(name):
    return _Metric(name=name, type="c")


def Increment(name, by=1):
    return Counter(name=name).with_value(value=by)


def Gauge(name):
    return _Metric(name=name, type="g")


def Histogram(name):
    return _Metric(name=name, type="h")


def Set(name):
    return _Metric(name=name, type="s")


def Timer(name):
    return _Metric(name=name, type="ms")
