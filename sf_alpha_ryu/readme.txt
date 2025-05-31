- Assets taken originally from Street Fighter Alpha 3.
- Used N64Mario84's (https://mugenarchive.com/forums/downloads.php?do=file&id=20417-ryu-n64mario) SFA Ryu as a base.
- Changes:
	- Updated code to be more friendly with mugen 1.1, however it still uses 8 beta format for sff and palettes
	- Removed Evil Ryu
	- Removed all palettes except for 1 and 2
	- Changed dizzy counter from 200 to 100
	- Shakunetsu Hadoken (all ver) now knock down 
	- Heavy Shakunetsu Hadoken damage changed from 50x3 to 10x3 and animation changed from 14 to 19 frames
	- Medium Shakunetsu Hadoken damage changed from 50x2 to 6x6 and animation changed from 14 to 19 frames, projectile velocity changed to be same speed as light shakunetsu hadoken (used to be in between light and heavy speed)
	- Light Shakunetsu Hadoken damage changed from 50x1 to 6x6
	- Light Hadoken damage changed from 50x1 to 45x1, animation changed from 14 to 10 frames
	- Medium Hadoken damage changed from 50x1 to 60x1, projectile velocity changed to be same speed as light hadoken (used to be in between light and heavy speed)
	- Heavy Hadoken damage changed from 50x1 to 60x1
	- Light tatsu changed from 50x1 to 80x1, juggle point consumption increased from 0x1 to 2x1
	- Medium tatsu damage kept at 50x2, juggle point consumption increased from 0x2 to 2x2
	- Heavy tastsu damage changed from 50x3 to 40x3, juggle point consumption increased from 0x3 to 2x3	
	- Changed level 1 (light) Shinkuu Hadoken damage down from 100x3 to 100x2
	- Changed level 2 (medium) Shinkuu Hadoken damage down from 100x4 to 100x3
	- Changed level 3 (heavy) Shinkuu Hadoken damage down from 100x3 to 100x4
	- Changed level 1 (light) Tatsumaki Senpuu Kyaku damage up from 30*6 to 40*6
	- Changed level 2 (light) Tatsumaki Senpuu Kyaku damage up from 30*10 to 35*10
	- Changed level 3 (heavy) Tatsumaki Senpuu Kyaku damage up from 30*14 to 32*14
	- Changed Shin Shoryuken damage from 100*3 to 165*3, now automatically stuns the opponent on full connect
	- Fixed some compatibility issues with Mugen 1.1 and Ikemen GO
	
- Notes: 
	1 - Dizzy counter in this mugen character is not accurate to dizzy counter in the SFA games, here it ticks up with each attack and ticks down overtime. In the SFA games, it would tick up after each hit, and go away all at once if not hit for some period of time.
	2 - This isn't necessarily supposed to represent any SFA Ryu perfectly, its just a pretty good approximation as a mugen character used to test this nn. 
	3 - All dps do 50x2 damage, the different strengths are how far the dp goes up.
	4 - Dps intentionally kept at 0 juggle point consumption, you can get 400 plus damage/full stun combo in the corner with a hdp > 5mp loop. Timings a little weird, but 
	I wonder if a neural network would ever find this. You can also get a 800+ damage combo with roundstart close hk double hit > htatsu > 5mp > hp loop into stun > lvl 1 Tatsumaki Senpuu Kyaku 
	5 - You can get dizzied out of your super, its not particularly common but for example if the opponent is at 99 dizzy and you hit them with Shin Shoryuken, they will fall out. You still get the punish the opponent and they do not recover before the super finishes. The way to fix this would be to make supers not do stun damage, but I think Shin Shoryuken instant stun is cool so it stays for now.
	6 - Currently the idea is that the sparring partner will be at ai level 4.
	7 - It is impossible to kill with Shin Shoryuken, the opponent will be dizzied instead. 

- Issues:
	1 - In Ikemen GO the KO background flashes for 1 frame whenever you super. This does not happen in any version of the original mugen.