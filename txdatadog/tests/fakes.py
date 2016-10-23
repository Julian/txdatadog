import ast

from pyrsistent import pvector
from twisted.internet.interfaces import IUDPTransport
from twisted.test.proto_helpers import FakeDatagramTransport
from zope.interface import implementer
import attr

from txdatadog.client import DogStatxD
from txdatadog.metrics import _ValuedMetric


@implementer(IUDPTransport)
class _ConnectableFakeDatagramTransport(FakeDatagramTransport):
    """
    A fake datagram transport that allows (null) connection attempts.

    These are done by things trying to do connected UDP.

    """

    connected = False

    def connect(self, host, port):
        """
        Do nothing.

        """

        self.connected = True


@attr.s
class Server(object):
    """
    A DogStatsD server.

    """

    _transports = attr.ib(default=pvector())

    @property
    def metrics(self):
        """
        The metrics that have been received so far.

        """

        for transport in self._transports:
            for metric in _deserialize(data for data, _ in transport.written):
                yield metric

    def dogstatxd(self):
        """
        Produce a client that will send metrics to this server.

        """

        transport = _ConnectableFakeDatagramTransport()

        client = DogStatxD()
        client.makeConnection(transport)

        self._transports = self._transports.append(transport)

        return client


def _deserialize(metric_datagrams):
    for metric in metric_datagrams:
        name, rest = metric.split(":", 1)
        value, rest = rest.split("|", 1)
        type_code, _, rest = rest.partition("|#")
        tags = pvector(
            tuple(tag.split(":", 1)) for tag in rest.split(",") if tag,
        )
        yield _ValuedMetric(
            name=name,
            value=ast.literal_eval(value),
            type=type_code,
            tags=tags,
        )
