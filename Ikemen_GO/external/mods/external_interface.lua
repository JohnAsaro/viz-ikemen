-- external_interface.lua
local sqlite3 = require("sqlite3")
local DB_PATH = "external/mods/bridge.db"
 
-- Open the DB (will create if it doesn't exist)
local db, err = sqlite3.new()
assert(db, err)
assert(db:open(DB_PATH, { cache = "shared" }))

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

-- Action Handlers
function forceAction(p, data)
	if not player(p) then return false end

	if name() == "Ryu" then
		changeState(data)
	end
end

function forceDP(p)
	if not player(p) then return false end

	if name() == "Ryu" then
		changeState(1000)
	end
end

-- End [Functions]

-- Per-frame polling loop
hook.add("loop", "external_interface", function()
  local rows, qerr = db:query([[
    SELECT id, cmd, arg FROM commands WHERE done = 0;
  ]])
  if not rows then
    if qerr ~= "no rows" then print("[Lua][DB error]", qerr) end
    return
  end

  for _, row in ipairs(rows) do
    if row.cmd == "forceAction" then
      forceAction(1, tonumber(row.arg))
    else
      print("[Lua] Unknown cmd:", row.cmd)
    end
    --db:execute(string.format(  --doesnt work, I need to find another way to do this
    --  "UPDATE commands SET done = 1 WHERE id = %d", row.id
    --)
  --)
  end
end)
