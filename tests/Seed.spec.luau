--!strict
-- Smoke spec for the W0-01 skeleton: gives TestEZ one real spec so the CI test job
-- (enabled once W0-03 provides the test place) executes against real code.

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Seed = require(ReplicatedStorage.Shared.Util.Seed)

return function()
	describe("Seed.rng", function()
		it("is deterministic for the same seed", function()
			local a = Seed.rng(1234)
			local b = Seed.rng(1234)
			expect(a:NextInteger(1, 1_000_000)).to.equal(b:NextInteger(1, 1_000_000))
		end)

		it("diverges for different seeds", function()
			local a = Seed.rng(1234)
			local b = Seed.rng(5678)
			expect(a:NextInteger(1, 1_000_000)).never.to.equal(b:NextInteger(1, 1_000_000))
		end)
	end)
end
