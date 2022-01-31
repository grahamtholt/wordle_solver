# Wordle Solver

Code to generate optimal guesses for the [Wordle](https://www.powerlanguage.co.uk/wordle/) puzzle game.
The game asks the player to guess a hidden word by making repeated, one-word guesses and then incorporating feedback.

Uses a word-list (currently from the wordle source code) and finds the guesses that maximize the entropy of the hidden word distribution.

## Performance
![Guess distribution](./test/guess_distribution.svg)

### Efficiency
Pursuing a maximum-entropy strategy is boring, but reliable!
The app never takes more than 5 guesses to find the Wordle.
In a rare few cases it gets it in 2.
But, sadly, it will never achieve the dream of the Wordle hole-in-one.

Also by virtue of this approach we do quite well even against an adversarial opponent like [Absurdle](https://qntm.org/files/wordle/)!
Because of the dynamic approach used there, to get interesting results please try the `custom_start` option in the `Wordler.start` method.
Finding the hidden word in 5 or 6 tries was typical of my Absurdle experience.

### Speed
The precomputed data take a few seconds to load, but finding optimal guesses takes less than a second for these small word-lengths.

## Usage
To use the simple commandline app with the python interpreter, simply:

```
>>> import app
>>> wordler = app.Wordler()
Loading data...
>>> wordler.start()
Guess SOARE (entropy 5.89)
Enter Wordle response for "SOARE" (0=gray, 1=yellow, 2=green):	00000
Guess CLINT (entropy 5.51)
Enter Wordle response for "CLINT" (0=gray, 1=yellow, 2=green):	01102
Choose randomly from "LIGHT" or "LIMIT"
>>>
```

Here's an example with Absurdle:
```
>>> wordler.start(max_guesses=10, custom_start="arise")
Guess ARISE (entropy 5.82)
Enter Wordle response for "ARISE" (0=gray, 1=yellow, 2=green):	00000
Guess MULCH (entropy 5.21)
Enter Wordle response for "MULCH" (0=gray, 1=yellow, 2=green):	00000
Guess GOODY (entropy 3.25)
Enter Wordle response for "GOODY" (0=gray, 1=yellow, 2=green):	02202
Guess BLITZ (entropy 2.00)
Enter Wordle response for "BLITZ" (0=gray, 1=yellow, 2=green):	00001
Choose "WOOZY"
```

See the included `example.py` for an example of guessing the hidden word "crimp" for Absurdle using the backend.

##Acknowledgments
Many thanks to [Josh Wardle](https://powerlanguage.co.uk/), creator of Wordle, and [qntm](https://qntm.org/), creator of Absurdle.
