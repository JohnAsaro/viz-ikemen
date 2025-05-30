; Ryu's Command File.

;-| Super Motions |--------------------------------------------------------
; Shinkuu Hadoken
[Command]
name = "shadoken_x"
command = ~D, DF, F, D, DF, F, x
time = 25
[Command]
name = "shadoken_y"
command = ~D, DF, F, D, DF, F, y
time = 25
[Command]
name = "shadoken_z"
command = ~D, DF, F, D, DF, F, z
time = 25

; Shinkuu Tatsumaki Senpuu Kyaku
[Command]
name = "shurricane_a"
command = ~D, DB, B, D, DB, B, a
time = 25
[Command]
name = "shurricane_b"
command = ~D, DB, B, D, DB, B, b
time = 25
[Command]
name = "shurricane_c"
command = ~D, DB, B, D, DB, B, c
time = 25

; Shin Shoryuken
[Command]
name = "shoryu_a"
command = ~D, DF, F, D, DF, F, a
time = 25
[Command]
name = "shoryu_b"
command = ~D, DF, F, D, DF, F, b
time = 25
[Command]
name = "shoryu_c"
command = ~D, DF, F, D, DF, F, c
time = 25

; Shun Goku Satsu
[Command]
name = "shungokusatsu"
command = x, x, F, a, z
time = 30

;-| Special Motions |------------------------------------------------------

; Shoryuken
[Command]
name = "shoryuken_x"
command = ~F, D, DF, x
[Command]
name = "shoryuken_y"
command = ~F, D, DF, y
[Command]
name = "shoryuken_z"
command = ~F, D, DF, z

; Shakunetsu Hadoken
[Command]
name = "fhadoken_x"
command = ~B, DB, D, DF, F, x
[Command]
name = "fhadoken_y"
command = ~B, DB, D, DF, F, y
[Command]
name = "fhadoken_z"
command = ~B, DB, D, DF, F, z

; Hadoken
[Command]
name = "hadoken_x"
command = ~D, DF, F, x
[Command]
name = "hadoken_y"
command = ~D, DF, F, y
[Command]
name = "hadoken_z"
command = ~D, DF, F, z
[Command]
name = "hadoken_s"
command = ~D, DF, F, s

; Tatsumaki Senpuu Kyaku
[Command]
name = "hurricane_a"
command = ~D, DB, B, a
[Command]
name = "hurricane_b"
command = ~D, DB, B, b
[Command]
name = "hurricane_c"
command = ~D, DB, B, c

; Counter Punch
[Command]
name = "counter_p"
command = x+y
[Command]
name = "counter_p"
command = y+z
[Command]
name = "counter_p"
command = x+z

; Counter Kick
[Command]
name = "counter_k"
command = a+b
[Command]
name = "counter_k"
command = b+c
[Command]
name = "counter_k"
command = a+c

;-| Double Tap |-----------------------------------------------------------
[Command]
name = "FF"     ;Required (do not remove)
command = F, F
time = 10

[Command]
name = "BB"     ;Required (do not remove)
command = B, B
time = 10

;-| 2/3 Button Combination |-----------------------------------------------
[Command]
name = "recovery" ;Required (do not remove)
command = x+y
time = 1

[Command]
name = "recovery"
command = y+z
time = 1

[Command]
name = "recovery"
command = x+z
time = 1

[Command]
name = "recovery"
command = a+b
time = 1

[Command]
name = "recovery"
command = b+c
time = 1

[Command]
name = "recovery"
command = a+c
time = 1

;-| Dir + Button |---------------------------------------------------------
[Command]
name = "back_x"
command = /$B,x
time = 1

[Command]
name = "back_y"
command = /$B,y
time = 1

[Command]
name = "back_z"
command = /$B,z
time = 1

[Command]
name = "down_x"
command = /$D,x
time = 1

[Command]
name = "down_y"
command = /$D,y
time = 1

[Command]
name = "down_z"
command = /$D,z
time = 1

[Command]
name = "fwd_x"
command = /$F,x
time = 1

[Command]
name = "fwd_y"
command = /$F,y
time = 1

[Command]
name = "fwd_z"
command = /$F,z
time = 1

[Command]
name = "up_x"
command = /$U,x
time = 1

[Command]
name = "up_y"
command = /$U,y
time = 1

[Command]
name = "up_z"
command = /$U,z
time = 1

[Command]
name = "back_a"
command = /$B,a
time = 1

[Command]
name = "back_b"
command = /$B,b
time = 1

[Command]
name = "back_c"
command = /$B,c
time = 1

