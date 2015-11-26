from header import *

from Document import *

class GlyphArea:

	root=[]
	docs=[]

	pausePanning = False

	def __init__(self, parent):
		self.parent = parent
		self.dd = parent.dd
		self.root = parent.root

		self.canvas = Canvas(self.root)

		self.numDocs=self.dd.numDocs
		self.createDocs()


		self.focus = []

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

			# now draw links between docs
			self.drawLinks(init=True)

			# draw legend
			# - two small squares and two small labels
			x0, y0 = 0,0
			x1, y1 = 20, 20
			fill1, fill2 = g.toHex(self.dd.glyphR2Colour), g.toHex(self.dd.glyphR3Colour)
			legend1ColourIndex = self.canvas.create_rectangle(x0, y0, x1, y1, tag="legend",
				fill=fill1, width=2, activewidth=2)
			lx, ly = x1, 0.5*(y0+y1)#0.5*(x0+x1)+25, 0.5*(y0+y1)+10
			self.legend1LabelIndex = self.canvas.create_text(lx+33, ly,tag="legend_label",
				text='h-index', font=(g.mainFont, 12, "normal"),
				fill=g.toHex(self.dd.labelColour))

			legend2ColourIndex = self.canvas.create_rectangle(x0, y0+30, x1, y1+30, tag="legend",
				fill=fill2, width=2, activewidth=2)
			self.legend2LabelIndex = self.canvas.create_text(lx+20, ly+30,tag="legend_label",
				text='WOS', font=(g.mainFont, 12, "normal"),
				fill=g.toHex(self.dd.labelColour))

			self.addBinds()

		else:
			for d in self.docs:
				d.draw()

			self.drawLinks(init=False)


	def drawLinks(self, init=False):
	
		canvasWidth = self.dd.glyphAreaWidth
		canvasHeight = self.dd.glyphAreaHeight

		if init:
			self.citeLinks=[]
			# loop over all doc pairs


			for i in range(self.numDocs):
				d1 = self.docs[i]
				for j in range(i+1, self.numDocs):
					d2 = self.docs[j]

					if d1.hasCiteLink(d2):
						# create a cite link
						x0, y0 = d1.loc; x0 *= canvasWidth; y0 *= canvasHeight
						x1, y1 = d2.loc; x1 *= canvasWidth; y1 *= canvasHeight

						fill = g.toHex(self.dd.citeLinkColour)
						index = self.canvas.create_line(x0, y0, x1, y1,
							fill=fill, width=2, tag="cite_link")

						self.citeLinks.append({"start":d1, "end":d2, "canvas_index":index})

						#print "here", x0, x1
			self.canvas.tag_lower("cite_link")

		else:
			
			for l in self.citeLinks:
				x0, y0 = l['start'].loc; x0 *= canvasWidth; y0 *= canvasHeight
				x1, y1 = l['end'].loc; x1 *= canvasWidth; y1 *= canvasHeight
				self.canvas.coords(l['canvas_index'], x0, y0, x1, y1)

	def addBinds(self):
		# panning
		self.canvas.bind('<Button-1>', self.startDrag)
		self.canvas.bind('<B1-Motion>', self.onDrag)
		self.canvas.bind('<ButtonRelease-1>', self.endDrag)

		# zooming
		self.canvas.bind('<4>', lambda event : self.zoom('in', event))
		self.canvas.bind('<5>', lambda event : self.zoom('out', event))


	# PANNING
	def startDrag(self, event):
		self.dragInit = (event.x, event.y)
		self.cursorPos = (event.x, event.y)

	def endDrag(self, event):
		self.pausePanning = False
		self.root.update()

	def onDrag(self, event):
		#if not self.pausePanning:
			# shift all objects on canvas
		delta = (event.x - self.cursorPos[0], event.y - self.cursorPos[1])

		self.cursorPos = (event.x, event.y)

		# use delta to update histogram ranges
		# need to take into account the size of the window
		yHWMin = self.parent.yHist.windowMin
		yHWMax = self.parent.yHist.windowMax
		yHTMin = self.parent.yHist.totalMin
		yHTMax = self.parent.yHist.totalMax

		xHWMin = self.parent.xHist.windowMin
		xHWMax = self.parent.xHist.windowMax
		xHTMin = self.parent.xHist.totalMin
		xHTMax = self.parent.xHist.totalMax

		yZoom = (yHWMax - yHWMin)/(yHTMax - yHTMin)
		xZoom = (xHWMax - xHWMin)/(xHTMax - xHTMin)
		dx = -1.0*delta[0] * xZoom
		dy = -1.0*delta[1] * yZoom


		self.parent.yHist.moveByPix((0, 1.0*dy), "both")
		
		self.parent.xHist.moveByPix((1.0*dx, 0), "both")

	def zoom(self, direction="in", event=[]):
	
		self.parent.yHist.zoom(direction)
		self.parent.xHist.zoom(direction)
		




	def createDocs(self):


		for i in range(self.numDocs):
			d = Document(self, rank=i+1, focus=(i==self.dd.focusNum and self.dd.docFocus))
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

