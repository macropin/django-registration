import sys

import six

from django.test import TestCase

from ..sixfill import get_six
from ..sixfill import nowrap
from ..sixfill import python_2_unicode_compatible


class SixDynamicPolyfillTestCase(TestCase):
    def test_python_2_unicode_compatible(self):
        """
        Test that enusres `python_2_unicode_compatible` is defined
        """
        self.assertIsNotNone(python_2_unicode_compatible)

    def test_get_six(self):
        """
        Test that enusres `get_six()` returns the same thing as `import six`
        """
        self.assertIs(get_six(), six)

    def test_nowrap_does_not_wrap(self):
        """
        Test that enusres `nowrap` will return the unwrapped function
        """
        def unwrapped():
            return
        wrapped = nowrap(unwrapped)
        self.assertIs(wrapped, unwrapped)

    def test_python_2_unicode_compatible_defined_in_polyfill_is_the_right_one(self):
        """
        Test that enusres `python_2_unicode_compatible` found in six polyfill
        contains the right implementation for this python interpreter
        """
        if sys.version_info.major == 2:
            self.assertIs(python_2_unicode_compatible, six.python_2_unicode_compatible)
        else:
            self.assertIs(python_2_unicode_compatible, nowrap)