[Command]
name = "down_a"
command = /$D,a
time = 1

[Command]
name = "down_b"
command = /$D,b
time = 1

[Command]
name = "down_c"
command = /$D,c
time = 1

[Command]
name = "fwd_a"
command = /$F,a
time = 1

[Command]
name = "fwd_b"
command = /$F,b
time = 1

[Command]
name = "fwd_c"
command = /$F,c
time = 1

[Command]
name = "up_a"
command = /$U,a
time = 1

[Command]
name = "up_b"
command = /$U,b
time = 1

[Command]
name = "up_c"
command = /$U,c
time = 1

;-| Single Button |---------------------------------------------------------
[Command]
name = "fwd"
command = $F
time = 1

[Command]
name = "down"
command = $D
time = 1

[Command]
name = "back"
command = $B
time = 1

[Command]
name = "up"
command = $U
time = 1

[Command]
name = "a"
command = a
time = 1

[Command]
name = "b"
command = b
time = 1

[Command]
name = "c"
command = c
time = 1

[Command]
name = "x"
command = x
time = 1

[Command]
name = "y"
command = y
time = 1

[Command]
name = "z"
command = z
time = 1

[Command]
name = "s"
command = s
time = 1

;-| Hold Button |--------------------------------------------------------------
[Command]
name = "hold_x"
command = /x
time = 1

[Command]
name = "hold_y"
command = /y
time = 1

[Command]
name = "hold_z"
command = /z
time = 1

[Command]
name = "hold_a"
command = /a
time = 1

[Command]
name = "hold_b"
command = /b
time = 1

[Command]
name = "hold_c"
command = /c
time = 1

[Command]
name = "hold_s"
command = /s
time = 1

;-| Hold Dir |--------------------------------------------------------------
[Command]
name = "holdfwd" ;Required (do not remove)
command = /$F
time = 1

[Command]
name = "holddownfwd"
command = /$DF
time = 1

[Command]
name = "holddown" ;Required (do not remove)
command = /$D
time = 1

[Command]
name = "holddownback"
command = /$DB
time = 1

[Command]
name = "holdback" ;Required (do not remove)
command = /$B
time = 1

[Command]
name = "holdupback"
command = /$UB
time = 1

[Command]
name = "holdup" ;Required (do not remove)
command = /$U
time = 1

[Command]
name = "holdupfwd"
command = /$UF
time = 1

;---------------------------------------------------------------------------
; Don't remove the following line. It's required by the CMD standard.
[Statedef -1]

;===========================================================================
;---------------------------------------------------------------------------
; Super Moves
;---------------------------------------------------------------------------
; Metsu/Shin Shoryuken
[State -1, shoryu_a]
type = ChangeState
value = 3020
triggerall = palno < 7
triggerall = power >= 3000
triggerall = command = "shoryu_a"
triggerall = statetype != A
trigger1 = ctrl

[State -1, shoryu_a]
type = ChangeState
value = 3020
triggerall = palno < 7
triggerall = power >= 3000
triggerall = command = "shoryu_a"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450

;---------------------------------------------------------------------------
; Metsu/Shin Shoryuken
[State -1, shoryu_a]
type = ChangeState
value = 3020
triggerall = palno < 7
triggerall = power >= 3000
triggerall = command = "shoryu_b"
triggerall = statetype != A
trigger1 = ctrl

[State -1, shoryu_a]
type = ChangeState
value = 3020
triggerall = palno < 7
triggerall = power >= 3000
triggerall = command = "shoryu_b"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450

;---------------------------------------------------------------------------
; Metsu/Shin Shoryuken
[State -1, shoryu_a]
type = ChangeState
value = 3020
triggerall = palno < 7
triggerall = power >= 3000
triggerall = command = "shoryu_c"
triggerall = statetype != A
trigger1 = ctrl

[State -1, shoryu_a]
type = ChangeState
value = 3020
triggerall = palno < 7
triggerall = power >= 3000
triggerall = command = "shoryu_c"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450

;---------------------------------------------------------------------------
; Messatsu Gou Shoryuu Lvl 1
[State -1, shoryu_a]
type = ChangeState
value = 3060
triggerall = palno > 6
triggerall = power >= 1000
triggerall = command = "shoryu_a"
triggerall = statetype != A
trigger1 = ctrl

[State -1, shoryu_a]
type = ChangeState
value = 3060
triggerall = palno > 6
triggerall = power >= 1000
triggerall = command = "shoryu_a"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450

