from header import *

from Document import *

class GlyphArea:

	root=[]
	docs=[]

	def __init__(self, parent):
		self.parent = parent
		self.dd = parent.dd
		self.root = parent.root

		self.canvas = Canvas(self.root)

		self.numDocs=self.dd.numDocs
		self.createDocs()

		return

	def draw(self, init=False):
		rootW=self.root.winfo_width()
		rootH=self.root.winfo_height()

		#print canvasW, canvasH

		if init:
			self.canvas.place(x=self.dd.histThickness, y=0, 
				width=rootW-self.dd.histThickness-self.dd.resultListWidth, height=rootH-self.dd.histThickness)
			bg = g.toHex(self.dd.background)
			self.canvas.configure(bg=bg, bd=0, highlightthickness=0)

			
			for d in self.docs:
				d.draw(init=True)
		else:
			for d in self.docs:
				d.draw()

	def createDocs(self):

		for i in range(self.numDocs):
			d = Document(self, rank=i+1)
			#d.printData()
			self.docs.append(d)


	# RANGE CALCULATION
	#    - only includes docs in window range by default
	def getRankRange(self, ignoreWindow=False):
		M = 0
		m = float('inf')

		for d in self.docs:
			if not (ignoreWindow or d.inWindow()): continue

			M = max(M, d.rank)
			m = min(m, d.rank)
		
		return (m, M)

	def getYearRange(self, ignoreWindow=False):
		M = 0
		m = float('inf')

		for d in self.docs:
			if not (ignoreWindow or d.inWindow()): continue
			M = max(M, d.year)

			m = min(m, d.year)
		
		return (m, M)

	def getCitationRange(self, ignoreWindow=False):
		M = 0
		m = float('inf')

		for d in self.docs:
			if not (ignoreWindow or d.inWindow()): continue
			M = max(M, d.citations)

			m = min(m, d.citations)
		
		return (m, M)

	def getWOSRange(self, ignoreWindow=False):
		M = 0
		m = float('inf')

		for d in self.docs:
			if not (ignoreWindow or d.inWindow()): continue
			#if not d.inWindow() and not ignoreWindow: continue

			M = max(M, d.WOS)

			m = min(m, d.WOS)
		
		return (m, M)

	def getHIndexRange(self, ignoreWindow=False):
		M = 0
		m = float('inf')

		for d in self.docs:
			if not (d.inWindow() or ignoreWindow): continue
			M = max(M, d.author_h_index)

			m = min(m, d.author_h_index)
		
		return (m, M)

