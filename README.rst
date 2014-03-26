===============================
Energy Meter Mercury 206
===============================

Implements primitives allowing to communicate with energy meter `Mercury 206 (RUS) <http://www.incotexcom.ru/m206.htm>`_ over serial interface with Python and get current display readings remotely.

* Free software: MIT license

Реализует примитивы позволяющие взаимодействовать со счётчиком электрической энергии `Меркурий 206 <http://www.incotexcom.ru/m206.htm>`_ через последовательный интерфейс и дистанционно получать текущие показания дисплея.

Usage
-----

Use a virtualenv::

    $ virtualenv mercury206.env
    $ source mercury206.env/bin/activate

Install package with all dependencies into virtualenv::

    $ pip install git+https://github.com/sergray/energy-meter-mercury206.git

Create sample configuration (requires Python 2.7)::

    $ mercury206_config

Edit ``${HOME}/.mercury206/config.ini``. It is possible to override default configuration path with environment variable ``MERCURY_CONFIG``.

Get display readings::

    $ mercury206_readings

Использование
-------------

Создадим и установим пакет и зависимости в виртуальное окружение::

    $ virtualenv mercury206.env
    $ source mercury206.env/bin/activate
    $ pip install git+https://github.com/sergray/energy-meter-mercury206.git

Создадим шаблон настроек (предполагает наличие Python 2.7)::

    $ mercury206_config

Отредактируем ``${HOME}/.mercury206/config.ini``. Путь в конфигурационному файлу можно переопределить с помощью переменной окружения ``MERCURY_CONFIG``.

Если путь к последовательному порту и адрес счётчика указаны правильно,получим показания счётчика::

    $ mercury206_readings
