from header import *

class DesignDetails:
	'''
		canvas: 450x800 (height x width in pixels)

		y-histogram: 450x70
			- left of canvas
		x-histogram: 70x800
			- below canvas

		sideList: 450x200
			- right of canvas
		topicArea: 200x800
			- below x-histogram
		pageCircle: 200x200
			- to right of topicArea
	'''
	def __init__(self):
		self.totalWidth = 800#1200
		self.totalHeight = 450#800


		self.histThickness = 70

		self.resultListWidth = 0#300
		self.resultListHeight = self.totalHeight - self.histThickness

		self.glyphAreaWidth = self.totalWidth-self.histThickness-self.resultListWidth
		self.glyphAreaHeight = self.totalHeight - self.histThickness

		
		# pick a document to set as "center" to emulate citation view
		self.docFocus=False
		self.focusNum = 10

		# gray out random results
		self.randomGrayFrac = 0.3

		self.maxGlyphR = 50.0
		self.minGlyphR = 10.0

		self.numDocs = 100

		''' DEFINE GOOGLE COLOURS '''

		self.grey1 = g.toFloatfHex('#000000')
		self.grey2 = g.toFloatfHex('#212121')
		self.grey3 = g.toFloatfHex('#303030')
		self.grey4 = g.toFloatfHex('#424242')

		self.very_light_grey = g.toFloatfHex('#e6e6e6')

		
		# www.google.com/design/spec/style/color.html#

		self.blue = g.toFloatfHex('#2196F3')
		self.red = g.toFloatfHex('#F44336')
		self.orange = g.toFloatfHex('#FF9800')
		self.yellow = g.toFloatfHex('#FFEB3B')
		self.green= g.toFloatfHex('#4CAF50')
		self.purple=g.toFloatfHex('#673AB7')
		self.white=(1,1,1)
		self.black=(0,0,0)

		self.lightblue = g.toFloatfHex('#03A9F4')

		''' ##################### '''

		'''
		# dark grey
		self.background = self.grey2

		self.glyphOpacity = 0.1

		self.glyphR1Colour = self.blue

		self.glyphR2Colour = self.yellow

		self.glyphR3Colour = self.red

		self.citeLinkColour = g.shadeN([self.background, self.white], [0,1], 0.1)

		# dark grey
		self.histBkg = self.grey4
		# light blue
		self.histFgd = self.blue

		self.histWindow = self.white

		self.histBar = self.orange
		self.histBarActive = self.red

		self.labelColour = (1,1,1)
		'''

		self.cbBlue1 = g.toFloatfHex('#2b8cbe')
		self.cbBlue2 = g.toFloatfHex('#a6bddb')
		self.cbBlue3 = g.toFloatfHex('#ece7f2')

		self.cbTeal1 = g.toFloatfHex('#1c9099')
		self.cbTeal2 = g.toFloatfHex('#a6bddb')
		

		self.background = self.very_light_grey

		self.glyphRankColour = (1,1,1)

		self.glyphOpacity = 0.1

		self.glyphR1Colour = self.black

		self.glyphR2Colour = g.toFloatfHex('#de2d26')

		self.glyphR3Colour = self.cbTeal1

		self.citeLinkColour = g.shadeN([self.background, self.black], [0,1], 0.1)


		# dark grey
		self.histBkg = (0.85, 0.85, 0.85)
		# light blue
		self.histFgd = self.blue

		self.histWindow = self.white

		self.histBar = self.orange
		self.histBarActive = self.red

		self.labelColour = (0,0,0)
		
		
		