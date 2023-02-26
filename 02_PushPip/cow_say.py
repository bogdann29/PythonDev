import cowsay
import argparse


def f(param, name):
    if not param:
        name = ''
    return name


p = argparse.ArgumentParser()

p.add_argument('message', type=str)

p.add_argument('-e', default='oo')
p.add_argument('-f', default=None)
p.add_argument('-l', default='default')
p.add_argument('-n', default=True)
p.add_argument('-T', default='  ')
p.add_argument('-W', default=40, type=int)

p.add_argument('-b', default='')
p.add_argument('-d', default='')
p.add_argument('-g', default='')
p.add_argument('-p', default='')
p.add_argument('-s', default='')
p.add_argument('-t', default='')
p.add_argument('-w', default='')
p.add_argument('-y', default='')

args = p.parse_args()

if args.l == 'default':
    params = f(args.b, 'b') + f(args.d, 'd') + f(args.g, 'g') + f(args.p, 'p') + f(args.s, 's') + f(args.t, 't') + \
             f(args.w, 'w') + f(args.y, 'y')
    cow = cowsay.cowsay(message=args.message,
                        cowfile=args.f,
                        preset=params,
                        eyes=args.e,
                        tongue=args.T,
                        width=args.W,
                        )
    print(cow)
else:
    print(cowsay.list_cows())
