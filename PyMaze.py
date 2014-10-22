import pygame, random
from pygame.locals import *

CONST_WIDTH = 640 #* 2
CONST_HEIGHT = 480 #* 2
CONST_BOX_WIDTH = 8 
CONST_BOX_HEIGHT = 8

class Labirint:
	def __init__(self, labPodlaga, resitevPodlaga):
		self.state = 'create'
		self.labArr = []
		self.lPodlaga = labPodlaga
		self.lPodlaga.fill((0,0,0,0)) #fill with black
		self.resPodlaga = resitevPodlaga # surface
		self.resPodlaga.fill((0,0,0,0))
		for i in range(CONST_HEIGHT/CONST_BOX_HEIGHT):
			pygame.draw.line(self.lPodlaga, (0,0,0,255), (0, i * CONST_BOX_HEIGHT), (CONST_WIDTH, i * CONST_BOX_HEIGHT))
			for j in range(CONST_WIDTH/CONST_BOX_WIDTH):
				self.labArr.append(0x0000)
				if (i == 0):
					pygame.draw.line(self.lPodlaga, (0,0,0,255), (j * CONST_BOX_WIDTH, 0), (j * CONST_BOX_WIDTH, CONST_HEIGHT))

		pygame.draw.rect(self.resPodlaga, (0,0,255,255), Rect(0,0,CONST_BOX_WIDTH, CONST_BOX_HEIGHT))
		pygame.draw.rect(self.resPodlaga, (0,0,0,0), Rect((CONST_WIDTH-CONST_BOX_WIDTH),(CONST_HEIGHT - CONST_HEIGHT),CONST_BOX_WIDTH, CONST_BOX_HEIGHT))
		self.vseCelice = (CONST_HEIGHT/CONST_BOX_HEIGHT) * (CONST_WIDTH/ CONST_BOX_WIDTH)
		self.stackCelic = []
		self.trenutnaCelica = random.randint(0, self.vseCelice-1)
		self.obiskaneCelice = 1
		self.smeri = [(-1,0), (0,1), (1,0), (0,-1)]

	def update(self):
		if self.state == 'idle':
			print "IDLE"
		elif self.state == 'create':
			#while loop
			if self.obiskaneCelice >= self.vseCelice:
				self.trenutnaCelica = 0 #pos top-left
				self.stackCelic = []
				self.state = 'solve'
				return
			moved = False
			while(self.obiskaneCelice < self.vseCelice):
				x = self. trenutnaCelica %(CONST_WIDTH/CONST_BOX_WIDTH)
				y = self. trenutnaCelica /(CONST_WIDTH/CONST_BOX_WIDTH)
				#find all neighbors with walls
				sosedje = []
				for i in range(len(self.smeri)):
					nx = x + self.smeri[i][0]
					ny = y + self.smeri[i][1]

					#Check the borders
					if ((nx >= 0) and (ny >= 0) and (nx < CONST_WIDTH/CONST_BOX_WIDTH) and (ny < CONST_HEIGHT/CONST_BOX_HEIGHT)):
						if (self.labArr[(ny * CONST_WIDTH/CONST_BOX_WIDTH + nx )] & 0x000F) == 0: #visited -> checked in binary
							nidx = ny * CONST_WIDTH/CONST_BOX_WIDTH + nx 
							sosedje.append((nidx, 1<<i))
				if len(sosedje) > 0:
					#chose random neighbor
					idx = random.randint(0, len(sosedje)-1)
					nidx, direction = sosedje[idx]
					#knock down the wall
					dx = x * CONST_BOX_WIDTH
					dy = y * CONST_BOX_HEIGHT

					b = CONST_BOX_HEIGHT

					if direction & 1: # if direction is West
						self.labArr[nidx] |= (4) # if direction is East
						pygame.draw.line(self.lPodlaga, (0,0,0,0), (dx, dy + b/8), (dx, dy +(b*7/8)))
					elif direction & 2: # if direction is South
						self.labArr[nidx] |= (8) # if direction is North
						pygame.draw.line(self.lPodlaga, (0,0,0,0), (dx+b/8, dy+b), (dx+(b*7/8), dy+b))
					elif direction & 4: # if direction is East
						self.labArr[nidx] |= (1) # if direction is West
						pygame.draw.line(self.lPodlaga, (0,0,0,0), (dx+b, dy+b/8), (dx+b, dy+(b*7/8)))
					elif direction & 8: # if direction is North
						self.labArr[nidx] |= (2) # if direction is South
						pygame.draw.line(self.lPodlaga, (0,0,0,0), (dx+b/8, dy), (dx+(b*7/8), dy))

					self.labArr[self.trenutnaCelica] |= direction
					self.stackCelic.append(self.trenutnaCelica)
					self.trenutnaCelica = nidx
					self.obiskaneCelice = self.obiskaneCelice + 1
					moved = True
				else:
					self.trenutnaCelica = self.stackCelic.pop()

		elif self.state == 'solve':
			if self.trenutnaCelica == (self.vseCelice-1):
				self.state = 'reset'
				return
			moved = False
			while (moved == False):
				x = self. trenutnaCelica %(CONST_WIDTH/CONST_BOX_WIDTH)
				y = self. trenutnaCelica /(CONST_WIDTH/CONST_BOX_WIDTH)

				sosedje = []
				directions = self.labArr[self.trenutnaCelica] & 0xF
				for i in range(len(self.smeri)):
					if (directions & (1 << i)) > 0:
						nx = x + self.smeri[i][0]
						ny = y + self.smeri[i][1]
						#Check the borders
						if ((nx >= 0) and (ny >= 0) and (nx < CONST_WIDTH/CONST_BOX_WIDTH) and (ny < CONST_HEIGHT/CONST_BOX_HEIGHT)):
							nidx = ny * CONST_WIDTH/CONST_BOX_WIDTH + nx 
							if ((self.labArr[nidx] & 0xFF00) == 0): #check there's no bactrack or solution
								sosedje.append((nidx,1 << i))
				if (len(sosedje) > 0):
					idx = random.randint(0, len(sosedje)-1)
					nidx, direction = sosedje[idx]
					dx = x * CONST_BOX_WIDTH
					dy = y * CONST_BOX_HEIGHT
					#set the opposite wall of the neighbor
					if direction & 1:
						self.labArr[nidx] |= (4 << 12)
					elif direction & 2:
						self.labArr[nidx] |= (8 << 12)
					elif direction & 4:
						self.labArr[nidx] |= (1 << 12)
					elif direction & 8:
						self.labArr[nidx] |= (2 << 12)
					#Draw a green square
					pygame.draw.rect(self.resPodlaga, (0,255,0,255), Rect(dx,dy, CONST_BOX_WIDTH, CONST_BOX_HEIGHT))
					self.labArr[self.trenutnaCelica] |= direction << 8

					self.stackCelic.append(self.trenutnaCelica)
					self.trenutnaCelica = nidx
					moved = True
				else:
					#Draw red square
					pygame.draw.rect(self.resPodlaga, (255,0,0,255), Rect((x*CONST_BOX_WIDTH), (y*CONST_BOX_HEIGHT), CONST_BOX_WIDTH, CONST_BOX_HEIGHT))
					 # Not a solution, so AND the bit to take away the solution bit
					self.labArr[self.trenutnaCelica] &= 0xF0FF
					self.trenutnaCelica = self.stackCelic.pop()
		elif self.state == 'reset':
			self.__init__(self.lPodlaga,self.resPodlaga)





	def narisi(self, screen):
		screen.blit(self.resPodlaga, (0,0))
		screen.blit(self.lPodlaga, (0,0))


