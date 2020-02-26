import argparse

# 1. Instantiate the parser
parser = argparse.ArgumentParser(description='Optional app description')


# 2. Add arguments
# Required positional argument
parser.add_argument('pos_arg', type=int,
                    help='A required integer positional argument')
# Optional positional argument
parser.add_argument('opt_pos_arg', type=int, nargs='?',
                    help='An optional integer positional argument')
# Optional argument
parser.add_argument('--opt_arg', type=int,
                    help='An optional integer argument')
# Switch
parser.add_argument('--switch', action='store_true',
                    help='A boolean switch')

# 3. Parse
args = parser.parse_args()

# 4. Access
print("Argument values:")
print(args.pos_arg)
print(args.opt_pos_arg)
print(args.opt_arg)
print(args.switch)

# 5.  Check Values
if args.pos_arg > 10:
    parser.error("pos_arg cannot be larger than 10")
    
###################

# Correct use:
# $ ./app 1 2 --opt_arg 3 --switch
# Argument values:
# 1
# 2
# 3
# True


# Incorrect arguments:
# $ ./app foo 2 --opt_arg 3 --switch
# usage: convert [-h] [--opt_arg OPT_ARG] [--switch] pos_arg [opt_pos_arg]
# app: error: argument pos_arg: invalid int value: 'foo'

# $ ./app 11 2 --opt_arg 3
# Argument values:
# 11
# 2
# 3
# False
# usage: app [-h] [--opt_arg OPT_ARG] [--switch] pos_arg [opt_pos_arg]
# convert: error: pos_arg cannot be larger than 10


# Full help:
# $ ./app -h
# usage: app [-h] [--opt_arg OPT_ARG] [--switch] pos_arg [opt_pos_arg]
# Optional app description

# positional arguments:
#   pos_arg            A required integer positional argument
#   opt_pos_arg        An optional integer positional argument

# optional arguments:
#   -h, --help         show this help message and exit
#   --opt_arg OPT_ARG  An optional integer argument
#   --switch           A boolean switch
