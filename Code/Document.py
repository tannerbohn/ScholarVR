from header import *

from fileIO import *



class Document:

	hidden=False

	def __init__(self, parent, rank):

		self.root = parent.root
		self.parent=parent
		self.canvas = parent.canvas
		self.dd = parent.dd

		self.rank=rank
		self.author = [self.randomName()]
		self.year = random.randint(1930, 2015)
		
		self.publisher = self.randomPublisher()
		self.WOS = random.randint(0, 500) 
		self.author_h_index = int(random.randint(0, 100))# * (self.WOS/500.0))

		self.citations = random.randint(0, 100) #1000/rank
		self.title = self.randomTitle()

		#self.loc=(random.random(), random.random())#(0.0,0.0)
		

		#self.draw()

		return


	def draw(self, init=False):
		canvasW=self.dd.glyphAreaWidth
		canvasH=self.dd.glyphAreaHeight


		self.getLoc()
		


		if not self.inWindow() and not init:
			if self.hidden:
				return
			else:
				self.hidden = True
				self.loc = (-100, -100)

		if self.inWindow() and self.hidden:
			self.hidden = False


		self.getRadius()

		self.getAngle2()
		self.getAngle3()




		# radius : rank
		# angle 1 : WOS
		# angle 2 : author h-index?

		x = 1.0*canvasW*self.loc[0]
		y = 1.0*canvasH*self.loc[1]

		r = self.radius



		
		r3 = r*3./3
		x0p, y0p = x-r3, y-r3
		x1p, y1p = x+r3, y+r3
		fill = g.toHex(g.shadeN([self.dd.background, self.dd.glyphR3Colour], [0,1], self.dd.glyphOpacity))
		fracFill = g.toHex(self.dd.glyphR3Colour)

		if init:
			self.circle3Index = self.canvas.create_oval(x0p, y0p, x1p, y1p,
				fill=fill, width=0, activewidth=0, tags="circle3")

			self.circle3FracIndex = self.canvas.create_arc(x0p, y0p, x1p, y1p,
				fill=fracFill, width=0, activewidth=0, tags="circle3",outline=fracFill,
				extent=-1.*self.angle3, start=90)
		else:

			self.canvas.coords(self.circle3Index, x0p, y0p, x1p, y1p)
			self.canvas.coords(self.circle3FracIndex, x0p, y0p, x1p, y1p)
			self.canvas.itemconfig(self.circle3FracIndex, extent=-1.*self.angle3)



		r2 = r*2./3
		x0p, y0p = x-r2, y-r2
		x1p, y1p = x+r2, y+r2
		fill =  g.toHex(g.shadeN([self.dd.background, self.dd.glyphR2Colour], [0,1], self.dd.glyphOpacity))
		fracFill = g.toHex(self.dd.glyphR2Colour)
		if init:
			self.circle2Index = self.canvas.create_oval(x0p, y0p, x1p, y1p,
				fill=fill, width=0, activewidth=0, tags="circle2")
			self.circle2FracIndex = self.canvas.create_arc(x0p, y0p, x1p, y1p,
				fill=fracFill, width=0, activewidth=0, tags="circle2", outline=fracFill,
				extent=-1.*self.angle2, start=90)
		else:
			self.canvas.coords(self.circle2Index, x0p, y0p, x1p, y1p)
			self.canvas.coords(self.circle2FracIndex, x0p, y0p, x1p, y1p)
			self.canvas.itemconfig(self.circle2FracIndex, extent=-1.*self.angle2)



		r1 = r*1./3
		x0p, y0p = x-r1, y-r1
		x1p, y1p = x+r1, y+r1
		fill = g.toHex(self.dd.glyphR1Colour)
		if init:
			self.circle1Index = self.canvas.create_oval(x0p, y0p, x1p, y1p,
				fill=fill, width=0, activewidth=0, tags="circle1")
			#self.circle1FracIndex = self.canvas.create_arc(x0p, y0p, x1p, y1p,
			#	fill="black", width=0, activewidth=0, tags="circle1", extent=-180, start=90)
		else:
			self.canvas.coords(self.circle1Index, x0p, y0p, x1p, y1p)



		inBounds = self.inWindow()
		
		'''
		if inBounds:
			self.canvas.itemconfig(self.circle1Index, fill="white")
		else:
			self.canvas.itemconfig(self.circle1Index, fill="red")
		'''

		if init:
			self.setBinds()

		return

	def setBinds(self):
		#self.canvas.tag_bind(self.circle1Index, '<Button-1>',
		#		(lambda event: self.printData()))

		# print info on enter/hover
		self.canvas.tag_bind(self.circle3Index, '<Enter>',
				(lambda event, widget="circle3": self.widgetEnter(event, widget)))
		self.canvas.tag_bind(self.circle3FracIndex, '<Enter>',
				(lambda event, widget="circle3": self.widgetEnter(event, widget)))
		self.canvas.tag_bind(self.circle2Index, '<Enter>',
				(lambda event, widget="circle2": self.widgetEnter(event, widget)))
		self.canvas.tag_bind(self.circle2FracIndex, '<Enter>',
				(lambda event, widget="circle2": self.widgetEnter(event, widget)))
		self.canvas.tag_bind(self.circle1Index, '<Enter>',
				(lambda event, widget="circle1": self.widgetEnter(event, widget)))
	

	def widgetEnter(self, event, name):

		if name in ["circle3", "circle2", "circle1"]:
			self.parent.parent.resultList.setText(self.dataStr())

	def randomName(self):
		constonants = 'bcdfghjklmnprstvwxz'
		vowels = 'aeiouy'

		FirstNameLen = random.randint(2, 5)
		LastNameLen = random.randint(2, 5)

		Fname=""
		for i in range(FirstNameLen):
			Fname=Fname+(constonants[random.randint(0, len(constonants)-1)])
			Fname=Fname+(vowels[random.randint(0, len(vowels)-1)])

		Lname=""
		for i in range(LastNameLen):
			Lname=Lname+(constonants[random.randint(0, len(constonants)-1)])
			Lname=Lname+(vowels[random.randint(0, len(vowels)-1)])

		return Fname.capitalize()+' '+Lname.capitalize()

	def randomPublisher(self):
		N1 = ['Science', 'Physics', 'Mathematics', 'Medicine', 'Computer Science', 'Nature']
		N2 = ['Journal', 'Papers']

		r = random.randint(0, 2)

		if r == 0:
			a = N1[random.randint(0, len(N1)-1)]
			b = N2[random.randint(0, len(N2)-1)]

			return a+' '+b
		elif r == 1:
			a = N1[random.randint(0, len(N1)-1)]
			b = N2[random.randint(0, len(N2)-1)]

			return b+' of '+a
		elif r == 2:
			a = N1[random.randint(0, len(N1)-1)]
			b = N2[random.randint(0, len(N2)-1)]
			c = N1[random.randint(0, len(N1)-1)]

			return b+' of '+a+' and '+c

	def randomTitle(self):
		nameData = jsonLoad('naming.json')

		scienceWords = nameData['scienceWords']
		adjectives = nameData['adjectives']
		verbs = nameData['verbs']

		s = scienceWords[random.randint(0, len(scienceWords)-1)]
		a = adjectives[random.randint(0, len(adjectives)-1)]
		v = verbs[random.randint(0, len(verbs)-1)]

		return v+' '+a+' '+s

	def dataStr(self):
		data=[]

		data.append("Title: %s"%self.title)
		data.append("Author: %s"%self.author)
		data.append("Author h-index: %s"%self.author_h_index)
		data.append("Year: %s"%self.year)
		data.append("Publisher: %s"%self.publisher)
		data.append("Citations: %s"%self.citations)
		data.append("WOS: %s"%self.WOS)
		data.append("Rank: %s"%self.rank)

		

		return '\n'.join(data)

	def getRadius(self):
		rank = self.rank

		minRank, maxRank = self.parent.getRankRange(ignoreWindow=False)
	
		if maxRank == minRank:
			self.radius = self.dd.maxGlyphR
			return


		rank_p = 1.0 - 1.0*(rank - minRank)/(maxRank - minRank)
		#print rank_p*rank_p
	

		self.radius = max(self.dd.maxGlyphR * rank_p*rank_p, self.dd.minGlyphR)

	def getLoc(self):

		# location depends on current histogram windows
		# if a doc is not in the window, it should be outside of the visible area
		(yMin,yMax),(xMin,xMax) = self.parent.getCitationRange(ignoreWindow=False), self.parent.getYearRange(ignoreWindow=False)

		xLoc = 0
		yLoc = 0


		#self.loc=(random.random(), random.random())#(0.0,0.0)

		#print yMin, yMax, xMin, xMax

		#print "xMax, xMin = ", xMax, xMin
		if xMax != xMin:
			xLoc = 1.0 * (self.year - xMin)/(xMax-xMin)
		else:
			xLoc = 0.5

		if yMax != yMin:
			yLoc = 1.0 - 1.0 * (self.citations - yMin)/(yMax-yMin)
		else:
			yLoc = 0.5

		#print xLoc, yLoc

		self.loc=(xLoc, yLoc)

	def getAngle2(self):
		# measures h-index of author 

		(minHI, maxHI) = self.parent.getHIndexRange(ignoreWindow=False)

		if maxHI != 0.0:
			self.angle2 = 359.9 * (1.0 * self.author_h_index / maxHI)
		else:
			self.angle2 = 359.9

	def getAngle3(self):
		# measures WOS score

		(minWOS, maxWOS) = self.parent.getWOSRange(ignoreWindow=False)

		if maxWOS != 0.0:
			self.angle3 = 359.9 * (1.0 * self.WOS / maxWOS)
		else:
			self.angle3 = 359.9

		#if self.angle3 > 360.0:
		#	print self.angle3, self.hidden


	def inWindow(self):

		yMin = self.parent.parent.yHist.windowMin#totalMin#
		yMax = self.parent.parent.yHist.windowMax#totalMax#

		xMin = self.parent.parent.xHist.windowMin#totalMin #
		xMax = self.parent.parent.xHist.windowMax#totalMax #

		inYear = self.year >= xMin and self.year <= xMax
		inCite = self.citations >= yMin and self.citations <= yMax

		inBounds = inYear and inCite

		return inBounds