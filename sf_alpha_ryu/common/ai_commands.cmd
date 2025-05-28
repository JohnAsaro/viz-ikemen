;====================================================================
;  AI-ONLY COMMAND FILE  (Ryu)
;  These State -1 blocks are appended to commands.cmd via
;     cmd = common/commands.cmd, common/ai_commands.cmd
;  in the .def file.  All human-input blocks remain in commands.cmd,
;  and every block here starts with  var(59) > 0  so ONLY the CPU
;  can use them.
;====================================================================

;--------------------------------------------------
;  Anti-air Shoryuken
;--------------------------------------------------
[State -1, CPU Shoryu AA]
type       = ChangeState
value      = 1000                 ; light dp 
triggerall = var(59) > 0         ; CPU only
triggerall = Ctrl                ; must have control
trigger1   = P2MoveType = A      ; opponent is attacking
trigger1   = P2StateType = A     ; …and airborne
trigger1   = P2BodyDist X < 45
trigger1   = Random < (40 + 5*AILevel)

;--------------------------------------------------
;  Zoning Hadouken
;--------------------------------------------------
[State -1, CPU Hadouken]
type       = ChangeState
value      = 1300                 ; light fireball
triggerall = var(59) > 0
triggerall = Ctrl
triggerall = StateType = S
trigger1   = P2BodyDist X > 120
trigger1   = Random < (10 + 8*AILevel)

;--------------------------------------------------
;  Walk forward  (fallback so AI never freezes)
;--------------------------------------------------
[State -1, CPU WalkFwd]
type       = ChangeState
value      = 20                  ; walk-forward state
triggerall = var(59) > 0
trigger1   = 1                   ; always true (keep last in file)

;=================  end of ai_commands.cmd  =========================
