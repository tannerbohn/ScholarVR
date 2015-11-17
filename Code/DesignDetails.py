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
		self.histThickness = 70

		self.glyphAreaWidth = 800
		self.glyphAreaHeight = 450

		self.resultListWidth = 200
		self.resultListHeight = self.glyphAreaHeight

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

		
		# dark grey
		self.background = self.grey2

		self.glyphOpacity = 0.1

		self.glyphR1Colour = self.blue

		self.glyphR2Colour = self.yellow

		self.glyphR3Colour = self.red

		self.citeLinkColour = g.shadeN([self.background, self.white], [0,1], 0.5)

		# dark grey
		self.histBkg = self.grey4
		# light blue
		self.histFgd = self.blue

		self.labelColour = (1,1,1)
		'''
		self.background = self.very_light_grey

		self.glyphOpacity = 0.1

		self.glyphR1Colour = self.green

		self.glyphR2Colour = self.red

		self.glyphR3Colour = self.blue

		self.citeLinkColour = self.black


		# dark grey
		self.histBkg = self.grey4
		# light blue
		self.histFgd = self.blue

		self.labelColour = (1,1,1)
		'''