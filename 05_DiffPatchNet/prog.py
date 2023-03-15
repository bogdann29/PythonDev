import asyncio
import cowsay as cs
import shlex as sx

conn_users = {}
clients = {}

list_cows = cs.list_cows()


async def auth_check(me):
    if me not in clients:
        await conn_users[me].put(
            "You need to login (command login <name>)"
        )
        return False
    return True


async def cow_chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info("peername"))
    print(me)
    conn_users[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(conn_users[me].get())

    while not reader.at_eof():
        done, pending = await asyncio.wait(
            [send, receive], return_when=asyncio.FIRST_COMPLETED
        )
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())

                text = q.result().decode().strip()
                command = sx.split(text)
                match command:
                    case ["login", login]:
                        if me not in clients:
                            if login in list_cows:
                                clients[me] = login, me
                                await conn_users[me].put(
                                    f"You are logged in as {login}"
                                )
                            else:
                                await conn_users[me].put(
                                    f"Incorrect username {login}"
                                )
                        else:
                            await conn_users[me].put(
                                f"You are already logged in as {clients[me][0]}"
                            )

                    case ["who"]:
                        if me not in clients:
                            await conn_users[me].put("You need to login (command login <name>)")
                        else:
                            await conn_users[me].put(
                                "Auth users: " + ", ".join([clients[usr][0] for usr in clients])
                            )
                    case ["cows"]:
                        if me not in clients:
                            await conn_users[me].put("You need to login (command login <name>)")
                        else:
                            await conn_users[me].put(
                                "Free logins: " + ", ".join(set(cs.list_cows()) - set([clients[usr][0] for usr in clients]))
                            )

                    case ["say", login, text]:
                        if me not in clients:
                            await conn_users[me].put("You need to login (command login <name>)")
                        else:
                            if login not in [clients[usr][0] for usr in clients]:
                                await conn_users[me].put(
                                    f"User {login} doesn't exist"
                                )
                            else:
                                message = cs.cowsay(
                                    message=text, cow=clients[me][0]
                                )
                                for out in clients.values():
                                    if out[0] == login:
                                        await conn_users[out[1]].put(message)
                                        break

                    case ["yield", text]:
                        if me not in clients:
                            await conn_users[me].put("You need to login (command login <name>)")
                        else:
                            message = cs.cowsay(message=text, cow=clients[me][0])
                            for out in clients.values():
                                if conn_users[out[1]] is not conn_users[me]:
                                    await conn_users[out[1]].put(
                                        f"{clients[me][0]}:\n{message}"
                                    )

                    case ["quit"]:
                        send.cancel()
                        receive.cancel()
                        print(me, "DONE")
                        del clients[me]
                        del conn_users[me]
                        writer.close()
                        await writer.wait_closed()
                        return

            elif q is receive:
                receive = asyncio.create_task(conn_users[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()

    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del conn_users[me]
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(cow_chat, "0.0.0.0", 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())