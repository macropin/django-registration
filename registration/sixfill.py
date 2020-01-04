import importlib
import sys

python_2_unicode_compatible = None


def nowrap(f, *args, **kwargs):
    return f


def get_six():
    return importlib.import_module('six')


if sys.version_info == (2,):
    python_2_unicode_compatible = get_six().python_2_unicode_compatible
else:
    python_2_unicode_compatible = nowrap
