# Ted Moonchild and the Roadies in Space

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

## Notes

* 170 x 47 is base assumed max terminal size
* Following commands entered into bash will show column and line size for terminal window.
  * `tput cols`
  * `tput lines`
* Command line arguments:
  * `python main.py [-d|--debug]` - Prints game calculations and results to console output.
  * `python main.py [-nc|--nocolor]` - Turns off colorama styles.
  * `python main.py [-w|--width] INT` - Specifies the terminal output width

## Combat Turn Logic

1. Random pick a number 0-5
    * If 4, miss; else move on
2. Random pick a number 0-5; set as `DMG`
3. Random pick a number 0-10
    * If 5, add `CRIT` to `DMG`; else move on
4. Add `ATKBNS` to `DMG`
5. Add `FXBNS` to `DMG`
6. Deal `DMG` to enemy

## CRIT & XP Table

```plaintext
XP Amount   Lvl     CRIT
------------------------
0           1       +2
300         2       +2
900         3       +2
2,700       4       +2
6,500       5       +3
14,000      6       +3
23,000      7       +3
34,000      8       +3
48,000      9       +4
64,000      10      +4
85,000      11      +4
100,000     12      +4
120,000     13      +5
140,000     14      +5
165,000     15      +5
195,000     16      +5
225,000     17      +6
265,000     18      +6
305,000     19      +6
355,000     20      +6
```

## Challenge Rating System

* The idea is that when entering new creatures to the database, you can assign a challenge rating instead of a creature level. Makes it easier than remembering the XP amounts and less thought involved in the question "How much is this enemy worth?"
* This will also determine the enemy's `CRITBNS`

```plaintext
CR      XP Amount   CRITBNS
---------------------------
0       50          +1
1       100         +1
2       250         +1
3       500         +2
4       1000        +2
5       1800        +2
6       2300        +2
7       2900        +3
8       3900        +3
9       5000        +3
10      5900        +3
11      7200        +4
12      8400        +4
13      10000       +4
14      11500       +4
15      13000       +5
16      15000       +5
17      18000       +5
18      20000       +6
19      22000       +6
20      25000       +7
```
