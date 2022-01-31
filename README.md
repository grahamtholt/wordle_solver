# Wordle Solver

Code to generate optimal guesses for the [Wordle](https://www.powerlanguage.co.uk/wordle/) puzzle game.
The game asks the player to guess a hidden word by making repeated, one-word guesses and then incorporating feedback.

Uses a word-list (currently from the wordle source code) and finds the guesses that maximize the entropy of the hidden word distribution.

## Performance
![Guess distribution](./test/guess_distribution.svg)
<img src="./test/guess_distribution.svg">

The precomputed data take a few seconds to load, but finding optimal guesses takes less than a second for these small word-lengths.

## Usage
To use the simple commandline app with the python interpreter, simply:

```
>>>import app
>>>wordler = app.Wordler('./resources/data.parquet')
>>> wordler = app.Wordler('./resources/data.parquet')
Loading data...
>>> wordler.start()
Guess soare (entropy 5.89)
Enter Wordle response for "SOARE" (0=gray, 1=yellow, 2=green):	00000
Guess clint (entropy 5.51)
Enter Wordle response for "CLINT" (0=gray, 1=yellow, 2=green):	01102
Choose randomly from "LIGHT" or "LIMIT"
```

See the included `example.py` for an example of guessing the hidden word "crimp" using the backend.