;---------------------------------------------------------------------------
; Messatsu Gou Shoryuu Lvl 2
[State -1, shoryu_b]
type = ChangeState
value = 3070
triggerall = palno > 6
triggerall = power >= 2000
triggerall = command = "shoryu_b"
triggerall = statetype != A
trigger1 = ctrl

[State -1, shoryu_b]
type = ChangeState
value = 3070
triggerall = palno > 6
triggerall = power >= 2000
triggerall = command = "shoryu_b"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450

;---------------------------------------------------------------------------
; Messatsu Gou Shoryuu Lvl 3
[State -1, shoryu_c]
type = ChangeState
value = 3080
triggerall = palno > 6
triggerall = power >= 3000
triggerall = command = "shoryu_c"
triggerall = statetype != A
trigger1 = ctrl

[State -1, shoryu_c]
type = ChangeState
value = 3080
triggerall = palno > 6
triggerall = power >= 3000
triggerall = command = "shoryu_c"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450

;---------------------------------------------------------------------------
; Shinkuu Tatsumaki Senpuu Kyaku Lvl 1
[State -1, hurricane_a]
type = ChangeState
value = 3100
triggerall = power >= 1000
triggerall = command = "shurricane_a"
triggerall = statetype != A
trigger1 = ctrl

[State -1, hurricane_a]
type = ChangeState
value = 3100
triggerall = power >= 1000
triggerall = command = "shurricane_a"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450

;---------------------------------------------------------------------------
; Shinkuu Tatsumaki Senpuu Kyaku Lvl 2
[State -1, hurricane_b]
type = ChangeState
value = 3110
triggerall = power >= 2000
triggerall = command = "shurricane_b"
triggerall = statetype != A
trigger1 = ctrl

[State -1, hurricane_b]
type = ChangeState
value = 3110
triggerall = power >= 2000
triggerall = command = "shurricane_b"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450

;---------------------------------------------------------------------------
; Shinkuu Tatsumaki Senpuu Kyaku Lvl 3
[State -1, hurricane_c]
type = ChangeState
value = 3120
triggerall = power >= 3000
triggerall = command = "shurricane_c"
triggerall = statetype != A
trigger1 = ctrl

[State -1, hurricane_c]
type = ChangeState
value = 3120
triggerall = power >= 3000
triggerall = command = "shurricane_c"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450

;---------------------------------------------------------------------------
; Shinkuu Hadoken Lvl 1
[State -1, shadoken_x]
type = ChangeState
value = 3200
triggerall = numproj = 0
triggerall = power >= 1000
triggerall = command = "shadoken_x"
triggerall = statetype != A
trigger1 = ctrl

[State -1, shadoken_x]
type = ChangeState
value = 3200
triggerall = numproj = 0
triggerall = power >= 1000
triggerall = command = "shadoken_x"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450

;---------------------------------------------------------------------------
; Shinkuu Hadoken Lvl 2
[State -1, shadoken_y]
type = ChangeState
value = 3210
triggerall = numproj = 0
triggerall = power >= 2000
triggerall = command = "shadoken_y"
triggerall = statetype != A
trigger1 = ctrl

[State -1, shadoken_y]
type = ChangeState
value = 3210
triggerall = numproj = 0
triggerall = power >= 2000
triggerall = command = "shadoken_y"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450

;---------------------------------------------------------------------------
; Shinkuu Hadoken Lvl 3
[State -1, shadoken_z]
type = ChangeState
value = 3220
triggerall = numproj = 0
triggerall = power >= 3000
triggerall = command = "shadoken_z"
triggerall = statetype != A
trigger1 = ctrl

[State -1, shadoken_z]
type = ChangeState
value = 3220
triggerall = numproj = 0
triggerall = power >= 3000
triggerall = command = "shadoken_z"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450


;===========================================================================
;---------------------------------------------------------------------------
; Special Moves

;---------------------------------------------------------------------------
; Light Shoryuken
[State -1, Shoryuken_x]
type = ChangeState
value = 1000
triggerall = command = "shoryuken_x"
triggerall = statetype != A
trigger1 = ctrl

[State -1, Shoryuken_x]
type = ChangeState
value = 1000
triggerall = command = "shoryuken_x"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450

;---------------------------------------------------------------------------
; Medium Shoryuken
[State -1, Shoryuken_y]
type = ChangeState
value = 1010
triggerall = command = "shoryuken_y"
triggerall = statetype != A
trigger1 = ctrl

[State -1, Shoryuken_y]
type = ChangeState
value = 1010
triggerall = command = "shoryuken_y"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450

