# Minesweeper
Classic minesweeper (customizable size and number of bombs, chord available)
- Left click on a covered tile to open it
- Right click on a covered tile to flag it
- Chord: if the number on an uncovered tile equals to the number of flags adjacent to it (eg: there is a "5" tile with 5 flags around it), left clicking on that tile will open all adjacent unflagged covered tiles
- F5 to restart

Future plans
- Implement an easy-start version (first click is always safe)
- Implement a recursive chord version
  - Recursive chord: if a tile is uncovered and the number equals to the number of flags adjacent to it, all adjacent unflagged covered tiles will automatically open at the same time (unlike standard chord, where a left click on the number is necessary to open them)
- Implement a flagging chord version
  - Flagging chord: if the number on an uncovered tile equals to the number of adjacent covered tiles (eg: there is a "3" tile with 3 covered tiles adjacent to it), left clicking on that tile will flag all adjacent covered tiles.
- Implement a guess-free version (guessing is always unnecessary)
- Implement a Minesweeper solver (probably needed for the guess-free version)
- Implement a cruel-but-fair version (necessary guesses are always safe, but punishes for unnecessary guessing)
