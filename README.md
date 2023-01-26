# Sangatsu

Sangatsu is a chess.com bot/cheat assistant that highlightsthe best moves for you on the board.

**I don't condone cheating, this was just a learning experience to me, please do not use it to cheat against other players.**

## Disclaimer
Chess.com has a [Fair Play Policy](https://www.chess.com/legal/fair-play) that states:
```
EXCEPTION: These rules do not apply to unrated games or tactics. However, if you intend to use assistance against your opponent, you must notify them beforehand. We may expand or narrow any applicable exceptions to the Fair Play Policy at any time without notice to you.
```
So, if you use this bot, you must notify your opponent beforehand. Or use it against bots.

## How it works

* TODO

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.
Note: this was tested on python 3.10, it may not work on other versions.


```bash
pip install -r requirements.txt
```
NOTE: Change the piece notations in chess.com from figures to text or it won't work.


## Usage

Straightforward, set up your credentials in a credentials.txt file with the following format
```
username
password
```

open sangatsu.py or use the command line.

```python
python3 sangatsu.py
```
If you join a tournament, click on Analysis tab after game is over so the bot can parse the game.


## Contributing
Pull requests are welcome.

## License
[MIT](https://choosealicense.com/licenses/mit/)