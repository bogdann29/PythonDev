import cmd
import shlex as sh
import cowsay


class cmdLine(cmd.Cmd):

    prompt = '>>>'
    vars = {
        2: cowsay.list_cows(),
        3: ['00', '@@', '^^', '=='],
        4: ['U', 'L', 'V', 'u']
    }


    def complete(self, text, line, startidx, endidx):
        n = len(sh.split(line[:startidx]))
        if n in vars:
            lst = vars[n]
        else:
            lst = []
        return [var for var in lst if var.startswith(text)]


    def cowthink_params(self, args):
        params_names = ['cow', 'eyes', 'tongue']
        optional_args = {}
        for i in range(len(args)):
            optional_args[params_names[i]] = args[i]
        return optional_args
    
    
    def do_list_cows(self, args):
        'Prints list of available cows'
        print(cowsay.list_cows())


    def do_cowsay(self, args):
        'Prints cow saying message'
        try:
            message, *m_args = sh.split(args)
            params = self.cowthink_params(m_args)
            print(cowsay.cowsay(message, **params))
        except ValueError:
            print('cow need a message')


    def do_cowthink(self, args):
        'Prints cow thinking message'
        try:
            message, *m_args = sh.split(args)
            params = self.cowthink_params(m_args)
            print(cowsay.cowthink(message, **params))
        except ValueError:
            print('cow need a message')


    def do_make_bubble(self, args):
        'Prints bubble with message'
        print(cowsay.make_bubble(args))
    

    def complete_cowsay(self, text, line, startidx, endidx):
        return self.complete(self, text, line, startidx, endidx)


    def complete_cowthink(self, text, line, startidx, endidx):
        return self.complete(text, line, startidx, endidx)


    def do_EOF(self, args):
        'End command line'
        return 1
    

    def do_exit(self, args):
        'End command line'
        return 1


if __name__ == '__main__':
    cmdLine().cmdloop()