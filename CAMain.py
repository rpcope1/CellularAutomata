import argparse
import app.CAApplication
import logging

root_logger = logging.getLogger("")
ch = logging.StreamHandler()
root_logger.addHandler(ch)
root_logger.setLevel(logging.ERROR)

arg_parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                 description='A program for examining Cellular Automata systems and rules. \
                                              \nThe program displays a 2-dimensional grid. The vertical    \
                                              \naxis represents time between iterations. The horizontal    \
                                              \naxis displays the state of each cell.                      \
                                              \nInformation: http://en.wikipedia.org/wiki/Cellular_automaton')

arg_parser.add_argument('-r', '--rule_file' , type=str, required=False,
                        help='A file that specifies a set of rules for each cell.  \
                              \n=== Rule structure ===                             \
                              \nR specifies rules, colon starts rule input         \
                              \nLeft hand side of semicolon is previous states     \
                              \nRight hand side of semicolon is resultant states   \
                              \n--- Example ---                                    \
                              \nR : 0, 0, 0 ; 0 \
                              \nR : 0, 0, 1 ; 0 ' )

#TODO: Implement logging more better-like
if __name__ == "__main__":
    args = arg_parser.parse_args()
    root = app.CAApplication.CellularAutomataMain()
    root.title('Cellular Automata')    
    if args.rule_file is not None:
        try:
            root.load(args.rule_file)
        except IOError:
            print "WARNING: passed in file ({}) could not be opened".format(args.rule_file)
            pass
    root.mainloop()