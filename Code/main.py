from header import *

from DesignDetails import *
from ScholarVR import *


def graphicsInit():
	global designDetails

	dd = designDetails
	tk_root.title("Google Scholar VR")
	#tk_root.geometry("%dx%d%+d%+d" % (g.WIDTH/2, g.HEIGHT/2, g.WIDTH/4, g.HEIGHT/4))
	tk_root.geometry("%dx%d%+d%+d" % (dd.glyphAreaWidth+dd.histThickness+dd.resultListWidth, 
		dd.glyphAreaHeight+dd.histThickness,
		g.WIDTH/4, g.HEIGHT/4))

	tk_root.config(bg=g.toHex(dd.very_light_grey))

	tk_root.update()

	#tk_root.protocol('WM_DELETE_WINDOW', exit_app)  # root is your root window

if __name__ == "__main__":

	tk_root = Tk()
	#tk_canvas = Canvas(tk_root)
	designDetails = DesignDetails()

	graphicsInit()

	# initialize set of documents
	
	SVR = ScholarVR(tk_root, designDetails)

	# create visualization

	tk_root.mainloop()
