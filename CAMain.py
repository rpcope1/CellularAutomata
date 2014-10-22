import sys
import app.CAApplication as Disp

width = 120

#TODO: Replace this with argparse.
def usage(program_name):
    sys.stderr.write('A program for examing Cellular Automata systems\n')
    sys.stderr.write('Usage: {} (rules file)\n'.format(program_name))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        root = Disp.CellularAutomataMain()
        root.title('Cellular Automata')
        root.mainloop()

    elif len(sys.argv) == 2:
        root = Disp.CellularAutomataMain()
        root.title('Cellular Automata')
        root.load(sys.argv[1])
        root.mainloop()
    else:
        usage(sys.argv[0])
        sys.exit(1)