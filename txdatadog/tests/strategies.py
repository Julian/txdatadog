import string

from hypothesis import strategies

from txdatadog import metrics


metric_name = strategies.text(
    string.ascii_letters + string.digits + ".",
).map(lambda name: name.encode("ascii"))

metric_without_value = strategies.one_of(
    strategies.builds(Metric, name=metric_name) for Metric in [
        metrics.Counter,
        metrics.Gauge,
        metrics.Histogram,
        metrics.Set,
        metrics.Timer,
    ]
)
tag = strategies.tuples(
    strategies.text(string.ascii_letters + string.digits + ".").map(
        lambda name: name.encode("utf-8"),
    ),
    strategies.text(string.ascii_letters + string.digits + ".").map(
        lambda name: name.encode("utf-8"),
    ),
)
value = strategies.integers()


@strategies.composite
def metric(draw):
    tags = draw(strategies.sets(tag))
    return draw(metric_without_value).with_value(
        value=draw(value),
    ).with_tags(*tags)
