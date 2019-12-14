import sys
import inspect

class CommandLineInterface:
    funcs = {}

    def command(self, f):
        self.funcs[f.__name__] = f

    def main(self):
        if len(sys.argv) == 1:
            print('USAGE: python example.py <command> [<key>=<value>]*')
            sys.exit(1)

        name = sys.argv[1]
        if name not in self.funcs:  # invalid function name
            print(f'Invalid function. Available functions: {", ".join(self.funcs)}')
            print('USAGE: python example.py <command> [<key>=<value>]*')
            sys.exit(1)

        splitted = [sys.argv[i].split('=') for i in range(2, len(sys.argv))]

        if not all(len(argument) == 2 and '' not in argument for argument in splitted):  # invalid parameter format
            print('Invalid arguments format. Format: [<key>=<value>]')
            print('USAGE: python example.py <command> [<key>=<value>]*')
            sys.exit(1)
            
        kwargs = {arg[0]: arg[1] for arg in splitted}

        if any(arg not in (args := inspect.getfullargspec(self.funcs[name]).args) for arg in kwargs):
            print(f'Invalid argument supplied. Function arguments: {", ".join(args)}')
            print('USAGE: python example.py <command> [<key>=<value>]*')
            sys.exit(1)

        self.funcs[name](**kwargs)