;---------------------------------------------------------------------------
; Hard Shoryuken
[State -1, Shoryuken_x]
type = ChangeState
value = 1020
triggerall = command = "shoryuken_z"
triggerall = statetype != A
trigger1 = ctrl

[State -1, Shoryuken_x]
type = ChangeState
value = 1020
triggerall = command = "shoryuken_z"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450

;---------------------------------------------------------------------------
; Light Tatsumaki Senpuu Kyaku (Ground)
[State -1, hurricane_a]
type = ChangeState
value = 1100
triggerall = command = "hurricane_a"
triggerall = statetype != A
trigger1 = ctrl

[State -1, hurricane_a]
type = ChangeState
value = 1100
triggerall = command = "hurricane_a"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450

;---------------------------------------------------------------------------
; Medium Tatsumaki Senpuu Kyaku (Ground)
[State -1, hurricane_b]
type = ChangeState
value = 1110
triggerall = command = "hurricane_b"
triggerall = statetype != A
trigger1 = ctrl

[State -1, hurricane_b]
type = ChangeState
value = 1110
triggerall = command = "hurricane_b"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450

;---------------------------------------------------------------------------
; Hard Tatsumaki Senpuu Kyaku (Ground)
[State -1, hurricane_c]
type = ChangeState
value = 1120
triggerall = command = "hurricane_c"
triggerall = statetype != A
trigger1 = ctrl

[State -1, hurricane_c]
type = ChangeState
value = 1120
triggerall = command = "hurricane_c"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450

;---------------------------------------------------------------------------
; Light Tatsumaki Senpuu Kyaku (Air)
[State -1, hurricane_a]
type = ChangeState
value = 1140
triggerall = command = "hurricane_a"
triggerall = statetype = A
trigger1 = ctrl

[State -1, hurricane_a]
type = ChangeState
value = 1140
triggerall = command = "hurricane_a"
triggerall = statetype = A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 600
trigger3 = stateno = 610
trigger4 = stateno = 615
trigger5 = stateno = 620
trigger6 = stateno = 630
trigger7 = stateno = 635
trigger8 = stateno = 640
trigger9 = stateno = 645
trigger10 = stateno = 650
trigger11 = stateno = 655

;---------------------------------------------------------------------------
; Medium Tatsumaki Senpuu Kyaku (Air)
[State -1, hurricane_b]
type = ChangeState
value = 1150
triggerall = command = "hurricane_b"
triggerall = statetype = A
trigger1 = ctrl

[State -1, hurricane_b]
type = ChangeState
value = 1150
triggerall = command = "hurricane_b"
triggerall = statetype = A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 600
trigger3 = stateno = 610
trigger4 = stateno = 615
trigger5 = stateno = 620
trigger6 = stateno = 630
trigger7 = stateno = 635
trigger8 = stateno = 640
trigger9 = stateno = 645
trigger10 = stateno = 650
trigger11 = stateno = 655

;---------------------------------------------------------------------------
; Hard Tatsumaki Senpuu Kyaku (Air)
[State -1, hurricane_c]
type = ChangeState
value = 1160
triggerall = command = "hurricane_c"
triggerall = statetype = A
trigger1 = ctrl

[State -1, hurricane_c]
type = ChangeState
value = 1160
triggerall = command = "hurricane_c"
triggerall = statetype = A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 600
trigger3 = stateno = 610
trigger4 = stateno = 615
trigger5 = stateno = 620
trigger6 = stateno = 630
trigger7 = stateno = 635
trigger8 = stateno = 640
trigger9 = stateno = 645
trigger10 = stateno = 650
trigger11 = stateno = 655

;---------------------------------------------------------------------------
; Light Shakunetsu Hadoken (Ground)
[State -1, fhadoken_x]
type = ChangeState
value = 1330
triggerall = numproj = 0
triggerall = command = "fhadoken_x"
triggerall = statetype != A
trigger1 = ctrl

[State -1, fhadoken_z]
type = ChangeState
value = 1330
triggerall = numproj = 0
triggerall = command = "fhadoken_x"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450

;---------------------------------------------------------------------------
; Medium Shakunetsu Hadoken (Ground)
[State -1, fhadoken_y]
type = ChangeState
value = 1340
triggerall = numproj = 0
triggerall = command = "fhadoken_y"
triggerall = statetype != A
trigger1 = ctrl

[State -1, fhadoken_z]
type = ChangeState
value = 1340
triggerall = numproj = 0
triggerall = command = "fhadoken_y"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450

