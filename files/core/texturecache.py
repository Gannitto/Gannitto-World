import pygame

class TextureCache:
	_textures = {}
	
	@classmethod
	def get(cls, path, scale=None):
		key = (path, scale)
		if key not in cls._textures:
			image = pygame.image.load(path)
			if scale:
				image = pygame.transform.scale(image, scale)
			cls._textures[key] = image
		return cls._textures[key]
