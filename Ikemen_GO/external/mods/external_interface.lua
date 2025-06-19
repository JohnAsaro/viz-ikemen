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

-- function print_r (t, fd) -- From: https://gist.github.com/dpino/af37d70554d157bbee289f489945cce5 
--     fd = fd or io.stdout
--     local function print(str)
--        str = str or ""
--        fd:write(str.."\n")
--     end
--     local print_r_cache={}
--     local function sub_print_r(t,indent)
--         if (print_r_cache[tostring(t)]) then
--             print(indent.."*"..tostring(t))
--         else
--             print_r_cache[tostring(t)]=true
--             if (type(t)=="table") then
--                 for pos,val in pairs(t) do
--                     if (type(val)=="table") then
--                         print(indent.."["..pos.."] => "..tostring(t).." {")
--                         sub_print_r(val,indent..string.rep(" ",string.len(pos)+8))
--                         print(indent..string.rep(" ",string.len(pos)+6).."}")
--                     elseif (type(val)=="string") then
--                         print(indent.."["..pos..'] => "'..val..'"')
--                     else
--                         print(indent.."["..pos.."] => "..tostring(val))
--                     end
--                 end
--             else
--                 print(indent..tostring(t))
--             end
--         end
--     end
--     if (type(t)=="table") then
--         print(tostring(t).." {")
--         sub_print_r(t,"  ")
--         print("}")
--     else
--         sub_print_r(t,"  ")
--     end
--     print()
-- end

-- function savetxt(t, filename)  -- Save table to txt, from: https://gist.github.com/dpino/af37d70554d157bbee289f489945cce5 
--    local fd = io.open(filename, "w")
--    print_r(t, fd)
--    fd:close()
-- end


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
        "UPDATE episodes SET winner = %d WHERE id = %d", winnerteam(), row.id
      )
      )
    end
    if row.cmd == "assertCommand" then
      assertExtCommand(1, tonumber(row.arg))
    else
      print("[Lua] Unknown cmd:", row.cmd)
    end
  end
end)