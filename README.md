# Telegram DX-Bot

A Telegram DX-Cluster bot.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

- redis
- python-telegram-bot

```
$ sudo apt-get install git python3 python3-pip
$ pip install python-telegram-bot --upgrade
$ pip install redis
```

Setting up redis:
```
$ wget http://download.redis.io/redis-stable.tar.gz
$ tar xvzf redis-stable.tar.gz
$ cd redis-stable
$ make
$ cd src
$ sudo cp redis-server /usr/local/bin
$ sudo cp redis-cli /usr/local/bin
$ cd ..
$ cd ..
$ rm redis-stable.tar.gz
```

### Installing

```
$ pip install python-telegram-bot --upgrade
$ ./setup.py
$ sudo systemctl enable redis.service
$ sudo systemctl enable dxbot.service
```

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Redis](https://github.com/antirez/redis) - Database
* [Python-Telegram-Bot](https://github.com/python-telegram-bot/python-telegram-bot) - Python telegram bot wrapper

## Authors

* **Hendrik Teuber, DD5HT** - *Initial work* - [DD5HT](https://github.com/DD5HT)

## License

This project is licensed under the LGPL-3 License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Many thanks to DL3LAR and DM5EE for initial testing 

