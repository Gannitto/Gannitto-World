import random
from dataclasses import dataclass, field
from PlayerAnimationsData import ITEM_OFFSETS, EYE_ANCHORS_REL, EYE_OFFSETS, BLINK_DURATION

@dataclass
class BlinkAnimation:
	tick: int = 0
	duration: int = BLINK_DURATION

	@property
	def active(self) -> bool:
		return self.tick > 0

	def update(self) -> bool:
		"""Возвращает True, пока анимация активна."""
		if self.tick > 0:
			self.tick -= 1
		return self.tick > 0

	def height(self) -> int:
		# 1..8 -> растёт, 9..16 -> сжимается; максимум 16 px
		t = min(self.tick, self.duration - self.tick + 1)
		return max(0, t * 2)

class PlayerAnimator:
	def __init__(self, player):
		self.player = player
		self.blink = BlinkAnimation()
		self.blink_timer = 0.0
		self.next_blink_in = random.uniform(2.0, 6.0)  # секунды

	def update(self, dt: float):
		# Таймер моргания в секундах, а не в кадрах
		if not self.blink.active:
			self.blink_timer += dt
			if self.blink_timer >= self.next_blink_in:
				self.blink_timer = 0.0
				self.next_blink_in = random.uniform(2.0, 6.0)
				self.blink.tick = self.blink.duration
		else:
			self.blink.update()

	def item_offset(self, direction: str, frame: int) -> tuple[int, int] | None:
		return ITEM_OFFSETS.get(direction, {}).get(frame)

	def eye_anchor(self, direction: str, frame: int) -> tuple[int, int] | None:
		anchors = EYE_ANCHORS_REL.get(direction)
		if anchors is None:
			return None
		return anchors.get(frame, anchors.get(None))

	def draw_blink(self, surface, direction: str, frame: int, center):
		if not self.blink.active or direction not in EYE_ANCHORS_REL:
			return
		anchor = self.eye_anchor(direction, frame)
		if anchor is None:
			return
		cx, cy = center
		ax, ay = cx + anchor[0], cy + anchor[1]
		h = self.blink.height()
		if h <= 0:
			return
		surface.fill(self.player.eye_color, (ax, ay, 8, h))
		second = EYE_OFFSETS.get(direction)
		if second is not None:
			surface.fill(self.player.eye_color, (ax + second[0], ay + second[1], 8, h))

