Readme File:
===================================================

Title :		BattleCity Arabic Remake
Description :	A remake of the classic game BattleCity in Arabic
Release Date :	September 21, 2010
Version :	1.0 RC2
License :	GPL version 3 (you should have received a copy)
Company :	CloudMill Games
Email :		salwanmax@gmail.com
Credits :	Salwan Asaad (aka. SandHawk) <Developer>
		Khalid Yousif (aka. DesertPanther) <QA>
		Graphics and Sound are taken from the original game		

===================================================

* Construction *

Base :		Python 2.5, PyGame 1.9.1, PyEnkido (my own game engine)
Editor :	Embedded
Known Bugs :	None!
Features :	A faithful recreation of the original mechanics
Secret :	`G` to enable invincibility (development purposes)
		F1-F6 give player 1 bonus items directly (development purposes)
                F7-F12 give player 2 bonus items directly (development purposes)

===================================================

* Play Information *

Game :		BattleCity Arabic Remake
Type :		Arcade
Requires :	Windows 2000 and later, Linux (Python + Pygame 1.9)
Players :	1 player for now
Controls :	- Player 1: Cursor keys and Space/LCtrl to fire
		- Player 2: WSAD keys and RCtrl to fire
		- Enter to select
		- Escape to pause then Q to quit or M for main menu

===================================================

* Change Log *

BattleCity Reamake 1.0 RC2 ()
Major:
- *Fixed* a glitch in carrying tank level across levels
- Optimizations to boost performance
--------------------------------------------

BattleCity Remake 1.0 RC1 (September 21, 2010)
Major:
- *Fixed* occasional read error when pickle tries to read game.bin
- *Fixed* issue that sometimes caused tanks to overlap
- Game now goes back to round 1 if you win round 50
Minor:
- Warning when base in danger
- Gameover notification when one of the player in a 2 players game dies

--------------------------------------------
BattleCity Remake 0.9.2 (September 20, 2010)
Major:
- Player 2 is fully functional and has it's own state
- *Fixed* occasional game.bin read error.
Minor:
- Added fullscreen mode support

--------------------------------------------
BattleCity Remake 0.9.1 (September 06, 2010)
Major:
- *Fixed* Ice tiles didn't work at all
- *Fixed* All power ups give a life
- *Fixed* Shells are drawn under water and ice tiles
Minor:
- The gameplay is made faster
- A better application icon
- Pressing Escape now pauses the game rather than 'P'
- Pause menu that give three choices: continue, back to mainmenu, and exit game.
- Score screen now can be skipped quickly by holding space or enter

--------------------------------------------
BattleCity Remake 0.9 (September 03, 2010)
- Initial release