#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vi:expandtab:tabstop=4 shiftwidth=4 textwidth=79

import django

# https://docs.djangoproject.com/en/1.10/releases/1.10/#using-user-is-authenticated-and-user-is-anonymous-as-methods

if django.VERSION < (1, 10):

    def is_authenticated(user_instance):
        return user_instance.is_authenticated()

else:

    def is_authenticated(user_instance):
        return user_instance.is_authenticated
