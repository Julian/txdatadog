from functools import partial

from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol
import attr


@attr.s
class DogStatxD(DatagramProtocol, object):

    host = attr.ib(default="127.0.0.1")
    port = attr.ib(default=8125)

    @classmethod
    def connected(cls, reactor=reactor, **kwargs):
        """
        Return a connected instance.

        """

        statsd = cls(**kwargs)
        reactor.listenUDP(0, statsd)
        return statsd

    def startProtocol(self):
        self.transport.connect(self.host, self.port)

    def send(self, metric):
        """
        Send the given metric.

        """

        self.transport.write(bytes(metric))

    def sender(self, metric):
        """
        Return a thunk that can be used to repeatedly send the given metric.

        """

        return partial(self.transport.write, bytes(metric))
