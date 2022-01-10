# Developer Guides

In this section is explained the entire game for developers.

## Game Cycle

The game cycle is composed by following stages:

1. Screen cleaning
2. System label writing
3. Events managing
4. Ruler updates
5. Tower updates
   a. Tower sprite updates
   b. Controlled soldiers updates
6. Other soldiers updates
7. Blit all and flip

This structure has to be reported in the code, in the `def game_cycle(self) -> bool:` function.

## Game Structure

```
-> Ruler
   |
   +-> Tower
       |
       +-> Soldiers controlled by tower
       |   |
       |   +-> Soldier
       |   +-> Soldier
       |
       +-> Routes
           |
           +-> Destination
```
