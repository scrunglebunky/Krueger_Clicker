# Welcome to Krueger Clicker!
## WARNING: THIS PROGRAM USES THE LIKENESS OF REAL PEOPLE. REAL IMAGES OF REAL PEOPLE THAT WERE IN MY COMP SCI CLASS. 
- This was a fun program that I made in 10th grade. 
- Krueger Clicker is a simple clicker-style idle game where you click my Computer Science instructor. 
- I made this four years ago now (2022), when I'd only been programming for two-ish years. 
- The program is very well documented, and decently well organized.


## THE GAMEPLAY
- You click Krueger to gain Kroogs
- You can purchase students to collect Kroogs for you.
- You can purchase upgrades that gives you more KPC (Kroogs Per Click) for both yourself and the students.
- When you max out on Students, you can purchase Super Students, which are 100 students condensed into one.
- Eventually you reach an end, when there's either nothing to purchase or the game takes up too much resources and crashes.


## KNOWN ISSUES
- One of my friends at the time was able to make a malicious save file to remotely execute code. 
    - This was because the program used eval() with no input validation.
- Eventually when you got far enough into the game, the game started heavily lagging due to taking up too many resources.
    - I mean, with a game with no end, it's hard to do something about it.
    - I could do it if I remade it now, but I'm not going to make a game like this again.
- For some reason I did error checking with importing TKinter, but didn't go through the effort of disabling saving/loading if it wasn't found.
    - I could very easily do this now, but for preservation purposes I will not. 


## OTHER TIDBITS
- "Notes" was my way of handling documentation at the time. 
- There was an update planned in the documentation (1.1.0) that added replayability with prestiges, but I never got around to it.
- All of the music is intentionally low-quality, and it is also royalty-free.
- The voicelines were Microsoft Sam with a lower pitch and speed.
- This game was placed on a Shared Drive through Windows Active Directory. 
    - Instead of separate downloaded instances, everyone played the same instance on their computer.
    - The "statistics.txt" was an actual combined number of everyone who had played the game. In its time, it had been played for >50,000 seconds (13 hours)