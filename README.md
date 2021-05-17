# PyMMO

![pymmo](https://github.com/luisoutomaior/pymmo/blob/main/pymmo.png?raw=true)



Template for a Python-based MMO game using sockets and PyGame. This template is a simple MMORPG with rudimentary chat and action battling functionality. 


### Requirements
- PyGame 2.0+

### Usage
For all commands below you must be situated in the root folder of this repository.

In one terminal, run server via:
```sh
python server.py
```

In another terminal, run the following to open a client, i.e. the game: 

```sh
python client.py
````

A game window will open and spawn two entities: a player object, which is your controllable character and comes in magenta; and an enemy object, which you can interact with. Both are added to the server. The names of all entities are shown alongside their health point bars.

#### Open multiple clients for multiplayer functionality

Open an additional terminal, and run in it the following command to open a new client instance:
```sh
python client.py
````



You can control your character via up/right/left/down keyboard arrows. You can attack an enemy or another player
Press space to attack, write any letters to 



This is just one of my weekend side-projects, but feel free to contribute :)


## WORK IN PROGRESS! Needs some work (please feel free to contribute!):

- Animated graphics (0%)
- Network stability (20%)
- Unit-tests (0%)
- Animated graphics (0%)
- Server-side computations (20%)


**This was put together in a rush to try to finish within a day or so... Code review and more refactoring is definitely needed, and would be highly appreciated!! :)**
