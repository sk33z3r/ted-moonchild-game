# Ted Moonchild and the Roadies in Space in Python

```plaintext
          (         *       )     )     )          ) (   (   (
  *   )   )\ )    (  `   ( /(  ( /(  ( /(   (   ( /( )\ ))\ ))\ )
` )  /(( (()/(    )\))(  )\()) )\()) )\())  )\  )\()|()/(()/(()/(
 ( )(_))\ /(_))  ((_)()\((_)\ ((_)\ ((_)\ (((_)((_)\ /(_))(_))(_))
(_(_()|(_|_))_   (_()((_) ((_)  ((_) _((_))\___ _((_|_))(_))(_))_
|_   _| __|   \  |  \/  |/ _ \ / _ \| \| ((/ __| || |_ _| |  |   \
  | | | _|| |) | | |\/| | (_) | (_) | .` || (__| __ || || |__| |) |
  |_| |___|___/  |_|  |_|\___/ \___/|_|\_| \___|_||_|___|____|___/


                             AND THE


          __  __      __   __ __         __ __     __ __
         |__)/  \ /\ |  \||_ (_   . _   (_ |__) /\/  |_
         | \ \__//--\|__/||____)  || )  __)|   /--\__|__
```

## Play the latest code

1. [Install Docker](https://docs.docker.com/compose/install/) and `docker-compose`
2. Clone this repo and change to it
3. Fullscreen your terminal (for now this is necessary)
4. Run `./test-run.sh local`
5. Enter the password: `m00nch1ld`

```shell
$ git clone https://git.blackrookllc.com/ted-moonchild/moonchild-game.git
$ cd ./moonchild-game
$ ./test-run.sh local
ted password: m00nch1ld
```

## FAQ

* **110 x 40** is the minimum terminal size
* Terminals are notoriously non-uniform. I won't be able to guarantee colors or even text input operations. I've noticed a few potential issues:
  * Some terminals do not return a height,width with the `getmaxyx()` method. This means centering and resizing might not operate correctly either.
  * Most terminals do not support `BACKSPACE` or `DELETE` when entering text input. So far `Ctrl+H` always works.
  * Even `xterm` between OS implementations varies in behavior.

## Combat Turn Logic

1. Random pick a number 0-5
    * If 4, miss; else move on
2. Random pick a number 0-5; set as `DMG`
3. Random pick a number 0-10
    * If 5, add `CRIT` to `DMG`; else move on
4. Add `ATKBNS` to `DMG`
5. Add `FXBNS` to `DMG`
6. Deal `DMG` to enemy

## Player Details

This table shows the scale for XP needed to reach each level.

```plaintext
XP Amount   Lvl
----------------
0           1
300         2
900         3
2,700       4
6,500       5
14,000      6
23,000      7
34,000      8
48,000      9
64,000      10
85,000      11
100,000     12
120,000     13
140,000     14
165,000     15
195,000     16
225,000     17
265,000     18
305,000     19
355,000     20
```

## Challenge Rating System

The idea is that when entering new creatures to the database, you can assign a challenge rating to define the creature's power. Makes it easier to place enemies and scale their attacks based on the player level, instead of hard coding stats for every creature. This also removes weak enemies from the game, and allows the player to grind, if desired, anywhere and still get comparable XP to their level.

The table below shows the XP award scale. This database also defines base stats and FLOYD rewards.

```plaintext
CR      XP Award
-----------------
0       50
1       100
2       250
3       500
4       1000
5       1800
6       2300
7       2900
8       3900
9       5000
10      5900
11      7200
12      8400
13      10000
14      11500
15      13000
16      15000
17      18000
18      20000
19      22000
20      25000
```
