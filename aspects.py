#!/usr/bin/env python
# Copyright (c) 2013, Zygmunt Krynicki, All rights reserved.
# See COPYING for license information.

"""
aspect -- aspect programming for python
=======================================

"""

from __future__ import division, unicode_literals, print_function

import sys
from unittest import TestCase, main

__all__ = ['Aspect']


class AspectType(type):
    """
    Type of all the Aspect classes.

    Implements special version of __rdiv__ to support Klass/Aspect[/Aspect...]
    syntax to express sets of aspects that affect a particular class.
    """

    def __rdiv__(self, other):
        assert isinstance(self, type) and issubclass(self, Aspect)
        if isinstance(other, Aspect):
            return Aspect(other.cls, other.aspect_set | set([self]))
        elif isinstance(other, type):
            return Aspect(other, set([self]))
        else:
            return NotImplemented

    __rtruediv__ = __rdiv__


class Aspect(AspectType(str("NewBase"), (object,), {})):

    def __init__(self, cls, aspect_set):
        self.cls = cls
        self.aspect_set = aspect_set

    def __repr__(self):
        return "{}/{}".format(
            self.cls.__name__,
            "/".join(sorted([aspect.__name__ for aspect in self.aspect_set])))


class AspectTests(TestCase):

    def setUp(self):
        """
        setup common data for all unit tests
        """

        class TestAspect(Aspect):
            pass

        class AnotherTestAspect(Aspect):
            pass

        class Klass(object):
            pass
        self.TestAspect = TestAspect
        self.AnotherTestAspect = AnotherTestAspect
        self.Klass = Klass

    def test_div_syntax(self):
        """
        verify that Klass/AnyAspectClass syntax creates a new Aspect
        instance with appropriate data inside
        """
        aspect = self.Klass / self.TestAspect
        # aspect should be an Aspect instance
        self.assertIsInstance(aspect, Aspect)
        # aspect.cls should be Klass
        self.assertIs(aspect.cls, self.Klass)
        # aspect.aspect_set should be a set containing TestAspect
        self.assertEqual(aspect.aspect_set, set([self.TestAspect]))

    def test_more_div(self):
        aspect = self.Klass / self.TestAspect / self.AnotherTestAspect
        # aspect should be an Aspect instance
        self.assertIsInstance(aspect, Aspect)
        # aspect.cls should be Klass
        self.assertIs(aspect.cls, self.Klass)
        # aspect.aspect_set should be a set containing TestAspect
        self.assertEqual(
            aspect.aspect_set, set([self.TestAspect, self.AnotherTestAspect]))

    def test_repr(self):
        """
        verify how the repr() function works
        """
        aspect1 = self.Klass / self.TestAspect
        self.assertEqual(repr(aspect1), "Klass/TestAspect")
        aspect2 = self.Klass / self.TestAspect / self.AnotherTestAspect
        self.assertEqual(repr(aspect2), "Klass/AnotherTestAspect/TestAspect")


if __name__ == "__main__":
    main()