;---------------------------------------------------------------------------
; Hard Shakunetsu Hadoken (Ground)
[State -1, fhadoken_z]
type = ChangeState
value = 1350
triggerall = numproj = 0
triggerall = command = "fhadoken_z"
triggerall = statetype != A
trigger1 = ctrl

[State -1, fhadoken_z]
type = ChangeState
value = 1350
triggerall = numproj = 0
triggerall = command = "fhadoken_z"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450

;---------------------------------------------------------------------------
; Light Hadoken (Ground)
[State -1, hadoken_x]
type = ChangeState
value = 1300
triggerall = numproj = 0
triggerall = command = "hadoken_x"
triggerall = statetype != A
trigger1 = ctrl

[State -1, hadoken_x]
type = ChangeState
value = 1300
triggerall = numproj = 0
triggerall = command = "hadoken_x"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450

;---------------------------------------------------------------------------
; Medium Hadoken (Ground)
[State -1, hadoken_y]
type = ChangeState
value = 1310
triggerall = numproj = 0
triggerall = command = "hadoken_y"
triggerall = statetype != A
trigger1 = ctrl

[State -1, hadoken_y]
type = ChangeState
value = 1310
triggerall = numproj = 0
triggerall = command = "hadoken_y"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450

;---------------------------------------------------------------------------
; Hard Hadoken (Ground)
[State -1, hadoken_z]
type = ChangeState
value = 1320
triggerall = numproj = 0
triggerall = command = "hadoken_z"
triggerall = statetype != A
trigger1 = ctrl

[State -1, hadoken_z]
type = ChangeState
value = 1320
triggerall = numproj = 0
triggerall = command = "hadoken_z"
triggerall = statetype != A
triggerall = movecontact
trigger1 = ctrl
trigger2 = stateno = 200
trigger3 = stateno = 210
trigger4 = stateno = 215
trigger5 = stateno = 216
trigger6 = stateno = 220
trigger7 = stateno = 222
trigger8 = stateno = 225
trigger9 = stateno = 230
trigger10 = stateno = 240
trigger11 = stateno = 250
trigger12 = stateno = 400
trigger13 = stateno = 410
trigger14 = stateno = 420
trigger15 = stateno = 430
trigger16 = stateno = 440
trigger17 = stateno = 450

;---------------------------------------------------------------------------
; Alpha Counter - Shoryuken
[State -1, Counter]
type = ChangeState
value = 950
triggerall = power >= 1000
triggerall = command = "counter_p"
triggerall = statetype != A
trigger1 = stateno = 150
trigger2 = stateno = 151
trigger3 = stateno = 152

;---------------------------------------------------------------------------
; Alpha Counter - Sweep
[State -1, Counter]
type = ChangeState
value = 960
triggerall = power >= 1000
triggerall = command = "counter_k"
triggerall = statetype != A
trigger1 = stateno = 150
trigger2 = stateno = 151
trigger3 = stateno = 152

;===========================================================================
;---------------------------------------------------------------------------
; Basic Moves
;---------------------------------------------------------------------------
; Glide Fwd
[State -1, Run Fwd]
type = ChangeState
value = 90
triggerall = PalNo > 6
trigger1 = command = "FF"
trigger1 = statetype = S
trigger1 = ctrl

;---------------------------------------------------------------------------
; Glide Back
[State -1, Run Back]
type = ChangeState
value = 95
triggerall = PalNo > 6
trigger1 = command = "BB"
trigger1 = statetype = S
trigger1 = ctrl

;---------------------------------------------------------------------------
; Hop Fwd
[State -1, Run Fwd]
type = ChangeState
value = 100
triggerall = PalNo < 7
trigger1 = command = "FF"
trigger1 = statetype = S
trigger1 = ctrl

;---------------------------------------------------------------------------
; Hop Back
[State -1, Run Back]
type = ChangeState
value = 105
triggerall = PalNo < 7
trigger1 = command = "BB"
trigger1 = statetype = S
trigger1 = ctrl

;---------------------------------------------------------------------------
; Recovery Roll Backward
[State -1, Roll_back]
type = ChangeState
value = 5220
triggerall = alive
triggerall = stateno != 5120
triggerall = stateno != 5291
triggerall = command = "holdback"
triggerall = command = "recovery"
trigger1 = statetype = L

; Recovery Roll Forward
[State -1, Roll_fwd]
type = ChangeState
value = 5230
triggerall = alive
triggerall = stateno != 5120
triggerall = stateno != 5291
triggerall = command = "holdfwd"
triggerall = command = "recovery"
trigger1 = statetype = L

