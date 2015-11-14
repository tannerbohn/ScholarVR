from header import *
from Document import *
from GlyphArea import *
from Histogram import *
from ResultList import *


class ScholarVR:
	


	def __init__(self, root, dd):
		self.root = root

		self.dd = dd

		self.glyphArea = GlyphArea(self)
		

		self.yHist = Histogram(self, 'y')
		self.xHist = Histogram(self, 'x')

		self.resultList = ResultList(self)


		

		self.glyphArea.draw(init=True)
		self.yHist.draw(init=True)
		self.xHist.draw(init=True)



		return




			