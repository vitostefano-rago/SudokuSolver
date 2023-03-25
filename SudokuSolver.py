import pygame
import SModules.SolverEngine
import SModules.SGUI
import SModules.SImageOutput


def main():
	row = -1
	col = -1
	SModules.SGUI.DrawRawGrid(1)
	loop = 0
	while True:
		tmp = SModules.SGUI.GUIEngine(row,col)
		row, col = tmp[0], tmp[1]
		if row < -5 or col < -5:
			cs = tmp[2].sdk
			if SModules.SolverEngine.ReceiveSudoku(tmp[2]) == 0:
				SModules.SGUI.SendOutPut("Grid division not set properly.")
			elif SModules.SolverEngine.ReceiveSudoku(tmp[2]) == 2:
				SModules.SGUI.SendOutPut("Too many different inputs added.")
			else:
				if row == -6 and col == -6:
					row, col = -1, -1
					if SModules.SolverEngine.CoherencyCheck(tmp[2].sdk) == 0:
						SModules.SGUI.SendOutPut("Input does not comply with rules.")
					else:
						SModules.SGUI.SendOutPut("Input is coherent.")
				
				elif row == -7 and col == -7:
					row, col = -1, -1
					if SModules.SolverEngine.CoherencyCheck(tmp[2].sdk) == 0:
						SModules.SGUI.SendOutPut("Input does not comply with rules.")
					else:
						loop = 0
						mxdff = 1
						lststp = 0
						wt = SModules.SGUI.GetWaitingTime()
						SModules.SImageOutput.GetWT(wt)
						SModules.SImageOutput.AddNextStep(-1)
						SModules.SImageOutput.AddNextStep(tmp[2])
						wit = ["Working on it", "Working on it.", "Working on it..", "Working on it..."]
						while SModules.SolverEngine.CountBlanks() > 0 or SModules.SolverEngine.CoherencyCheck(cs) == 0:
							#Give the possibility to exit
							SModules.SGUI.GUIMinimal()
							if pygame.time.get_ticks() > lststp + wt:
								lststp = pygame.time.get_ticks()
								#Move towards the solution after having waited the proper amount of time
								tmp = SModules.SolverEngine.Solving()
								if tmp[1] < 0:
									#Case Sudoku is invalid
									mxdff = -1
									SModules.SGUI.SendOutPut("This Sudoku has no solution.")
									break
								else:
									#Sudoku is valid
									loop += 1
									mxdff = max(mxdff, tmp[1])
									SModules.SGUI.UpdateValues(tmp[0])
									SModules.SImageOutput.AddNextStep(tmp[0])
									cs = tmp[0].sdk
									if mxdff < 16:
										SModules.SGUI.DspAllVals(1)
									else:
										SModules.SGUI.DspAllVals(2)
									SModules.SGUI.SendOutPut(wit[int(loop % 4)])
									SModules.SGUI.WriteDifficulty(mxdff)
									SModules.SGUI.DisplayLoop(loop)
						
						if mxdff > 0:
							SModules.SGUI.SendOutPut("Finished!")
				
				elif row == -8 and col == -8:
					row, col = -1, -1
					SModules.SImageOutput.UniteFrames(-1)
					if SModules.SolverEngine.CountBlanks() == 0 and SModules.SolverEngine.CoherencyCheck(cs) == 1:
						cit = ["Creating the GIF", "Creating the GIF.", "Creating the GIF..", "Creating the GIF..."]
						for cnt in range(loop + 2):
							#Give the possibility to exit
							SModules.SGUI.GUIMinimal()
							SModules.SImageOutput.UniteFrames(cnt)
							SModules.SGUI.SendOutPut(cit[int(loop % 4)])
						SModules.SGUI.SendOutPut("GIF created!")
					else:
						SModules.SGUI.SendOutPut("Please solve the Sudoku first.")


main()