; Ground Recovery
[State -1, Ground_Recovery]
type = ChangeState
value = 5240
triggerall = alive
triggerall = command = "recovery"
trigger1 = stateno = 5100

;---------------------------------------------------------------------------
;===========================================================================
;---------------------------------------------------------------------------
; Overhead Throw
[State -1, Throw]
type = ChangeState
value = 800
triggerall = command = "holdfwd" || command = "holdback"
triggerall = command = "counter_p"
trigger1 = statetype = S
trigger1 = ctrl

;---------------------------------------------------------------------------
; Kick Throw
[State -1, Throw]
type = ChangeState
value = 810
triggerall = command = "holdfwd" || command = "holdback"
triggerall = command = "counter_k"
trigger1 = statetype = S
trigger1 = ctrl

;---------------------------------------------------------------------------
; Hadoken Fake-out
[State -1, Taunt]
type = ChangeState
value = 196
triggerall = PalNo < 7
triggerall = numproj = 0
triggerall = command = "hadoken_s"
trigger1 = statetype = S
trigger1 = ctrl

;---------------------------------------------------------------------------
; Taunt
[State -1, Taunt]
type = ChangeState
value = 195
triggerall = command = "s"
triggerall = command != "holddown"
trigger1 = statetype = S
trigger1 = ctrl

;---------------------------------------------------------------------------
; Stand Light Punch
[State -1, Stand Light Punch]
type = ChangeState
value = 200
triggerall = command = "x"
triggerall = command != "holddown"
trigger1 = statetype = S
trigger1 = ctrl

;---------------------------------------------------------------------------
; Stand Medium Punch
[State -1, Stand Medium Punch]
type = ChangeState
value = 210
triggerall = command = "y"
triggerall = command != "holdfwd"
triggerall = command != "holddown"
trigger1 = statetype = S
trigger1 = ctrl

;---------------------------------------------------------------------------
; Overhead Smash
[State -1, Overhead Smash]
type = ChangeState
value = 215
triggerall = PalNo < 7
triggerall = command = "fwd_y"
triggerall = command != "holddown"
trigger1 = statetype = S
trigger1 = ctrl

;---------------------------------------------------------------------------
; Top Down Chop
[State -1, Chop]
type = ChangeState
value = 216
triggerall = PalNo > 6
triggerall = command = "fwd_y"
triggerall = command != "holddown"
trigger1 = statetype = S
trigger1 = ctrl

;---------------------------------------------------------------------------
; Stand Strong Punch
[State -1, Stand Strong Punch]
type = ChangeState
value = 220
triggerall = command = "z"
triggerall = command != "holdback"
triggerall = command != "holdfwd"
triggerall = command != "holddown"
trigger1 = statetype = S
trigger1 = ctrl

;---------------------------------------------------------------------------
; Stand Elbow Fist
[State -1, Elbow Smash]
type = ChangeState
value = 222
triggerall = command = "back_z"
triggerall = command != "holddown"
trigger1 = statetype = S
trigger1 = ctrl

;---------------------------------------------------------------------------
; Elbow Smash
[State -1, Elbow Smash]
type = ChangeState
value = 225
triggerall = command = "fwd_z"
triggerall = command != "holddown"
trigger1 = statetype = S
trigger1 = ctrl

;---------------------------------------------------------------------------
; Stand Light Kick
[State -1, Stand Light Kick]
type = ChangeState
value = 230
triggerall = command = "a"
triggerall = command != "holddown"
trigger1 = statetype = S
trigger1 = ctrl

;---------------------------------------------------------------------------
; Standing Medium Kick
[State -1, Standing Medium Kick]
type = ChangeState
value = 240
triggerall = command = "b"
triggerall = command != "holdfwd"
triggerall = command != "holddown"
trigger1 = statetype = S
trigger1 = ctrl

;---------------------------------------------------------------------------
; Standing Strong Kick
[State -1, Standing Strong Kick]
type = ChangeState
value = 250
triggerall = command = "c"
triggerall = command != "holddown"
trigger1 = statetype = S
trigger1 = ctrl

;---------------------------------------------------------------------------
; Crouching Light Punch
[State -1, Crouching Light Punch]
type = ChangeState
value = 400
triggerall = command = "x"
triggerall = command = "holddown"
trigger1 = statetype = C
trigger1 = ctrl

;---------------------------------------------------------------------------
; Crouching Medium Punch
[State -1, Crouching Medium Punch]
type = ChangeState
value = 410
triggerall = command = "y"
triggerall = command = "holddown"
trigger1 = statetype = C
trigger1 = ctrl

