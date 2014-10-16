from random import shuffle, randrange

def maze(w,h):
	vis = [[0] * w + [1] for i in range(h)] + [[1] * (w + 1)] #z enkami oznacis robove 
	#vis = [[0 for i in range(w)] for i in range(h)]
	ver = [["|  "] * w + ['|'] for i in range(h)] + [[]]
	hor = [["+--"] * w + ['+'] for i in range(h + 1)]	

	def dfs(x,y):
		vis[y][x]=1 #pazi x in y
		neb = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
		shuffle(neb)
		for (xx, yy) in neb:
			if vis[yy][xx]: continue
			elif xx == x: hor[max(y,yy)][x] = "+  "
			elif yy == y: ver[y][max(x,xx)] = "   "
			dfs(xx,yy)

	dfs(randrange(w), randrange(h))
	for (a,b) in zip(hor, ver):
		print ("".join(a + ['\n'] + b ))

a,b=map(int, raw_input().strip().split())
maze(a,b)