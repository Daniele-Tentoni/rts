# Tower

Is a blank square in the map and is a part of your kingdom. You have a kingdom as long you have control at least one tower. Towers are placed in your kingdom in a random position.

Inside the blank square you can see the number of soldiers defending that tower.

It generates 1 [Soldier](#soldier) per second up to 10. You control a tower as long as one of your soldier control it. If attackers soldiers kill all yours, you lose the tower control. If your soldiers kill all enemy ones, you take control of tower.

| Property                      | Value           | Description                                                           |
| ----------------------------- | --------------- | --------------------------------------------------------------------- |
| Soldiers generated per second | 1 soldier / sec | Number of soldiers generated per second by the tower                  |
| Maximum number of soldiers    | 10              | Maximum number of soldiers that can stay in a tower at the same time  |
| Soldier output per second     | 1 soldier/sec   | Soldiers that come out from the tower to go to another one per second |

When the tower reach its maximum soldier capacity, it stops the progress to the next one until other soldiers dies.

## Routes

![Routes](../img/routes.gif)

Between tower you can create routes to send your soldiers to fight for your kingdom. They will fight against enemy soldiers sent to protect other towers and if they reach the other site, they will conquer it.

You can create a route between two towers, by clicking on one and release the mouse button or clicking on another one. Soldiers from each tower will start to walk on the route.

If you create a route between two your towers, the one with more soldiers will send them helping the other one, trying to balance the number in each tower.

Each tower could have a route to it for every player. If tower A and tower B have already a route created by player Z, if the same player create a route between B and C, the route between A and B will be destroyed and all soldiers already in that route will return to their origin tower.

## Future releases

In a future release, maximum limits of soldiers per tower will be increased. Tower will have a level depending on how many soldiers you have stick in it. When the limit will be reached, the tower increase the level and the maximum limit of soldiers. When enemy soldiers attack, if they take the number of defending soldiers below a minimum limit, the tower level will be decreased.

The following table present how levels will be managed:

| Level | Soldiers/sec | Soldier output/sec | Maximum | Minimum |
| ----- | :----------: | :----------------: | :-----: | :-----: |
|   1   |     1/s      |        1/s         |    2    |    0    |
|   2   |     1/s      |        1/s         |    5    |    2    |
|   3   |     1/s      |        1/s         |   10    |    5    |
|   4   |     1/s      |        1/s         |   20    |   10    |
|   5   |     1/s      |        1/s         |   50    |   20    |
