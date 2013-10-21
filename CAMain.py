import Tkinter
import sys
import script.CA as CA
import script.Disp as Disp

width = 120

if __name__ == "__main__":
	for arg in sys.argv[1:]:
		root = Tkinter.Tk()
		root.title(arg)
		start = [0]*width + [1] + [0]*width
		rules = CA.LoadRules(arg)
		grid = CA.EvolveSystemMulti(start, rules, len(start)/2)
		Disp.GridDisplay(root, grid, 800, 800)
		root.mainloop()