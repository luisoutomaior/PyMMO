

# PyMMO

![pymmo](https://github.com/luisoutomaior/pymmo/blob/main/pymmo.png?raw=true)



**_PyMMO_** is an attempt at template for a Python-based MMO game built using **_PyGame_** on top of Python's built-in **_socket_** protocol library. This template implements a simple MMORPG with baked in features such as:
- In-Game Chat bubbles functionality;
- Action battling with server-side processing functionality;
- Ability to be run on a cloud server, locally in your machine, or anywhere in-between due to the use of sockets.

## Preview:

https://user-images.githubusercontent.com/5900245/118431275-2872ec00-b693-11eb-9fe6-0bde1151463b.mov

## Requirements
- PyGame 2.0+

## Usage

### Running the PyMMO server
For all commands below you must be situated in the root folder of this repository.

In one terminal, run server via:
```sh
python server.py
```

### Running the PyMMO client template 
In another terminal, run the following to open a client, i.e. the game: 

```sh
python client.py
````

A game window will open and spawn two entities: a player object, which is your controllable character and comes in magenta; and an enemy object, which you can interact with. Both are added to the server. The names of all entities are shown alongside their health point bars.

### Open multiple clients for multiplayer functionality

Open an additional terminal, and run in it the following command to open a new client instance:
```sh
python client.py
````


Adjust network settings by changing IP and port values in macro.py according to your needs.

### In-game commands:
- **Move** your character via up/right/left/down keyboard arrows. 
- **Attack** an enemy or another player by pressing space. This will damage the entity you are overlapping with, and it can damage both "enemy" and "player" entities. When HP bar reaches zero, the entity is killed and removed from the server. 
- **Chat** in-game by pressing any lowercase letter to write text to the in-game chat floatting bubble. Press enter to publish the text bubble you entered to all other players in the scene.







## WORK IN PROGRESS! Needs some work (please feel free to contribute!):

- Animated graphics (0%)
- Network stability (20%)
- Unit-tests (0%)
- Animated graphics (0%)
- Server-side computations (20%)


**This was put together in a rush to try to finish within a day or so... Contributions such as additional features, code polishment/review/refactoring, optimization, are not only needed, but would be highly appreciated!! Huge thanks in advance! :)**
