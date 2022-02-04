# Ted Moonchild and the Roadies in Space in Python

![game demo](https://moonchild.space/images/tmatris_gameplay.gif)

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

* Fullscreen terminal is suggested for now, but the minimum size of the World UI is `111 x 43`
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

The stats are scaled according to the following formulas:

| **Column** | **Formula**                   |
|------------|-------------------------------|
| **XPREQ**  | `PrevReq + ( PrevLvl * 300 )` |
| **HPMAX**  | `CurLvl * 75`                 |
| **MPMAX**  | `CurLvl * 25`                 |
| **SP**     | Manual entry                  |

The table below represents the results:

| **LEVEL** | **XPREQ** | **HPMAX** | **MPMAX** | **SP** |
|-----------|-----------|-----------|-----------|--------|
| 1         | 0         | 75        | 25        | 0      |
| 2         | 300       | 150       | 50        | 5      |
| 3         | 900       | 225       | 75        | 5      |
| 4         | 1800      | 300       | 100       | 5      |
| 5         | 3000      | 375       | 125       | 5      |
| 6         | 4500      | 450       | 150       | 5      |
| 7         | 6300      | 525       | 175       | 5      |
| 8         | 8400      | 600       | 200       | 5      |
| 9         | 10800     | 675       | 225       | 5      |
| 10        | 13500     | 750       | 250       | 5      |
| 11        | 16500     | 825       | 275       | 5      |
| 12        | 19800     | 900       | 300       | 5      |
| 13        | 23400     | 975       | 325       | 5      |
| 14        | 27300     | 1050      | 350       | 5      |
| 15        | 31500     | 1125      | 375       | 5      |
| 16        | 36000     | 1200      | 400       | 10     |
| 17        | 40800     | 1275      | 425       | 10     |
| 18        | 45900     | 1350      | 450       | 10     |
| 19        | 51300     | 1425      | 475       | 10     |
| 20        | 57000     | 1500      | 500       | 10     |

## Challenge Rating System

The following table represents the scale for XP and Floyd rewards, and base stats for enemies. The idea is to be able to scale enemies in areas based on Ted's level, so grinding could be done at any level, anywhere.

Some enemies will have stat modifiers to add some strategy to the player's decisions on adding stat points. Boss enemies will especially have one or two stats inflated to incentivize a more thoughtful approach to leveling.

| **RATING** | **XPAWARD** | **FLOYDS MIN** | **FLOYDS MAX** | **ATK** | **DEF** | **MOJO** | **LUK** | **ACC** |
|------------|-------------|----------------|----------------|---------|---------|----------|---------|---------|
| 0          | 25          | 0              | 5              | 0       | 0       | 0        | 0       | 0       |
| 1          | 50          | 20             | 25             | 2       | 2       | 2        | 2       | 2       |
| 2          | 75          | 40             | 50             | 4       | 4       | 4        | 4       | 4       |
| 3          | 100         | 60             | 75             | 4       | 4       | 4        | 4       | 4       |
| 4          | 125         | 80             | 100            | 5       | 5       | 5        | 5       | 5       |
| 5          | 150         | 100            | 125            | 5       | 5       | 5        | 5       | 5       |
| 6          | 175         | 120            | 150            | 5       | 5       | 5        | 5       | 5       |
| 7          | 200         | 140            | 175            | 6       | 6       | 6        | 6       | 6       |
| 8          | 225         | 160            | 200            | 6       | 6       | 6        | 6       | 6       |
| 9          | 250         | 180            | 225            | 6       | 6       | 6        | 6       | 6       |
| 10         | 275         | 200            | 250            | 6       | 6       | 6        | 6       | 6       |
| 11         | 300         | 220            | 275            | 8       | 8       | 8        | 8       | 8       |
| 12         | 325         | 240            | 300            | 8       | 8       | 8        | 8       | 8       |
| 13         | 350         | 260            | 325            | 8       | 8       | 8        | 8       | 8       |
| 14         | 375         | 280            | 350            | 8       | 8       | 8        | 8       | 8       |
| 15         | 400         | 300            | 375            | 10      | 10      | 10       | 10      | 10      |
| 16         | 425         | 320            | 400            | 10      | 10      | 10       | 10      | 10      |
| 17         | 450         | 340            | 425            | 10      | 10      | 10       | 10      | 10      |
| 18         | 475         | 360            | 450            | 15      | 15      | 15       | 15      | 15      |
| 19         | 500         | 380            | 475            | 15      | 15      | 15       | 15      | 15      |
| 20         | 525         | 400            | 500            | 20      | 20      | 20       | 20      | 20      |
