from termcolor import cprint, colored


# Special print functions
print_good = lambda x: cprint(x, "green")
print_info = lambda x: cprint(x, "blue")
print_bad = lambda x: cprint(x, "red")
important_info = lambda x: colored(x, "blue", attrs=["bold"])
