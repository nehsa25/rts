class GameButton():
	logutils = None

	def __init__(self, rect, text_input, font, base_color, hovering_color):
		self.image = None
		self.font = font
		self.base_color = base_color
		self.hovering_color = hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		self.text_rect = rect

	def update(self, screen):
		screen.blit(self.text, self.text_rect)

	def check_position(self, position):
		if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
			return True
		return False

	def change_color(self, position):
		if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)
