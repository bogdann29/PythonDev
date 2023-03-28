import cmd
import shlex as sh
import threading
import sys
import readline
import socket

lock = threading.Lock()


class Cowchat(cmd.Cmd):
    @staticmethod
    def snd_rcv(msg, need=True):
        s.send((msg.strip() + "\n").encode())
        if need:
            ans = s.recv(1024).decode().strip().replace("'", "")
            return ans

    def do_login(self, args):
        resp = Cowchat.snd_rcv("login " + args.strip())
        print(resp)

    def complete_login(self, text, line, *args):
        with lock:
            cows = sh.split(
                Cowchat.snd_rcv("cows")[13:].replace(",", "")
            )
            return [s for s in cows if s.startswith(text)]

    def do_who(self, args):
        resp = Cowchat.snd_rcv("who")
        print(resp)

    def do_cows(self, args):
        resp = Cowchat.snd_rcv("cows")
        print(resp)

    def do_yield(self, args):
        Cowchat.snd_rcv("yield " + args.strip(), need=False)
    
    def do_say(self, args):
        Cowchat.snd_rcv("say " + args.strip(), need=False)
    
    def complete_say(self, text, line, *args):
        with lock:
            if len(text.split()) <= 1:
                who = sh.split(
                    Cowchat.snd_rcv("who")[12:].replace(",", "")
                )
                return [s for s in who if s.startswith(text)]

    def do_exit(self, args):
        return 1


def get_messages():
    while True:
        if not lock.locked():
            ans = s.recv(1024).decode().strip().replace("'", "")
            if ans:
                print(ans + "\n")
                print(
                    f"\n{cmdline.prompt}{readline.get_line_buffer()}",
                    end="",
                    flush=True,
                )


def main():
    global cmdline
    cmdline = Cowchat()
    gm = threading.Thread(target=get_messages, args=())
    gm.start()
    cmdline.cmdloop()


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 1337))
        main()