;---------------------------------------------------------------------------
; Crouching Strong Punch
[State -1, Crouching Strong Punch]
type = ChangeState
value = 420
triggerall = command = "z"
triggerall = command = "holddown"
trigger1 = statetype = C
trigger1 = ctrl

;---------------------------------------------------------------------------
; Crouching Light Kick
[State -1, Crouching Light Kick]
type = ChangeState
value = 430
triggerall = command = "a"
triggerall = command = "holddown"
trigger1 = statetype = C
trigger1 = ctrl

;---------------------------------------------------------------------------
; Crouching Medium Kick
[State -1, Crouching Medium Kick]
type = ChangeState
value = 440
triggerall = command = "b"
triggerall = command = "holddown"
trigger1 = statetype = C
trigger1 = ctrl

;---------------------------------------------------------------------------
; Crouching Strong Kick
[State -1, Crouching Strong Kick]
type = ChangeState
value = 450
triggerall = command = "c"
triggerall = command = "holddown"
trigger1 = statetype = C
trigger1 = ctrl

;---------------------------------------------------------------------------
; Jump Light Punch
[State -1, Jump Light Punch]
type = ChangeState
value = 600
triggerall = command = "x"
trigger1 = statetype = A
trigger1 = ctrl

;---------------------------------------------------------------------------
; Jump Medium Punch
[State -1, Jump Medium Punch]
type = ChangeState
value = 610
triggerall = command = "y"
triggerall = Vel X > 0 || Vel X < 0
trigger1 = statetype = A
trigger1 = ctrl

;---------------------------------------------------------------------------
; Jump-up Medium Punch
[State -1, Jump Medium Punch]
type = ChangeState
value = 615
triggerall = command = "y"
triggerall = Vel X = 0
trigger1 = statetype = A
trigger1 = ctrl

;---------------------------------------------------------------------------
; Jump Strong Punch
[State -1, Jump Strong Punch]
type = ChangeState
value = 620
triggerall = command = "z"
trigger1 = statetype = A
trigger1 = ctrl

;---------------------------------------------------------------------------
; Jump Light Kick
[State -1, Jump Light Kick]
type = ChangeState
value = 630
triggerall = command = "a"
triggerall = Vel X > 0 || Vel X < 0
trigger1 = statetype = A
trigger1 = ctrl

;---------------------------------------------------------------------------
; Jump-up Light Kick
[State -1, Jump Light Kick]
type = ChangeState
value = 635
triggerall = command = "a"
triggerall = Vel X = 0
trigger1 = statetype = A
trigger1 = ctrl

;---------------------------------------------------------------------------
; Jump Medium Kick
[State -1, Jump Medium Kick]
type = ChangeState
value = 640
triggerall = command = "b"
triggerall = Vel X > 0 || Vel X < 0
trigger1 = statetype = A
trigger1 = ctrl

;---------------------------------------------------------------------------
; Jump-up Medium Kick
[State -1, Jump Medium Kick]
type = ChangeState
value = 645
triggerall = command = "b"
triggerall = Vel X = 0
trigger1 = statetype = A
trigger1 = ctrl

;---------------------------------------------------------------------------
; Jump Strong Kick
[State -1, Jump Strong Kick]
type = ChangeState
value = 650
triggerall = command = "c"
triggerall = Vel X > 0 || Vel X < 0
trigger1 = statetype = A
trigger1 = ctrl

;---------------------------------------------------------------------------
; Jump-up Strong Kick
[State -1, Jump Strong Kick]
type = ChangeState
value = 655
triggerall = command = "c"
triggerall = Vel X = 0
trigger1 = statetype = A
trigger1 = ctrl

;---------------------------------------------------------------------------
; Hop Kick
[State -1, Hop Kick]
type = ChangeState
value = 700
triggerall = command = "fwd_b"
triggerall = command != "holddown"
trigger1 = statetype = S
trigger1 = ctrl

;---------------------------------------------------------------------------
;====================================================================
;  AI Code - Doesn't completely override the random action triggers of the mugen CPU, but that is fine, makes it more player like
;====================================================================
; Note random refers to a random num 0-999
;====================================================================

