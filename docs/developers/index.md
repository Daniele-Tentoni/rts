# Developer Guides

In this section is explained the entire game for developers. Here you can learn how to getting started contributing and add features or unit testing.

Start here: [Getting Started](getting_started.md).

Then learn how to contribute on many common things like game assets.

Learn how to contribute to [unit testing](unit_testing.md) and bug fixing to make this game a better game.

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
─> Ruler
   |
   └─> Tower
       |
       ├─> Soldiers controlled by tower
       |   |
       |   └─> Soldier
       |   └─> Soldier
       |
       └─> Routes
           |
           └─> Destination
```
