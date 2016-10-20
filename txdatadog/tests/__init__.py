import os

from hypothesis import HealthCheck, settings


settings.register_profile(
    "coverage", settings(
        max_examples=1, suppress_health_check=[HealthCheck.too_slow],
    ),
)
settings.register_profile("deep", settings(max_examples=2000))
settings.load_profile(os.environ.get("HYPOTHESIS_PROFILE", "default"))
