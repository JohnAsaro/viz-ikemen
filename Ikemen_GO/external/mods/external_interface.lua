-- external_interface.lua
local sqlite3 = require("sqlite3")
local DB_PATH = "external/mods/bridge.db"

-- Open the DB (will create if it doesn't exist)
local db, err = sqlite3.new()
assert(db, err)
assert(db:open(DB_PATH, { cache = "shared" }))

-- Action Space (adjust if not using kfm)
local action_space = {
  [0] = true, [1] = true, [2] = true, [3] = true, [4] = true, [5] = true, [6] = true, [7] = true, [8] = true, [9] = true, [10] = true,
  [11] = true, [12] = true, [13] = true, [14] = true, [15] = true, [16] = true, [17] = true, [18] = true, [19] = true, [20] = true,
  [21] = true, [22] = true, [23] = true, [24] = true, [25] = true, [26] = true, [27] = true, [28] = true, [29] = true, [30] = true,
  [31] = true, [32] = true, [33] = true, [34] = true, [35] = true, [36] = true, [37] = true, [38] = true, [39] = true, [40] = true,
  [41] = true, [42] = true, [43] = true, [44] = true, [45] = true
}
-- [Functions]

-- Info
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

function debugInfo()
  
  print("=== Player Tables ===")
  print("main.t_players:")
  for i, v in ipairs(main.t_players) do
    print("  [" .. i .. "] = " .. tostring(v))
  end

  print("main.t_remaps:")
  for i, v in ipairs(main.t_remaps) do
    print("  [" .. i .. "] = " .. tostring(v))
  end

  print("main.t_pIn:")
  for i, v in ipairs(main.t_pIn) do
    print("  [" .. i .. "] = " .. tostring(v))
  end

  print("main.t_lastInputs:")
  for i, v in ipairs(main.t_lastInputs) do
    print("  [" .. i .. "] = table (empty)")
  end

  print("main.t_cmd:")
  for i, v in ipairs(main.t_cmd) do
    print("  [" .. i .. "] = " .. tostring(v))
  end
end

-- Action Handlers

function forceAction(p, data)
	if not player(p) then return false end

	if name() == "Kung Fu Man" then
		changeState(data)
	end
end

function assertExtCommand(p, arg)
	if not player(p) then return false end

	if name() == "Kung Fu Man" then
			mapSet('ext_command', arg)
	end
end
  
-- End [Functions]

-- Per-frame polling loop
hook.add("loop", "external_interface", function()
  
  local rows, qerr = db:query([[
    SELECT reset, pause FROM environment;
  ]])

  for _, row in ipairs(rows) do
    if row.reset == 1 then
      reload() -- Reload the game if asserted from the DB
      db:query("UPDATE environment SET reset = 0")
    end
    if row.pause == 1 then
      togglePause() -- Toggle pause if asserted from the DB
      db:query("UPDATE environment SET pause = 0")
    end
  end

  local rows, qerr = db:query([[
    SELECT id, done FROM buffer;
  ]])

  for _, row in ipairs(rows) do
    if row.done == -1 then -- Buffer not logged yet
      logScreenBuffer() -- Use log_entry.go, log screen buffer to db to replace placeholder entry
      -- Fun fact: This is actually faster than updating the -1 entry directly
    end
  end

  local rows, qerr = db:query([[
    SELECT id, cmd, arg, winner FROM episodes WHERE done = 0;
  ]])

  if not rows then
    if qerr ~= "no rows" then print("[Lua][DB error]", qerr) end
    return
  end

  for _, row in ipairs(rows) do
    if roundover() then 
      db:query(
        string.format(
        "UPDATE episodes SET winner = %d WHERE id = %d", winnerteam(), row.id -- set winner if round is over
      )
      )
    end
    if row.cmd == "assertCommand" and action_space[row.arg] then -- make KFM do the action corresponding to the number arg
      assertExtCommand(1, row.arg)
    else
      print("[Lua] Unknown cmd:", row.cmd)
    end
  end

end)