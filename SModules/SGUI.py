import pygame

#Initialize pygame module
pygame.init()

cols = 9
rows = 9
#size of subcell row, size of subcell culomn
div = [3,3]
sudoku = [[0 for _ in range(cols)] for _ in range(rows)]
nvl = [["" for _ in range(cols)] for _ in range(rows)]
dvl = [["" for _ in range(cols)] for _ in range(rows)]
wait = 1

tl = 3
sl = 1

rs = 900
sr = 200
br = 100

valuelst = [str(cols),str(div[0]),str(div[1]),str(wait)]

#window, to be changed later
window = pygame.display.set_mode((1,1))


def DrawRawGrid(ap = 0):
	global window
	global rows
	global cols
	global div
	global sudoku
	global wait
	global tl
	global sl
	global rs
	global sr
	global br
	
	ws = rs + tl + cols - (rs + tl) % cols
	
	window = pygame.display.set_mode((ws + sr,ws + br))
	window.fill((255,255,255))
	pygame.display.set_caption("Ultimate Sudoku Solver")
	
	#Draw delimiting lines
	pygame.draw.line(window, (0,0,0), [0, ws],[ws + sr, ws],tl)
	pygame.draw.line(window, (0,0,0), [ws,0], [ws, ws], tl)
	
	#draw vertical lines
	for cnt in range(cols):
		if cnt % div[0] == 0:
			pygame.draw.line(window, (0,0,0), [int(ws/cols*cnt),0], [int(ws/cols*cnt), ws], tl)
		else:
			pygame.draw.line(window, (0,0,0), [int(ws/cols*cnt),0], [int(ws/cols*cnt), ws], sl)
	
	#draw horizontal lines
	for cnt in range(rows):
		if cnt % div[1] == 0:
			pygame.draw.line(window, (0,0,0), [0, int(ws/rows*cnt)], [ws, int(ws/rows*cnt)], tl)
		else:
			pygame.draw.line(window, (0,0,0), [0, int(ws/rows*cnt)], [ws, int(ws/rows*cnt)], sl)
	
	#Write permanent texts
	tfont = pygame.font.SysFont("Arial", 30)
	tmessage = tfont.render("Status:", False, (0,0,0))
	tsteps = tfont.render("Steps:", False, (0,0,0))
	tdiff = tfont.render("Difficulty:", False, (0,0,0))
	tsize = tfont.render("Size", False, (0,0,0))
	tdiv = tfont.render("Division", False, (0,0,0))
	tx = tfont.render("X", False, (0,0,0))
	twt = tfont.render("Wait (s)", False, (0,0,0))
	window.blit(tmessage,(20, ws + br/3 - 8))
	window.blit(tdiff,(ws/2 + 120, ws + br/3 - 8))
	window.blit(tsteps,(ws + 35, ws + br/3 - 8))
	window.blit(tsize, (ws + (sr - tsize.get_width()) // 2, 50))
	window.blit(tdiv, (ws + (sr - tdiv.get_width()) // 2,150))
	window.blit(tx, (ws + (sr - tx.get_width()) // 2,200))
	window.blit(twt, (ws + (sr - twt.get_width()) // 2, 250))
	
	#Draw/write user inputs (size, division, waiting time)
	pygame.draw.rect(window, (0,0,0), [ws +sr/4, 90, sr/2, 50],1)
	tmi = tfont.render(valuelst[0], False, (0,0,0))
	window.blit(tmi, (ws +sr/2 - 10, 100))
	pygame.draw.rect(window, (0,0,0), [ws +sr/8, 190, sr/4, 50],1)
	trn = tfont.render(valuelst[1], False, (0,0,0))
	window.blit(trn, (ws +sr/4 - 10, 200))
	pygame.draw.rect(window, (0,0,0), [ws + 5*sr/8, 190, sr/4, 50],1)
	tcn = tfont.render(valuelst[2], False, (0,0,0))
	window.blit(tcn, (ws + 3*sr/4 - 10, 200))
	pygame.draw.rect(window, (0,0,0), [ws + sr/4, 290, sr/2, 50], 1)
	twv = tfont.render(valuelst[3], False, (0,0,0))
	window.blit(twv, (ws +sr/2 - 10, 300))
	
	
	#Draw/write buttons
	pygame.draw.rect(window, (200,200,200), [ws + tl - sl, 350, sr-sl, ws-350],0)
	bfont = pygame.font.SysFont("Arial", 38)
	sfont = pygame.font.SysFont("Arial", 60)
	pygame.draw.line(window, (0,0,0), [ws, 350],[ws + sr, 350],tl)
	pygame.draw.line(window, (0,0,0), [ws, 550],[ws + sr, 550],tl)
	pygame.draw.line(window, (0,0,0), [ws, 750],[ws + sr, 750],tl)
	tchc1 = bfont.render("Check", False, (0,0,0))
	tchc2 = bfont.render("Coherency", False, (0,0,0))
	tst = sfont.render("Start", False, (0,0,0))
	texp = bfont.render("Export", False, (0,0,0))
	window.blit(tchc1, (ws + (sr - tchc1.get_width()) // 2, 400))
	window.blit(tchc2, (ws + (sr - tchc2.get_width()) // 2, 450))
	window.blit(tst, (ws + (sr - tst.get_width()) // 2, 620))
	window.blit(texp, (ws + (sr - texp.get_width()) // 2, 815))
	
	
	if ap == 1:
		#Actually plot the grid only if requested (needed because of complete re-draws)
		pygame.display.update()

class SudokuTransmit():
	def __init__(self, sdk, sz, dv):
		self.sdk = sdk
		self.sz = sz
		self.dv = dv

def HighLightCell(rs,row,col,color):
	global rows
	global cols
	global window
	global tl
	global sl
	#Calculate starting corner
	ws = rs + tl + cols - (rs + tl) % cols
	sc = [int(ws / cols) * col, int(ws / rows) * row]
	#Vertical lines
	if row % div[1] == 0:
		#Case top line needs to be thick
		pygame.draw.line(window, color,sc,[sc[0] + int(ws / cols), sc[1]], tl)
		pygame.draw.line(window, color,[sc[0], sc[1] + int(ws / rows)],[sc[0] + int(ws / cols), sc[1]  + int(ws / rows)], sl)
	if row % div[1] == div[1] - 1:
		#Case bottom line needs to be thick
		pygame.draw.line(window, color,sc,[sc[0] + int(ws / cols), sc[1]], sl)
		pygame.draw.line(window, color,[sc[0], sc[1] + int(ws / rows)],[sc[0] + int(ws / cols), sc[1]  + int(ws / rows)], tl)
	if row % div[1] != 0 and row % div[1] != div[1] - 1:
		#Case no horizontal line needs to be thick
		pygame.draw.line(window, color,sc,[sc[0] + int(ws / cols), sc[1]], sl)
		pygame.draw.line(window, color,[sc[0], sc[1] + int(ws / rows)],[sc[0] + int(ws / cols), sc[1]  + int(ws / rows)], sl)
	#Horizontal lines
	if col % div[0] == 0:
		#Case left line needs to be thick
		pygame.draw.line(window, color,sc,[sc[0], sc[1] + int(ws / rows)], tl)
		pygame.draw.line(window, color,[sc[0]+ int(ws / cols), sc[1]],[sc[0] + int(ws / cols), sc[1]  + int(ws / rows)], sl)
	if col % div[0] == div[0] - 1:
		#Case rigth line needs to be thick
		pygame.draw.line(window, color,sc,[sc[0], sc[1] + int(ws / rows)], sl)
		pygame.draw.line(window, color,[sc[0]+ int(ws / cols), sc[1]],[sc[0] + int(ws / cols), sc[1]  + int(ws / rows)], tl)
	if col % div[0] != 0 and col % div[0] != div[0] - 1:
		#Case no line needs to be thick
		pygame.draw.line(window, color,sc,[sc[0], sc[1] + int(ws / rows)], sl)
		pygame.draw.line(window, color,[sc[0]+ int(ws / cols), sc[1]],[sc[0] + int(ws / cols), sc[1]  + int(ws / rows)], sl)
	pygame.display.update()


def ClickCell(oldr, oldc, xpos, ypos):
	global valuelst
	global tl
	global sl
	global rs
	global sudoku
	global nvl
	
	#Eliminate highlight from old cell, if previous was inside game area
	if oldr >= 0 and oldc >= 0:
		HighLightCell(rs,oldr,oldc,(0,0,0))
	
	#Eliminate highlight if it was outside game area, reset displayed number (for cases it is eliminated and would not be re-displayed)
	else:
		ws = rs + tl + cols - (rs + tl) % cols
		tfont = pygame.font.SysFont("Arial", 30)
		if oldr == -2 and oldc == -2:
			pygame.draw.rect(window, (0,0,0), [ws +sr/4, 90, sr/2, 50],1)
		elif oldr == -3 and oldc == -3:
			pygame.draw.rect(window, (0,0,0), [ws +sr/8, 190, sr/4, 50],1)
		elif oldr == -4 and oldc == -4:
			pygame.draw.rect(window, (0,0,0), [ws +5*sr/8, 190, sr/4, 50],1)
		elif oldr == -5 and oldc == -5:
			pygame.draw.rect(window, (0,0,0), [ws +sr/4, 290, sr/2, 50],1)
	
	ws = rs + tl + cols - (rs + tl) % cols
	#Handle actual click
	if xpos <= ws and ypos <= ws:
		#Calculate row, column that was clicked, area inside game area was clicked
		row = round((ypos - ws/rows/2)/(ws/rows))
		col = round((xpos - ws/cols/2)/(ws/cols))
		HighLightCell(rs,row, col,(255,0,0))
		valuelst = [str(cols),str(div[0]),str(div[1]),str(wait)]
	
	elif xpos > ws + 20 and ypos > 90 and ypos < 140:
		#Size area was clicked
		row, col = -2, -2
		pygame.draw.rect(window, (255,255,255), [ws +sr/4, 90, sr/2, 50],0)
		pygame.draw.rect(window, (255,0,0), [ws +sr/4, 90, sr/2, 50],1)
		valuelst[0] = ""
		pygame.display.update()
	
	elif xpos > ws + 20 and xpos < ws + 80 and ypos > 190 and ypos < 240:
		#Subcell row area was clicked
		row, col = -3, -3
		pygame.draw.rect(window, (255,255,255), [ws +sr/8, 190, sr/4, 50],0)
		pygame.draw.rect(window, (255,0,0), [ws +sr/8, 190, sr/4, 50],1)
		valuelst[1] = ""
		pygame.display.update()
	
	elif xpos > ws + 120 and ypos > 190 and ypos < 240:
		#Subcell column area was clicked
		row, col = -4, -4
		pygame.draw.rect(window, (255,255,255), [ws +5*sr/8, 190, sr/4, 50],0)
		pygame.draw.rect(window, (255,0,0), [ws +5*sr/8, 190, sr/4, 50],1)
		valuelst[2] = ""
		pygame.display.update()
	
	elif xpos > ws + 20 and ypos > 290 and ypos < 340:
		#Size area was clicked
		row, col = -5, -5
		pygame.draw.rect(window, (255,0,0), [ws +sr/4, 290, sr/2, 50],1)
		pygame.display.update()
	
	else:
		#Area outside everything was clicked
		valuelst = [str(cols),str(div[0]),str(div[1]),str(wait)]
		row, col = -1, -1
		valuelst = [str(cols),str(div[0]),str(div[1]),str(wait)]
		if oldr <= -2 and oldc <= -2:
			#Eliminate previous non-game area highlighting
			pygame.display.update()
		if xpos > ws:
			if ypos > 350 and ypos < 550:
				row, col = -6, -6
			elif ypos > 550 and ypos < 750:
				row, col = -7, -7
				for cntr in range(rows):
					for cntc in range(cols):
						if sudoku[cntr][cntc] != 0:
							nvl[cntr][cntc] = sudoku[cntr][cntc]
			elif ypos > 750 and ypos < ws:
				row, col = -8, -8
	return row, col


def ArrowCellMove(rs, oldr, oldc, arr):
	global rows
	global cols
	global tl
	global sl
	if oldr >= 0 and oldc >= 0:
		row, col = oldr, oldc
		HighLightCell(rs,oldr,oldc,(0,0,0))
		if arr == pygame.K_DOWN and row < rows - 1:
			#Key down pressed, not yet at botton row
			row += 1
		elif arr == pygame.K_UP and row > 0:
			#Key up pressed, not yet at toprow:
			row -= 1
		elif arr == pygame.K_LEFT and col > 0:
			#Left key pressed, not yet at leftmost arrow
			col-= 1
		elif arr == pygame.K_RIGHT and col < cols - 1:
			#Right arrow pressed, not yet at rigthmost arrow
			col += 1
		elif arr == pygame.K_TAB:
			#In case of tabulator, start at the beginning of the next row
			col = 0
			row += 1
			if row == rows:
				row = 0
		elif arr ==  pygame.K_BACKSPACE:
			#In case of backspace, go to the last cell of the previous row
			col = cols - 1
			row -= 1
			if row < 0:
				row = rows - 1
		HighLightCell(rs,row, col,(255,0,0))
	else:
		row, col = oldr, oldc
	return row, col


def CellOutPut(row, col, color):
	global sudoku
	global rows
	global cols
	global window
	global rs
	global nvl
	global div
	global wait
	global valuelst
	global tl
	global dvl
	
	ws = rs + tl + cols - (rs + tl) % cols
	
	#Inside game area
	if row >= 0 and col >= 0:
		nsiz = int(rs*0.7/cols)
		rpos = int((ws/rows - nsiz)/2) + 2
		cpos = int((ws/cols - nsiz)/2 + nsiz/20)
		nfont = pygame.font.SysFont("Arial", nsiz)
		if sudoku[row][col] == 0:
			pygame.draw.rect(window,(255,255,255),[ws*col/cols,ws*row/rows,ws/cols,ws/rows],0)
		else:
			dvl[row][col] = nfont.render(str(sudoku[row][col]), False, color)
			window.blit(dvl[row][col],(ws*col/cols + cpos, ws*row/rows + rpos))
	elif row < -1 and col < -1:
		tfont = pygame.font.SysFont("Arial", 30)
		if row == -2 and col == -2:
			pygame.draw.rect(window, (255,255,255), [ws +sr/4, 90, sr/2, 50],0)
			tmi = tfont.render(valuelst[0], False, (0,0,0))
			window.blit(tmi, (ws +sr/2 - 10, 100))
			pygame.draw.rect(window, (255,0,0), [ws +sr/4, 90, sr/2, 50],1)
			if valuelst[0] != "" and valuelst[0] != "0":
				rows, cols = int(valuelst[0]), int(valuelst[0])
				DrawRawGrid(1)
				sudoku = [[0 for _ in range(cols)] for _ in range(rows)]
				nvl = [["" for _ in range(cols)] for _ in range(rows)]
				dvl = [["" for _ in range(cols)] for _ in range(rows)]
		elif (row == -3 and row == -3):
			pygame.draw.rect(window, (255,255,255), [ws +sr/8, 190, sr/4, 50],0)
			trn = tfont.render(valuelst[1], False, (0,0,0))
			window.blit(trn, (ws +sr/4 - 10, 200))
			pygame.draw.rect(window, (255,0,0), [ws +sr/8, 190, sr/4, 50],1)
			if valuelst[1] != "" and valuelst[2] != "" and valuelst[1] != "0" and valuelst[2] != "0":
				div[0], div[1] = int(valuelst[1]), int(valuelst[2])
				DrawRawGrid()
				DspAllVals(0)
		elif (row == -4 and row == -4):
			pygame.draw.rect(window, (255,255,255), [ws + 5*sr/8, 190, sr/4, 50],0)
			tcn = tfont.render(valuelst[2], False, (0,0,0))
			window.blit(tcn, (ws + 3*sr/4 - 10, 200))
			pygame.draw.rect(window, (255,0,0), [ws + 5*sr/8, 190, sr/4, 50],1)
			if valuelst[1] != "" and valuelst[2] != "" and valuelst[1] != "0" and valuelst[2] != "0":
				div[0], div[1] = int(valuelst[1]), int(valuelst[2])
				DrawRawGrid()
				DspAllVals(0)
		elif row == -5 and col == -5:
			pygame.draw.rect(window, (255,255,255), [ws + sr/4, 290, sr/2, 50], 0)
			twv = tfont.render(valuelst[3], False, (0,0,0))
			window.blit(twv, (ws +sr/2 - 10, 300))
			if valuelst[3] != "":
				wait = int(valuelst[3])
			else:
				wait = 0
			pygame.draw.rect(window, (255,0,0), [ws + sr/4, 290, sr/2, 50], 1)


def DspAllVals(pp):
	global sudoku
	global rows
	global cols
	global nvl
	global window
	
	#Before the solver started working
	if pp == 0:
		for cntr in range(rows):
			for cntc in range (cols):
				if sudoku[cntr][cntc] !=0:
					CellOutPut(cntr, cntc, (0,0,0))
	
	#After the solver started working
	if pp == 1:
		for cntr in range(rows):
			for cntc in range (cols):
				if sudoku[cntr][cntc] !=0 and nvl[cntr][cntc] == "":
					#This means that a value has been added by the solver
					CellOutPut(cntr, cntc, (255,0,0))
	
	#Bruteforce was used, previously filled cell may become blank or a new number may need to be entered
	if pp == 2:
		DrawRawGrid()
		for cntr in range(rows):
			for cntc in range (cols):
				if sudoku[cntr][cntc] !=0 and nvl[cntr][cntc] == "":
					#This means that a value has been added by the solver
					CellOutPut(cntr, cntc, (255,0,0))
				elif nvl[cntr][cntc] != "":
					#This means value was present originally
					CellOutPut(cntr, cntc, (0,0,0))
	
	pygame.display.update()


def ManageKeyInput(row, col, kh, nc):
	global sudoku
	global valuelst
	global nvl
	
	#Inside game area
	if row >= 0 and col >= 0:
		#Handle case delete key was pressed
		if kh == -1:
			sudoku[row][col] = 0
			nvl[row][col] = ""
		#Valid key was pressed
		else:
			if sudoku[row][col] == 0 and kh != "0":
				if kh != 0:
					sudoku[row][col] = kh
			elif sudoku[row][col] != 0:
				if len(sudoku[row][col]) < 2:
					sudoku[row][col] += kh
	
	#Outside game area
	elif row < -1 and col < -1 and row >= -5 and col >= -5:
		#Delete was pressed
		if kh == -1:
			valuelst[-row-2] = ""
		elif kh in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"} and valuelst[-row-2] != "0":
			valuelst[-row-2] += kh
	
	CellOutPut(row,col,(0,0,0))
	pygame.display.update()


def GUIEngine(row,col):
	global sudoku
	global rows
	global div
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		
		if event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			tmp = ClickCell(row,col,pos[0],pos[1])
			row, col = tmp[0], tmp[1]
		
		if event.type == pygame.KEYDOWN:
			#Exit with excape
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				exit()
			
			#Handle movement between cells
			elif event.key in {pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_TAB, pygame.K_BACKSPACE}:
				tmp =  ArrowCellMove(900,row,col,event.key)
				row, col = tmp[0], tmp[1]
			
			#Eliminate content of cell
			elif event.key == pygame.K_DELETE:
				ManageKeyInput(row, col, -1, 1)
			
			#Add to content of cell
			elif event.unicode in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "q", "Q", "w", "W", "e", "E", "r", "R", "t", "T", "y", "Y", "u", "U", "i", "I", "o", "O", "p", "P", "a", "A", "s", "S", "d", "D", "f", "F", "g", "G", "h", "H", "j", "J", "k", "K", "l", "L", "z", "Z", "x", "X", "c", "C", "v", "V", "b", "B", "n", "N", "m", "M"}:
				ManageKeyInput(row, col, event.unicode.upper(),1)
	
	trd = SudokuTransmit(sudoku, rows, div)
	return row, col, trd

def GUIMinimal():
	for event in pygame.event.get():
		if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			pygame.quit()
			exit()

def SendOutPut(st):
	global window
	global rs
	global tl
	global cols
	
	ws = rs + tl + cols - (rs + tl) % cols
	
	pygame.draw.rect(window, (255,255,255), [125, ws + tl, 430, 100], 0)
	tfont = pygame.font.SysFont("Arial", 30)
	tom = tfont.render(st, False, (0,0,0))
	window.blit(tom,(125, ws + br/3 - 8))
	pygame.display.update()

def WriteDifficulty(dl):
	global window
	global rs
	global tl
	global cols
	
	ml = {1: "Easy", 2: "Medium", 4: "Hard", 8: "Extreme", 16: "Evil"}
	ws = rs + tl + cols - (rs + tl) % cols
	pygame.draw.rect(window, (255,255,255), [ws/2 + 250, ws + tl, 150, 100], 0)
	tfont = pygame.font.SysFont("Arial", 30)
	td = tfont.render(ml[dl], False, (0,0,0))
	window.blit(td,(ws/2 + 250, ws + br/3 - 8))
	pygame.display.update()

def DisplayLoop(l):
	global window
	global rs
	global tl
	global sr
	
	ws = rs + tl + cols - (rs + tl) % cols
	pygame.draw.rect(window, (255,255,255), [ws + 140, ws + tl, 100, 100], 0)
	tfont = pygame.font.SysFont("Arial", 30)
	dl = tfont.render(str(l), False, (0,0,0))
	window.blit(dl,(ws + 140, ws + br/3 - 8))
	pygame.display.update()

def UpdateValues(ns):
	global sudoku
	
	sudoku = ns.sdk

def GetWaitingTime():
	global wait
	
	return wait * 1000