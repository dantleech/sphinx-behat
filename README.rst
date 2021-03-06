Behat Sphinx Extension
======================

This WIP Sphinx Extension adds support for generating behat `.feature`
files from restructured text documentation.

Basically each section of the documentation is interpreted as a `Scenario` and
the extension adds a role `:behat:` which enables you to add Behat scenario
parts (e.g. `Given x`, `Then y`).

Some things to note:

- **Code modification instructions and diffs**: Lots of instructions involve
  code modification (e.g. add this line to your configuration file). It is
  tricky (but not impossible) to present this information in a way which is
  100% acceptable for humans. The compromise is to use the `diff` format in
  the documenation (this is more precise anyway). But understandably prople
  won't think this is ideal - but what is more ideal?  That the code works or
  that it looks nice?

- **Dependencies**: Lots of documentation is made up of a series, with each
  document building on the result of the previous article. This needs to be
  implemented somehow.

- **Work in progrss**: This is still a work in progres.

Currently, given you have the following file::

    Controllers and Templates
    =========================

    Requirements
    ------------

    - PHP 5.4 :behat:`Given I execute "php"` :behat:`Then the command should not fail`

    Installation
    ------------

    Clone the repository
    ~~~~~~~~~~~~~~~~~~~~

    First clone the repository :behat:`Given you execute the following`:

    .. code-block:: bash

        git clone git@github.com:sulu-cmf/sulu-standard.git
        cd sulu-standard

    and checkout the development branch :behat:`And you execute the following`:

    .. code-block:: bash

        git checkout develop

    :behat:`Then the file "composer.json" should exist`

    Create the default configuration
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    For the project to work you must also create some default configuraiton files,
    to use doctrine-dbal execute :behat:`Given you execute the following`:

    .. code-block:: bash

        cp app/config/phpcr_jackrabbit.yml.dist app/config/phpcr.yml

    Alternatively, if you want to use jackrabbit:

    .. code-block:: bash

        cp app/config/phpcr_jackrabbit.yml.dist app/config/phpcr.yml

    :behat:`Then the command should not fail`

    You may want to change the name of the default database :behat:`And you apply the following diff`:

    .. code-block:: diff

        diff --git a/app/config/parameters.yml.dist b/app/config/parameters.yml.dist
        index 2e78e75..1d77cad 100644
        --- a/app/config/parameters.yml.dist
        +++ b/app/config/parameters.yml.dist
        @@ -2,7 +2,7 @@ parameters:
             database_driver:    pdo_mysql
             database_host:      127.0.0.1
             database_port:      ~
        -    database_name:      sulu
        +    database_name:      mydatabasename
             database_user:      root
             database_password:  ~

    Install the dependencies
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Make sure the composer is installed :behat:`Given composer is installed` (https://getcomposer.org)
    for installation instructions)

    Then install the dependencies :behat:`Given you execute the following`:

    .. code-block:: bash

        composer.phar install

    :behat:`Then the command should not fail`

    Initialize the Environment
    --------------------------

    Create the database and schema :behat:`Given you execute the following`:

    .. code-block:: bash

        php app/console doctrine:database:create
        php app/console doctrine:schema:create


And you enable this extension and run::

    sphinx-build -b behat source/ build content-to-controllers.rst

Then it will build the following file::

    Feature: content-to-controllers
        This document should work

        Scenario: Create the default configuration
            Given you execute the following (in "bash"):
            """
            cp app/config/phpcr_jackrabbit.yml.dist app/config/phpcr.yml
            """
            Then the command should not fail
            And you apply the following diff (in "diff"):
            """
            diff --git a/app/config/parameters.yml.dist b/app/config/parameters.yml.dist
            index 2e78e75..1d77cad 100644
            --- a/app/config/parameters.yml.dist
            +++ b/app/config/parameters.yml.dist
            @@ -2,7 +2,7 @@ parameters:
                 database_driver:    pdo_mysql
                 database_host:      127.0.0.1
                 database_port:      ~
            -    database_name:      sulu
            +    database_name:      mydatabasename
                 database_user:      root
                 database_password:  ~
            """

        Scenario: Install the dependencies
            Given composer is installed
            Given you execute the following (in "bash"):
            """
            composer.phar install
            """
            Then the command should not fail

        Scenario: Requirements
            Given I execute "php"
            Then the command should not fail

        Scenario: Initialize the Environment
            Given you execute the following (in "bash"):
            """
            php app/console doctrine:database:create
            php app/console doctrine:schema:create
            """

        Scenario: Clone the repository
            Given you execute the following (in "bash"):
            """
            git clone git@github.com:sulu-cmf/sulu-standard.git
            cd sulu-standard
            """
            And you execute the following (in "bash"):
            """
            git checkout develop
            """
            Then the file "composer.json" should exist
