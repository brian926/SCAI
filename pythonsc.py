#!/usr/bin/env python3

import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2 import NEXUS, PROBE, PYLON, ASSIMLATOR, ASSIMLATOR, GATEWAY, CYBERNETICSCORE, STALKER

Class SentdeBot(sc2.BotAI):
	async def on_step(self, iteration):

		# What to do every step
		# In SCAI/bot_ai.py
		await self.distriute_workers()
		await self.build_workers()
		await self.build_pylons()
		await self.expand()
		await self.build_assimilator()
		await self.offensive_force_buildings()
		await self. build_offensive_force()

	async def build_workers(self):
		for nexus in self.units(NEXUS).ready.noqueue:
			if self.can_afford(PROBE):
				await self.do(nexus.train(PROBE))

	async def build_pylons(self):
		if self.supply_left < 5 and not self.already_pending(PYLON):
			nexuses = self.units(NEXUS).ready
			if nexuses.exists:
				if self.can_afford(PYLON):
					await self.build(PYLON, near = nexuses.first)

	async def expand(self):
		if self.units(NEXUS).amount < 2 and self.can_afford(NEXUS):
			await self.exand_now()

	async def build_assimilator(self):
		for nexus in self.units(NEXUS).ready:
			vaspenes = self.state.verspene_geyser.closer_than(20.0, nexus)
			for vaspene in vaspenes:
				if not self.can_afford(ASSIMLATOR):
					break
				worker = self.select_build_worker(vaspene.position)
				if worker is None:
					break
				if not self.units(ASSIMLATOR).closer_than(1.0, vaspene).exists:
					await self.do(worker.build(ASSIMLATOR, vaspene))

	async def offensive_force_buildings(self):
		if self.units(PYLON).ready.exists:
			pylon = self.units(PYLON).ready.random
			if self.units(GATEWAY).ready.exists:
				if not self.units(CYBERNETICSCORE):
					if self.can_afford(CYBERNETICSCORE) and not self.already_pending(CYBERNETICSCORE):
						await self.build(CYBERNETICSCORE, near = plyon)
			else:
				if self.can_afford(GATEWAY) and not self.already_pending(GATEWAY):
					await self.build(GATEWAY, near = pylon)

	async def build_offensive_force(self):
		for gw in self.units(GATEWAY).ready.noqueue:
			if self.can_afford(STALKER) and self.supply_left > 0:
				await self.do(gw.train(STALKER))

run_game(maps.get("AbyssaReefLE"), [
	Bot(Race.Protoss, SentdeBot()),
	Computer(Race.Terran, Difficulty.Easy)
], realtime=True)