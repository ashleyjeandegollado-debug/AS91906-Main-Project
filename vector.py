from mysprite import MySprite
from imagelist import ImageList
import pygame

#snake class
class Snake():
	#direction
	UP=0
	DOWN=1
	RIGHT=2
	LEFT=3
	VECTOR=[(0, -1), (0, 1), (1, 0), (-1, 0)]
	def __init__(self, x, y, w, h, screen, images, direction = UP):
		self._x = x
		self._y = y
		self._w = w
		self._h = h
		self._direction= direction
		self._screen = screen
		self._images= images
	def reset(self):
		self._seg_list = []
		#create tail
		self._seg_list.append(MySprite(self._x, self._y, self._w, self._h, self._images, self._screen))
		#create head
		self._seg_list.append(MySprite(self._x, self._y, self._w, self._h, self._images, self._screen))

	def update(self):
		HEAD = 0
		TAIL = -1
		if self._grow:
			#delete the tail
			#create new head
			self._seg_list.insert(Snake.Head(1, HEAD))
			self._seg_list.insert(Snake.Tail(-1, TAIL))

	def draw(self):
		for segment in self._seg_list:
			segment.draw()