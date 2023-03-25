from PIL import Image, ImageDraw, ImageFont

solsteps = []
wt = 1000
dd = [3,3]
tl = 3
sl = 1
rs = 900
siz = 9
imig = []
bckgnd = 0

class SudokuTransmit():
	def __init__(self, sdk, sz, dv):
		self.sdk = sdk
		self.sz = sz
		self.dv = dv


def GetWT(w):
	global wt
	
	wt = w


def AddNextStep(stp):
	global solsteps
	global dd
	global siz
	
	if stp == -1:
		solsteps = []
	
	else:
		if solsteps == []:
			dd = stp.dv
			siz = stp.sz
		tmp = [[stp.sdk[cntr][cntc] for cntc in range(siz)] for cntr in range(siz)]
		solsteps.append(tmp)


def GenerateFrame(osdk, csdk):
	global tl
	global sl
	global rs
	global wt
	global dd
	global siz
	global bckgnd
	global imig
	
	ws = int(rs + tl + siz - (rs + tl) % siz)
	img = bckgnd.copy()
	imgdrw = ImageDraw.Draw(img)
	nsiz = int(rs*0.7/siz)
	rpos = int((ws/siz - nsiz)/2) + 2
	cpos = int((ws/siz - nsiz)/2 + nsiz/20)
	fnt = ImageFont.truetype("arial.ttf", nsiz)
	
	#In case the first image is being generated, add the original simbols to it
	if len(imig) == 0:
		for cntr in range(siz):
			for cntc in range(siz):
				if csdk[cntr][cntc] != 0:
					imgdrw.text((ws*cntc/siz + cpos, ws*cntr/siz + rpos), str(csdk[cntr][cntc]), font = fnt, fill = (0,0,0))
		bckgnd = img.copy()
	
	#Add only the simbols added as part of the solution
	else:
		for cntr in range(siz):
			for cntc in range(siz):
				if csdk[cntr][cntc] != 0 and osdk[cntr][cntc] == 0:
					imgdrw.text((ws*cntc/siz + cpos, ws*cntr/siz + rpos), str(csdk[cntr][cntc]), font = fnt, fill = (255,0,0))
	
	return img

def CreateCanvas():
	global tl
	global sl
	global rs
	global wt
	global dd
	global siz
	global bckgnd
	
	ws = int(rs + tl + siz - (rs + tl) % siz)
	
	img = Image.new("RGB", (ws, ws), (255, 255, 255))
	imgdrw = ImageDraw.Draw(img)
	
	#Draw vertical lines
	for cnt in range(siz):
		if cnt % dd[0] == 0:
			imgdrw.line([(int(cnt * ws/siz), 0),(int(cnt * ws/siz), ws)], fill = (0,0,0), width = tl)
		else:
			imgdrw.line([(int(cnt * ws/siz), 0),(int(cnt * ws/siz), ws)], fill = (0,0,0), width = sl)
	imgdrw.line([((ws-sl, 0)),(ws-sl, ws)], fill = (0,0,0), width = tl)
	
	#Draw horizontal lines
	for cnt in range(siz):
		if cnt % dd[1] == 0:
			imgdrw.line([(0,int(cnt * ws/siz)),(ws, int(cnt * ws/siz))], fill = (0,0,0), width = tl)
		else:
			imgdrw.line([(0,int(cnt * ws/siz)),(ws, int(cnt * ws/siz))], fill = (0,0,0), width = sl)
	imgdrw.line([((0,ws-sl)),(ws-tl, ws-sl)], fill = (0,0,0), width = tl)
	
	bckgnd = img.copy()

def UniteFrames(cst):
	global solsteps
	global wt
	global imig
	
	if cst < len(solsteps) and cst >= 0:
		imig.append(GenerateFrame(solsteps[0], solsteps[cst]))
		
		if cst == 0:
			ti = imig[0]
			imig.append(ti)
		
		if cst == len(solsteps) - 1:
			ti = imig[len(imig) - 1]
			imig.append(ti)
	
	elif cst >= len(solsteps):
		imig[0].save("Sudoku.gif", save_all=True, append_images = imig[1:], optimize = False, duration = 250 + wt * 0.5, loop = 0)
	
	elif cst == -1:
		imig = []
		CreateCanvas()