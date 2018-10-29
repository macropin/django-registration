.. _admin-approval-backend:
.. module:: registration.backends.admin_approval

The admin approval backend
==========================

As an alternative to :ref:`the default backend <default-backend>`, and
an example of writing alternate workflows, |project| bundles
an approval-needed registration system in
``registration.backend.admin_approval``. This backend's workflow is similar to
the default with one extra step of approval from an admin. Specifically the
steps are the following:

1. A user signs up by filling out a registration form.

2. The user confirms the account by following the link sent to the email
   address supplied during registration.

3. An admin receives an email with a link that will approve the user
   registration.

4. When the admin approves the request, the user receives an email informing
   them that they can now login.


Configuration
-------------

To make use of this backend, simply include the URLConf
``registration.backends.admin_approval.urls`` at whatever location you choose
in your URL hierarchy.

This backend makes use of the same settings documented in
:ref:`the default backend <default-backend>` plus the following settings:

``REGISTRATION_ADMINS``
    A list with the same structure as the ``ADMINS`` Django setting containing
    names and emails. Approval emails will be sent to the emails defined here.
    If this setting is not set (or is empty), emails defined in ``ADMINS``
    will be used. Optionally, this can be defined as a string with the path
    of a callable that returns a list of the same structure as the
    ``ADMINS`` setting.
