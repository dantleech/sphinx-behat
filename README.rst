Behat Sphinx Extension
======================

This POC Sphinx Extension aims to add support for generating behat `.feature`
files from restructured text documentation.

Currently if you have the file::

    Controllers and Templates
    -------------------------

    Make your content route aware
    .............................

    This is a test tutorial. First of all you should :given:`run the following`::

    .. code-block:: bash

        $ echo "Hello World"

    Then :then:`you should see "Hello World"`

And you enable this extension and run::

    sphinx-build -b behat source/ build source/testfile.rst

Then it will build the following file::

    Feature: content-to-controllers
        This document should work

        Scenario: Controllers and Templates

        Scenario: Make your content route aware
            Given run the following
            Then you should see "Hello World"

Obviously thats not perfect, but its a start.