;--------------------------------------------------
;  Shoryuken Anti-Air
;  •  < 45 px      ? Light Shoryuken   (1000)
;  •  45–59 px     ? Medium Shoryuken  (1010)
;  •  60–85 px     ? Heavy Shoryuken   (1020)
;--------------------------------------------------
;--------------------------------------------------
;  1)  Light DP  (close)
;--------------------------------------------------
[State -1, CPU Shoryu light]
type       = ChangeState
value      = 1000                 ; light DP state
triggerall = var(59) > 0          ; CPU only
triggerall = Ctrl                 ; can act
triggerall = Pos Y = 0            ; grounded
trigger1   = P2MoveType = A && P2StateType = A
trigger1   = P2BodyDist X < 45
trigger1   = Random < (40 + 12*AILevel)

;--------------------------------------------------
;  2)  Medium DP  (mid range)
;--------------------------------------------------
[State -1, CPU Shoryuken medium]
type       = ChangeState
value      = 1010                 ; medium DP state
triggerall = var(59) > 0
triggerall = Ctrl
triggerall = Pos Y = 0
trigger1   = P2MoveType = A && P2StateType = A
trigger1   = P2BodyDist X >= 45 && P2BodyDist X < 60
trigger1   = Random < (40 + 12*AILevel)

;--------------------------------------------------
;  3)  Heavy DP  (farther but still AA range)
;--------------------------------------------------
[State -1, CPU Shoryuken heavy]
type       = ChangeState
value      = 1020                 ; heavy DP state
triggerall = var(59) > 0
triggerall = Ctrl
triggerall = Pos Y = 0
trigger1   = P2MoveType = A && P2StateType = A
trigger1   = P2BodyDist X >= 60 && P2BodyDist X < 85
trigger1   = Random < (40 + 12*AILevel)

;--------------------------------------------------
;  Zoning Hadouken (Far)
;  • 40 % chance = Heavy Shakunetsu Hadoken (1350)
;  • 60 % chance = Heavy Hadoken (1320)
;--------------------------------------------------
[State -1, CPU Hadouken Far]
type       = ChangeState
value      = ifelse(Random < 400, 1350, 1320)   ; 40/60 split
triggerall = var(59) > 0
triggerall = Ctrl
triggerall = StateType = S
trigger1   = P2BodyDist X > 170 

trigger1   = Random < (100 + 100*AILevel)
;--------------------------------------------------
;  Zoning Hadouken (Close)
;  • 40 % chance = Light Shakunetsu Hadoken (1330)
;  • 60 % chance = Light Hadoken (1300)
;--------------------------------------------------
[State -1, CPU Hadouken Close]
type       = ChangeState
value      = ifelse(Random < 400, 1330, 1300)   ; 40/60 split
triggerall = var(59) > 0
triggerall = Ctrl
triggerall = StateType = S
trigger1   = P2BodyDist X <= 170
trigger1   = P2BodyDist X >= 100
trigger1   = Random < (100 + 100*AILevel)

;--------------------------------------------------
;  Throw when in close range
;--------------------------------------------------
[State -1, CPU Close Throw]
type       = ChangeState
value      = 800                 ; throw attempt
triggerall = var(59) > 0         ; CPU only
triggerall = Ctrl                ; Ryu has control
triggerall = StateType = S       ; Ryu is standing
triggerall = Pos Y = 0           ; (redundant but explicit)

; ---- opponent must be throwable ------------------------------
triggerall = EnemyNear, StateType = S   ; opponent standing
triggerall = EnemyNear, MoveType != H   ; not in hit-stun / lying

; ---- distance window -----------------------------------------
trigger1   = P2BodyDist X < 25          ; in throw range

; ---- small randomness so it doesn't throw every single time --
trigger1   = Random < (40 + 30*AILevel)  ; 4–28% depending on difficulty
;--------------------------------------------------

;--------------------------------------------------
;  CPU Alpha Counter  – 5 % each
;--------------------------------------------------

;--------------------------------------------------
;  Shoryu AC  (state 950)
;--------------------------------------------------
[State -1, CPU AC Shoryu]
type       = ChangeState
value      = 950
triggerall = var(59) > 0         ; CPU only
triggerall = Power >= 1000       ; need 1 bar
triggerall = StateNo = [150,152] ; exactly the guard-shake states
persistent = 0                   ; one roll per block-string
trigger1   = P2BodyDist X < 50          ; in counter range
trigger1   = Random < 50         ; 5 %  (0–49)
;--------------------------------------------------
;  Sweep AC  (state 960)
;--------------------------------------------------
[State -1, CPU AC Sweep]
type       = ChangeState
value      = 960
triggerall = var(59) > 0
triggerall = Power >= 1000
triggerall = StateNo = [150,152]
persistent = 0
trigger1   = Random >= 50 && Random < 100   ; next 5 %  (50–99)
;==============================================================

