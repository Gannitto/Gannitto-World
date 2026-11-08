import pygame

class TextureCache:
	_textures = {}
	
	@classmethod
	def get(cls, path, scale_x=None, scale_y=None, convert_alpha=True, use_cache=True):
		scale = (scale_x, scale_y) if scale_y else (scale_x, scale_x)
		key = (path, scale)
		if key not in cls._textures or not use_cache:
			image = pygame.image.load(path)
			if scale:
				image = pygame.transform.scale(image, scale)
				if convert_alpha:
					image = image.convert_alpha()
				else:
					image = image.convert()
			cls._textures[key] = image
		return cls._textures[key]

load = TextureCache.get