#Main function
def main():
	pygame.init() #initialization

	#Create display and set dimensions on 640X480
	screen = pygame.display.set_mode((CONST_WIDTH,CONST_HEIGHT))
	pygame.display.set_caption('Labirint')
	pygame.mouse.set_visible(0)

	#Background
	bacground =  pygame.Surface(screen.get_size()) #get size of screen
	bacground = bacground.convert()
	bacground.fill((255,255,255))

	labPodlaga = pygame.Surface(screen.get_size())
	labPodlaga = labPodlaga.convert_alpha() #give some alpha values
	labPodlaga.fill((0,0,0,0))
	resitevPodlaga = pygame.Surface(screen.get_size())
	resitevPodlaga = labPodlaga.convert_alpha()
	resitevPodlaga.fill((0,0,0,0))

	lab = Labirint(labPodlaga, resitevPodlaga)


	screen.blit(bacground, (0,0))
	pygame.display.flip()
	clock =  pygame.time.Clock()

	while True:
		clock.tick(60) #60 fps
		for event in pygame.event.get(): #goes thru events
			#quits if escape is clicked
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					return
		lab.update()
		screen.blit(bacground, (0,0))
		lab.narisi(screen)
		pygame.display.flip()

	#return 


if __name__ == '__main__': main() #when python starts start main funciton