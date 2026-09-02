--!strict
-- Runs TestEZ specs inside the test place via the Open Cloud Luau Execution API (context/02 §7).
-- Env: ROBLOX_API_KEY, ROBLOX_UNIVERSE_ID, ROBLOX_TEST_PLACE_ID.
-- Exits 0 with a skip message when ROBLOX_TEST_PLACE_ID is unset (expected until W0-03).

local net = require("@lune/net")
local process = require("@lune/process")
local serde = require("@lune/serde")
local task = require("@lune/task")

local apiKey = process.env.ROBLOX_API_KEY
local universeId = process.env.ROBLOX_UNIVERSE_ID
local placeId = process.env.ROBLOX_TEST_PLACE_ID

if not placeId or placeId == "" then
	print("ROBLOX_TEST_PLACE_ID not set — skipping in-engine tests (expected until W0-03).")
	process.exit(0)
end
assert(apiKey and apiKey ~= "", "ROBLOX_API_KEY must be set when ROBLOX_TEST_PLACE_ID is set")
assert(
	universeId and universeId ~= "",
	"ROBLOX_UNIVERSE_ID must be set when ROBLOX_TEST_PLACE_ID is set"
)

-- Runs every *.spec ModuleScript under ReplicatedStorage.Tests and errors on any failure,
-- which flips the Luau Execution task to FAILED.
local TEST_SCRIPT = table.concat({
	'local ReplicatedStorage = game:GetService("ReplicatedStorage")',
	"local TestEZ = require(ReplicatedStorage.DevPackages.TestEZ)",
	"local results = TestEZ.TestBootstrap:run({ ReplicatedStorage.Tests }, TestEZ.Reporters.TextReporter)",
	"if results.failureCount > 0 or #results.errors > 0 then",
	'\terror("TestEZ: " .. tostring(results.failureCount) .. " failure(s)")',
	"end",
}, "\n")

local base = `https://apis.roblox.com/cloud/v2/universes/{universeId}/places/{placeId}`
local headers = { ["x-api-key"] = apiKey :: string, ["Content-Type"] = "application/json" }

local createResp = net.request({
	url = `{base}/luau-execution-session-tasks`,
	method = "POST",
	headers = headers :: any,
	body = serde.encode("json", { script = TEST_SCRIPT, timeout = "280s" }),
})
assert(createResp.ok, `failed to create Luau task ({createResp.statusCode}): {createResp.body}`)
local taskPath: string = serde.decode("json", createResp.body).path
print(`created task: {taskPath}`)

-- Poll until terminal state (tasks may run up to 5 minutes).
local final
for _ = 1, 60 do
	task.wait(5)
	local pollResp = net.request({
		url = `https://apis.roblox.com/cloud/v2/{taskPath}`,
		method = "GET",
		headers = headers :: any,
	})
	assert(pollResp.ok, `failed to poll task ({pollResp.statusCode}): {pollResp.body}`)
	final = serde.decode("json", pollResp.body)
	if final.state ~= "QUEUED" and final.state ~= "PROCESSING" then
		break
	end
end

-- Surface the place-side logs either way.
local logsResp = net.request({
	url = `https://apis.roblox.com/cloud/v2/{taskPath}/logs`,
	method = "GET",
	headers = headers :: any,
})
if logsResp.ok then
	local logs = serde.decode("json", logsResp.body)
	if logs.luauExecutionSessionTaskLogs then
		for _, entry in logs.luauExecutionSessionTaskLogs do
			for _, message in entry.messages or {} do
				print(message)
			end
		end
	end
else
	warn(`could not fetch task logs ({logsResp.statusCode})`)
end

print(`task state: {final.state}`)
if final.state ~= "COMPLETE" then
	process.exit(1)
end
