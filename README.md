# Minesweeper
Classic minesweeper (customizable size and number of bombs, chording available)
- Left click on a covered tile to open it
- Right click on a covered tile to flag it
- Chording: if the number on an uncovered tile equals to the number of flags adjacent to it (eg: there is a "5" tile with 5 flags around it), left clicking on that tile will open all adjacent unflagged covered tiles
- F5 to restart

Future plans
- Implement an easy-start version (first click is always safe)
- Implement a recursive chording version
- Implement a flagging chord version
  - Flagging chord: if the number on an uncovered tile equals to the number of adjacent covered tiles (eg: there is a "3" tile with 3 covered tiles adjacent to it), left clicking on that tile will flag all adjacent covered tiles.
- Implement a guess-free version (guessing is always unnecessary)
- Implement a Minesweeper solver (probably needed for the guess-free version)
- Implement a cruel-but-fair version (necessary guesses are always safe, but punishes for unnecessary guessing)
