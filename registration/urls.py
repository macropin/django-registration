import warnings

warnings.warn("Using include('registration.urls') is deprecated; use include('registration.backends.default.urls') instead",
              PendingDeprecationWarning)

from registration.backends.default.urls import *
