# Roadmap

This will be the roadmap to the future versions of this game. About now the contributors are:

- [Daniele Tentoni](https://github.com/daniele-tentoni)

So if you wanna contribute to the project, let me know!

Before the release of version 0.2.0, we have to do those things:

1. Create the route module to link two towers
2. Move soldiers around towers smoothly while there's not a route linked to the tower
3. Move soldiers on a route if there's one between their tower
4. Create a local storage of data for future data and make it available to the entire application (maybe another singleton?)
5. Create hints using pygame_gui for new players to help them with the game
6. Create a settings page where users could reset hints for new players and show/hide the fps label

I can't program how many minor releases there will be before 1.0 release, but I don't wanna release the first version of the game without those features:

1. Multiplayer mode

    a. Menu window with

        - Singleplayer (one player vs dummy npc)

        - Multiplayer (search other players on public servers)

        - Credits (download contributions from Github and shows their avatars)

2. Tower levels (already described in this doc)
3. Route disruption and recovering (already described in this doc)
4. Settings window with reset local storage options and localization changes
