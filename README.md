# Dice Parser

This is an app designed to take a text string in RPG dice notation and
roll those dice, returning the result and a breakdown of how the result
was arrived at.

# Changelog

0.0.1
Added the main parser.py file
Currently does literally nothing except spit back the arguments you give it in the form of a joined string
This is gonna take a while

# Dice Notation

At its simplest, Dice Notation allows you to indicate a number of dice to
roll, and the number of sides each of those dice have. For example: 1d6,
4d6, 5d12, etc.

Then you can perform mathematical operations on the result. So 2d6+3 would
roll 2 six sided dice, add them together, and add 3 to the result. You
can use any of the four main operators: +, -, *, /

Then we get into the complex part, and the part where specific RPG systems
rear their heads of various degrees of physical repulsiveness.

# Modifiers

The following is a list of modifiers used in most game systems, followed by
modifiers from specific game systems.

k[x]h/k[x]l:	keeps only the [x] highest or lowest results rolled. This
		modifier is used in calculating character statistics in
		D&D - 4d6 k3h, or roll four six sided dice and keep the
		three highest results.

rr[x]:		rerolls dice which come up as [x] (default 1). [x] can be a
		range, in which case it is inclusive. Dice can only be
		rerolled once; if the second result is also a rerollable
		number, tough luck.


