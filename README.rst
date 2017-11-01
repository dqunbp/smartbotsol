===============
pythonSmartBots
===============


.. image:: https://img.shields.io/pypi/v/smartbotsol.svg
        :target: https://pypi.python.org/pypi/smartbotsol

.. image:: https://img.shields.io/travis/dqunbp/smartbotsol.svg
        :target: https://travis-ci.org/dqunbp/smartbotsol

.. image:: https://readthedocs.org/projects/smartbotsol/badge/?version=latest
        :target: https://smartbotsol.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/dqunbp/smartbotsol/shield.svg
     :target: https://pyup.io/repos/github/dqunbp/smartbotsol/
     :alt: Updates


smart conversation bots package


* Free software: MIT license
* Documentation: https://smartbotsol.readthedocs.io.


Getting started
----------------
1. Describe yor states
2. Create `server.py`:

    .. code-block:: python

        from telegram.ext import Updater
        from smartbotsol import StateMachine
        from smartbotsol.telegram import FsmTelegramHandler

        import logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
        log = logging.getLogger(__name__)

        from states import BootStrapState

        handler = FsmTelegramHandler(
            StateMachine(
                BootStrapState(),
                filters=[]
            )
        )

        def create_bot():
            token = os.environ.get('TELEGRAM_TOKEN')
            port = int(os.environ.get('PORT', '5000'))
            updater = Updater(token)
            updater.dispatcher.add_handler(handler)            
            return updater

        def start_polling_bot():
            bot = create_bot()
            bot.start_polling(read_latency=50.0)
            return bot

        if __name__ == '__main__':
            start_polling_bot()

For async runs pass `async=True`: 

    .. code-block:: python

        handler = FsmTelegramHandler(
            StateMachine(
                BootStrapState(),
                filters=[]
            ),
            async=True
        )

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

