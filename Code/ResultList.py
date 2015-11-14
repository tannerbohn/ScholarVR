from header import *

class ResultList:

	def __init__(self, parent):

		self.root = parent.root
		self.dd = parent.dd

		self.canvas = Canvas(self.root)

		self.draw(init=True)

		return

	def draw(self, init=False):
		rootW=self.root.winfo_width()
		rootH=self.root.winfo_height()

		canvasW=self.dd.resultListWidth
		canvasH=self.dd.resultListHeight

		#print canvasW, canvasH

		if init:
			self.canvas.place(x=rootW-self.dd.resultListWidth, y=0, 
				width=self.dd.resultListWidth, height=self.dd.resultListHeight)
			self.canvas.configure(bg=g.toHex(self.dd.grey3), bd=0, highlightthickness=0)

			self.textIndex = self.canvas.create_text(0,0,anchor=NW, font=(g.mainFont, 10, "normal"),
					fill=g.toHex(self.dd.labelColour), width=self.dd.resultListWidth)

	def setText(self, text):

		self.canvas.itemconfig(self.textIndex, text=text)
