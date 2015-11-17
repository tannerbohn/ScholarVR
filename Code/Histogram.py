from header import *

class Histogram:

	def __init__(self, parent, orientation):

		self.parent = parent
		self.root = parent.root
		self.dd = self.parent.dd

		self.canvas = Canvas(self.root)

		self.orientation = orientation

		# totalMin, totalMax
		self.updateTotalRange()
		self.getWindowRange(init=True)

			

		return



	def draw(self, init=False, barReset=False):
		canvasW=self.root.winfo_width()
		canvasH=self.root.winfo_height()

		self.getWindowRange()
		self.getBins()


		#print canvasW, canvasH

		if barReset or init:
			# need to clear bin bars
			# remove existing bars from canvas?
			self.binBars = []


		
		if self.orientation == 'y':
			if init:
				self.canvas.place(x=0, y=0, 
					width=self.dd.histThickness, height=self.dd.glyphAreaHeight)

				bg = g.toHex(self.dd.histBkg)
				self.canvas.configure(bg=bg, bd=0, highlightthickness=0, relief='ridge')


				# now draw the bin bars
				numBins = len(self.bins)
				for i in range(numBins):
					# need to flip hist upsidedown for y-axis
					i_p = numBins-i-1

					x0, y0 = 0, (1.*i/numBins)*self.dd.glyphAreaHeight
					x1, y1 = self.dd.histThickness*self.bins[i_p], (1.*(i+1)/numBins)*self.dd.glyphAreaHeight
					fill = g.toHex(self.dd.histFgd)
					index = self.canvas.create_rectangle(x0, y0, x1, y1, tag="bar",
						fill=fill, width=0, activewidth=0)

					self.binBars.append(index)



				# labels for total min and max
				tx, ty = self.dd.histThickness*0.5, 10
				self.totalMaxLabelIndex = self.canvas.create_text(tx, ty,tag="label",
					text='%s'%self.totalMax, font=(g.mainFont, 12, "normal"),
					fill=g.toHex(self.dd.labelColour))

				tx, ty = self.dd.histThickness*0.5, self.dd.glyphAreaHeight-10
				self.totalMinLabelIndex = self.canvas.create_text(tx, ty,tag="label",
					text='%s'%self.totalMin, font=(g.mainFont, 12, "normal"),
					fill=g.toHex(self.dd.labelColour))

				# label for axis units
				tx, ty = self.dd.histThickness*0.5, self.dd.glyphAreaHeight-30
				self.unitsLabelIndex = self.canvas.create_text(tx, ty,tag="label",
					text='citations', font=(g.mainFont, 12, "normal"),
					fill=g.toHex(self.dd.labelColour))
			else:
				# now draw the bin bars
				numBins = len(self.bins)
				for i in range(numBins):
					# need to flip hist upsidedown for y-axis
					i_p = numBins-i-1
					x0, y0 = 0, (1.*i/numBins)*self.dd.glyphAreaHeight
					x1, y1 = self.dd.histThickness*self.bins[i_p], (1.*(i+1)/numBins)*self.dd.glyphAreaHeight
					if barReset:
						fill = g.toHex(self.dd.histFgd)
						index = self.canvas.create_rectangle(x0, y0, x1, y1, tag="bar",
							fill=fill, width=0, activewidth=0)

						self.binBars.append(index)
					else:
						self.canvas.coords(self.binBars[i], x0, y0, x1, y1)


				

		elif self.orientation == 'x':
			if init:
				self.canvas.place(x=self.dd.histThickness, y=self.dd.glyphAreaHeight, 
					width=canvasW-self.dd.histThickness-self.dd.resultListWidth, height=canvasH-self.dd.glyphAreaHeight)

				bg = g.toHex(self.dd.histBkg)
				self.canvas.configure(bg=bg, bd=0, highlightthickness=0, relief='ridge')

				# now draw the bin bars
				numBins = len(self.bins)
				for i in range(numBins):
					x0, y0 = (1.*i/numBins)*self.dd.glyphAreaWidth, self.dd.histThickness*(1.0-self.bins[i])
					x1, y1 = (1.*(i+1)/numBins)*self.dd.glyphAreaWidth, self.dd.histThickness
					fill = g.toHex(self.dd.histFgd)
					index = self.canvas.create_rectangle(x0, y0, x1, y1, tag="bar",
						fill=fill, width=0, activewidth=0)

					self.binBars.append(index)


				# labels for total min and max
				tx, ty = self.dd.glyphAreaWidth-20, self.dd.histThickness*0.5
				self.totalMaxLabelIndex = self.canvas.create_text(tx, ty,
					text='%s'%self.totalMax, font=(g.mainFont, 12, "normal"), tag="label",
					fill=g.toHex(self.dd.labelColour))

				tx, ty = 20, self.dd.histThickness*0.5
				self.totalMinLabelIndex = self.canvas.create_text(tx, ty,
					text='%s'%self.totalMin, font=(g.mainFont, 12, "normal"), tag="label",
					fill=g.toHex(self.dd.labelColour))

				# label for axis units
				tx, ty = 20, 10 #self.dd.histThickness*0.0
				self.unitsLabelIndex = self.canvas.create_text(tx, ty, tag="label",
					text='year', font=(g.mainFont, 12, "normal"),
					fill=g.toHex(self.dd.labelColour))
			else:
				# now draw the bin bars
				numBins = len(self.bins)
				for i in range(numBins):
					x0, y0 = (1.*i/numBins)*self.dd.glyphAreaWidth, self.dd.histThickness*(1.0-self.bins[i])
					x1, y1 = (1.*(i+1)/numBins)*self.dd.glyphAreaWidth, self.dd.histThickness
					if barReset:
						fill = g.toHex(self.dd.histFgd)
						index = self.canvas.create_rectangle(x0, y0, x1, y1, tag="bar",
							fill=fill, width=0, activewidth=0)
						self.binBars.append(index)
					else:
						self.canvas.coords(self.binBars[i], x0, y0, x1, y1)


					

		
		if init:
			self.drawSlidingWindow(init=True)

			self.canvas.tag_raise("label")

		if init:
			self.setBinds()


	def updateTotalRange(self):
		if self.orientation == 'y':
			self.totalMin, self.totalMax = self.parent.glyphArea.getCitationRange(ignoreWindow=True)
			dist = self.totalMax - self.totalMin
			#self.totalMin = int(self.totalMin - dist*0.1)
			self.totalMax = int(self.totalMax + dist*0.1)
		else: #'x'
			self.totalMin, self.totalMax = self.parent.glyphArea.getYearRange(ignoreWindow=True)
			dist = self.totalMax - self.totalMin
			self.totalMin = int(self.totalMin - dist*0.1)
			self.totalMax = int(self.totalMax + dist*0.1)

		#dist = self.totalMax - self.totalMin
		#self.totalMin = int(self.totalMin - dist*0.1)
		#self.totalMax = int(self.totalMax + dist*0.1)

	def getWindowRange(self, init=False):
		if init:
			self.windowMin = 0.25*self.totalMax+0.75*self.totalMin
			self.windowMax = 0.75*self.totalMax+0.25*self.totalMin
			


	def getBins(self):
		# calculate the actual bin values for the histogram

		# num bins ~ sqrt(num results)
		numBins = int(math.sqrt(len(self.parent.glyphArea.docs)))
		bins = [0.0 for i in range(numBins)]

		# loop through docs and put them into bins
		for d in self.parent.glyphArea.docs:

			X = d.year
			if self.orientation == 'y':
				# calculate bin of d.citations
				X = d.citations
				
			
			#n = round((numBins-1) * (X - self.min)/(self.max - self.min))

			# fit X to [0, 1]
			X = (1.*X - self.totalMin)/(1.*self.totalMax - self.totalMin)
			n = round((numBins-1.0)*X)

			#if self.orientation == 'x':
			#	print d.year, n
			bins[int(n)] += 1.0

		# normalize bin values
		bSum = max(bins)#sum(bins)
		bins = [v/bSum for v in bins]

		self.bins = bins

		#print "bins = ", len(self.bins)

	def drawSlidingWindow(self, init=False):
		#self.windowMin, self.windowMax = self.min, (0.75*self.max+0.25*self.min)

		# sliding window:
		#	- a bar to grab and move for each side
		#	- tint the  stuff below it (or try stipple?)

		if self.orientation == 'y':

			if init:
				# fraction of way down glyph height
				frac1 = 1.0 - (self.windowMax-self.totalMin)/(self.totalMax-self.totalMin)
				frac2 = 1.0 - (self.windowMin-self.totalMin)/(self.totalMax-self.totalMin)

				x0, y0 = 0, self.dd.glyphAreaHeight*frac1
				x1, y1 = self.dd.histThickness, self.dd.glyphAreaHeight*frac2
				

				self.windowIndex = self.canvas.create_rectangle(x0, y0, x1, y1, tag="window",
					outline="black", fill="white", width=2, stipple='gray25')

				self.pixLoc=(x0, y0)



				# labels for window min and max
				tx, ty = self.dd.histThickness*0.25, y0+10
				self.windowMaxLabelIndex = self.canvas.create_text(tx, ty,
					text='%s'%int(self.windowMax), font=(g.mainFont, 12, "normal"),
					fill=g.toHex(self.dd.labelColour))

				tx, ty = self.dd.histThickness*0.25, y1-10
				self.windowMinLabelIndex = self.canvas.create_text(tx, ty,
					text='%s'%int(self.windowMin), font=(g.mainFont, 12, "normal"),
					fill=g.toHex(self.dd.labelColour))

			else:
				# fraction of way down glyph height
				frac1 = 1.0 - (self.windowMax-self.totalMin)/(self.totalMax-self.totalMin)
				frac2 = 1.0 - (self.windowMin-self.totalMin)/(self.totalMax-self.totalMin)

				x0, y0 = 0, self.dd.glyphAreaHeight*frac1
				x1, y1 = self.dd.histThickness, self.dd.glyphAreaHeight*frac2
					
				self.canvas.coords(self.windowIndex, x0, y0, x1, y1)


				# labels for window min and max
				tx, ty = self.dd.histThickness*0.25, y0+10
				self.canvas.coords(self.windowMaxLabelIndex, tx, ty)
				self.canvas.itemconfig(self.windowMaxLabelIndex, text='%s'%int(self.windowMax))

				tx, ty = self.dd.histThickness*0.25, y1-10
				self.canvas.coords(self.windowMinLabelIndex, tx, ty)
				self.canvas.itemconfig(self.windowMinLabelIndex, text='%s'%int(self.windowMin))
		else: #'x'

			if init:
				x0, y0 = self.dd.glyphAreaWidth*(self.windowMin - self.totalMin)/(self.totalMax-self.totalMin), self.dd.histThickness
				x1, y1 = self.dd.glyphAreaWidth*(self.windowMax - self.totalMin)/(self.totalMax-self.totalMin), 0
					


				self.windowIndex = self.canvas.create_rectangle(x0, y0, x1, y1, tag="window",
					outline="black", fill="white", width=2, stipple='gray25')

				self.pixLoc=(x0, y0)

				# labels for total min and max
				tx, ty = x1-10, self.dd.histThickness*0.75
				self.windowMaxLabelIndex = self.canvas.create_text(tx, ty,
					text='%s'%int(self.windowMax), font=(g.mainFont, 12, "normal"),
					fill=g.toHex(self.dd.labelColour))

				tx, ty = x0+10, self.dd.histThickness*0.75
				self.windowMinLabelIndex = self.canvas.create_text(tx, ty,
					text='%s'%int(self.windowMin), font=(g.mainFont, 12, "normal"),
					fill=g.toHex(self.dd.labelColour))

				
			else:
				x0, y0 = self.dd.glyphAreaWidth*(self.windowMin - self.totalMin)/(self.totalMax-self.totalMin), self.dd.histThickness
				x1, y1 = self.dd.glyphAreaWidth*(self.windowMax - self.totalMin)/(self.totalMax-self.totalMin), 0
					
				# labels for total min and max
				tx, ty = x1-10, self.dd.histThickness*0.75
				self.canvas.coords(self.windowMaxLabelIndex, tx, ty)
				self.canvas.itemconfig(self.windowMaxLabelIndex, text='%s'%int(self.windowMax))

				tx, ty = x0+10, self.dd.histThickness*0.75
				self.canvas.coords(self.windowMinLabelIndex, tx, ty)
				self.canvas.itemconfig(self.windowMinLabelIndex, text='%s'%int(self.windowMin))


				self.canvas.coords(self.windowIndex, x0, y0, x1, y1)


		if not init:
			self.draw()
			self.parent.glyphArea.draw()


		return



	# define interactions
	def setBinds(self):

		# change cursor on hover
		self.canvas.tag_bind(self.windowIndex, '<Enter>',
				(lambda event, widget="window": self.widgetEnter(event, widget)))
		self.canvas.tag_bind(self.windowIndex, '<Leave>',
				(lambda event, widget="window": self.widgetLeave(event, widget)))

		# drag window to move
		self.canvas.tag_bind(self.windowIndex, '<Button-1>', self.startDrag)
		self.canvas.tag_bind(self.windowIndex, '<ButtonRelease-1>', self.endDrag)
		self.canvas.tag_bind(self.windowIndex, '<B1-Motion>', self.onLeftDrag)

	def widgetEnter(self, event=[], widget=""):
		if widget=="window":
			self.canvas.config(cursor="hand1")

	def widgetLeave(self, event=[], widget=""):

		self.canvas.config(cursor="arrow")

	def startDrag(self, event):

		self.dragInit = (event.x, event.y)
		self.cursorPos = (event.x, event.y)
	

		#print self.cursorPos

	def endDrag(self, event):

		self.draw()
		
		self.root.update()


	def onLeftDrag(self, event):

		
		delta = (event.x - self.cursorPos[0], event.y - self.cursorPos[1])

		self.cursorPos = (event.x, event.y)
		#print "drag:", event.x, event.y
		#self.moveTo((1.0*event.x/self.root.winfo_width(), 1.0*event.y/self.root.winfo_height()))

		if self.orientation == 'y':
			self.moveByPix((0, 1.0*delta[1]))
		else: #'x'
			self.moveByPix((1.0*delta[0], 0))
		

		return

	def moveByPix(self, (x,y)):


		newX, newY = self.pixLoc[0] + x, self.pixLoc[1]+y

		hDims = self.getHistDims()

		if newX < 0:
			newX = 0
		if newX > self.dd.glyphAreaWidth-hDims[0]:
			newX = self.dd.glyphAreaWidth-hDims[0]
		if newY < 0:
			newY = 0
		if newY > self.dd.glyphAreaHeight-hDims[1]:
			newY = self.dd.glyphAreaHeight-hDims[1]

		self.pixLoc = (newX, newY)

		# determine new window max/min
		diff = self.windowMax - self.windowMin
		if self.orientation == 'y':
			newFrac = 1.0 * newY/self.dd.glyphAreaHeight
			self.windowMax = (1.0-newFrac)*self.totalMax + (newFrac)*self.totalMin
			self.windowMin = self.windowMax - diff
		else: #'x'
			newFrac = 1.0 * newX/self.dd.glyphAreaWidth
			self.windowMin = (1.0-newFrac)*self.totalMin + (newFrac)*self.totalMax
			self.windowMax = self.windowMin + diff


		self.drawSlidingWindow()

		self.draw()

	def getHistDims(self):

		if self.orientation == 'y':
			frac1 = 1.0 - (self.windowMax-self.totalMin)/(self.totalMax-self.totalMin)
			frac2 = 1.0 - (self.windowMin-self.totalMin)/(self.totalMax-self.totalMin)

			x0, y0 = 0, self.dd.glyphAreaHeight*frac1
			x1, y1 = self.dd.histThickness, self.dd.glyphAreaHeight*frac2

			return (x1-x0, y1-y0)

		else:
			x0, y0 = self.dd.glyphAreaWidth*(self.windowMin - self.totalMin)/(self.totalMax-self.totalMin), self.dd.histThickness
			x1, y1 = self.dd.glyphAreaWidth*(self.windowMax - self.totalMin)/(self.totalMax-self.totalMin), 0

			return (x1-x0, y1-y0)