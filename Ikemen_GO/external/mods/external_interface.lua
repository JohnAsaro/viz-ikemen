debug_timer = 0

function playerstateInfo(p)
	local si_oldid = id()
	if not player(p) then return false end
	local si_ret = string.format(
		'State No: %d (P%d); CTRL: %s; Type: %s; MoveType: %s; Physics: %s; Time: %d',
		stateno(), stateownerplayerno(), boolToInt(ctrl()), statetype(), movetype(), physics(), time()-1
	)
	playerid(si_oldid)
	return si_ret
end

function forceDP(p)
	local si_oldid = id()
	if not player(p) then return false end

	-- Only do this if the player is Ryu and use net-safe Random method
	if name() == "Ryu" then
		changeState(1000)
	end
end


--;===========================================================
--; MATCH LOOP
--;===========================================================
local endFlag = false

--function called during match via config.json CommonLua
function loop()
	hook.run("loop")
    debug_timer = debug_timer + 1
    if debug_timer % 300 == 0 then -- Print every 5 seconds (300 frames at 60 FPS)  
        print(statusInfo(1))
		print(playerstateInfo(1))
        print(statusInfo(2))
		print(playerstateInfo(2))
        debug_timer = 1
		forceDP(1)
    end
	if start == nil then --match started via command line without -loadmotif flag
		if esc() then
			endMatch()
			os.exit()
		end
		if indialogue() then
			dialogueReset()
		end
		togglePostMatch(false)
		toggleDialogueBars(false)
		return
	end
	--credits
	if main.credits ~= -1 and getKey(motif.attract_mode.credits_key) then
		sndPlay(motif.files.snd_data, motif.attract_mode.credits_snd[1], motif.attract_mode.credits_snd[2])
		main.credits = main.credits + 1
		resetKey()
	end
	--music
	start.f_stageMusic()
	--match start
	if roundstart() then
        print("Match started!")
		setLifebarElements({bars = main.lifebar.bars})
		if roundno() == 1 then
			speedMul = 1
			speedAdd = 0
			start.victoryInit = false
			start.resultInit = false
			start.continueInit = false
			start.hiscoreInit = false
			endFlag = false
			if indialogue() then
				dialogueReset()
			end
			if gamemode('training') then
				menu.f_trainingReset()
			end
		end
		start.turnsRecoveryInit = false
		start.dialogueInit = false
	end
	if winnerteam() ~= -1 and player(winnerteam()) and roundstate() == 4 and isasserted("over") then
		--turns life recovery
		start.f_turnsRecovery()
	end
	--dialogue
	if indialogue() then
		start.f_dialogue()
	--match end
	elseif roundstate() == -1 then
		if not endFlag then
			resetMatchData(false)
			endFlag = true
		end
		--victory screen
		if start.f_victory() then
			return
		--result screen
		elseif start.f_result() then
			return
		--continue screen
		elseif start.f_continue() then
			return
		end
		clearColor(motif.selectbgdef.bgclearcolor[1], motif.selectbgdef.bgclearcolor[2], motif.selectbgdef.bgclearcolor[3])
		togglePostMatch(false)
	end
	hook.run("loop#" .. gamemode())
	--pause menu
	if main.pauseMenu then
		playerBufReset()
		menu.f_run()
	else
		main.f_cmdInput()
		--esc / m
		if (esc() or (main.f_input(main.t_players, {'m'}) and not network())) and not start.challengerInit then
			if network() or gamemode('demo') or gamemode('randomtest') or (not config.EscOpensMenu and esc()) then
				endMatch()
			else
				menu.f_init()
			end
		--demo mode
		elseif gamemode('demo') and ((motif.attract_mode.enabled == 1 and main.credits > 0 and not sndPlaying(motif.files.snd_data, motif.attract_mode.credits_snd[1], motif.attract_mode.credits_snd[2])) or (motif.attract_mode.enabled == 0 and main.f_input(main.t_players, {'pal'})) or fighttime() >= motif.demo_mode.fight_endtime) then
			endMatch()
		--challenger
		elseif motif.challenger_info.enabled ~= 0 and gamemode('arcade') then
			if start.challenger > 0 then
				start.f_challenger()
			else
				--TODO: detecting players that are part of P1 team
				--[[for i = 1, #main.t_cmd do
					if commandGetState(main.t_cmd[i], '/s') then
						print(i)
					end
				end]]
				if main.f_input(main.t_players, {'s'}) and main.playerInput ~= 1 and (motif.attract_mode.enabled == 0 or main.credits ~= 0) then
					start.challenger = main.playerInput
				end
			end
		end
	end
end


-- sends inputs to buffer with debug print statements
--function main.f_cmdInput() -- override main.f_cmdInput
--    for i = 1, config.Players do
--        if main.t_pIn[i] > 0 then
--            if i < 3 then  -- Only print for players 1 and 2
--                debug_timer = debug_timer + 1
--                if debug_timer % 300 == 0 then -- Print every 5 seconds (300 frames at 60 FPS)  
--                    print(statusInfo(1))
--                    print(statusInfo(2))
--                    debug_timer = 1
--                end
--            end
--            commandInput(main.t_cmd[i], main.t_pIn[i])
--        end
--    end
--end

-- return bool based on command input, with debug output
--main.playerInput = 1 -- override main.playerInput
--function main.f_input(p, b)
--    for _, pn in ipairs(p) do
--        for _, btn in ipairs(b) do
--            if btn == 'pal' then
--                local palState = main.f_btnPalNo(pn)
--                if palState > 0 then
--                    main.playerInput = pn
--                    print(string.format("DEBUG: Player %d palette input detected (palState: %d)", pn, palState))
--                    return true
--                end
--            elseif commandGetState(main.t_cmd[pn], btn) then
--                main.playerInput = pn
--                print(string.format("DEBUG: Player %d input '%s' detected", pn, btn))
--                return true
--            end
--        end
--    end
--    --print("DEBUG: No input detected for given players/buttons.")
--    return false
--end
