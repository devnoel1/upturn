import asyncio
import os
import sys
from typing import Union, List
import pyrogram
from pyrogram import Client, errors, raw, filters
from pyrogram.types import InputPhoneContact
from pyrogram.handlers import MessageHandler
from pyrogram.errors import RPCError, FloodWait, UserAlreadyParticipant, PeerIdInvalid
import time
from redis import Redis

pyrogram.session.Session.notice_displayed = True


# PROF start
PROF_CLIENTS_DIR = './clients'

async def prof_send(app, chat_ids):
    with open('prof-firstname.txt', 'r') as namesFile:
        names = namesFile.readlines()
    with open('prof-lastname.txt', 'r') as namesFile1:
        names1 = namesFile1.readlines()
    with open('prof-bio.txt', 'r') as namesFile2:
        names2 = namesFile2.readlines()
    with open('prof-profile.txt', 'r') as namesFile3:
        names3 = namesFile3.readlines()
    with open('prof-username.txt', 'r') as namesFile4:
        names4 = namesFile4.readlines()
    

    for i in range(0,1):
        try:
            await app.update_profile(first_name=names[prof_clients.index(app)], last_name=names1[prof_clients.index(app)], bio=names2[prof_clients.index(app)])
            await app.set_profile_photo(photo="prof-photos/"+names3[prof_clients.index(app)].replace("\n",""))
            await app.update_username(names4[prof_clients.index(app)].replace("\n",""))
        except Exception as e:
            print(str(e))

        await asyncio.sleep(1)


async def prof_main(t=0):

    print('\n- Start Clients:')

    global prof_clients
    prof_clients = []
    tasks = []
    for f in os.listdir(PROF_CLIENTS_DIR):
        if not f.endswith(".session"):
            continue

        session_name = f.replace('.session', '')
        print(f'\n- Client({session_name})')
        client = Client(session_name, workdir=PROF_CLIENTS_DIR)
        try:
            await client.start()
            print(f' - Client({session_name}): Started')
        except RPCError as e:
            print(f' - Client({session_name}) Not Started: {e}')
            continue
        prof_clients.append(client)
        tasks.append(asyncio.ensure_future(prof_send(client,"1")))

    await asyncio.gather(*tasks)
    await asyncio.gather(*[client.stop() for client in prof_clients])


async def prof_corn_main(sleep_time):
    while True:
        await prof_main()
        print(f'Sleep for {sleep_time} seconds')
        await asyncio.sleep(sleep_time)


async def prof_add_client():
    session_name = input('Input session name: ')
    async with Client(session_name, workdir=PROF_CLIENTS_DIR) as new_client:
        print(f'- New Client {new_client.storage.database}')


async def prof_usage():
    print('BAD ARGS')

def TelegramBulkAccountProfileChanger(args):
    if not os.path.exists(PROF_CLIENTS_DIR):
        os.mkdir(PROF_CLIENTS_DIR)

    if len(args) == 1:
        func = prof_main()
    elif len(args) == 2:
        if args[1].isdigit():
            func = prof_corn_main(int(args[1]))
        elif args[1] == '--add':
            func = prof_add_client()
        else:
            func = prof_usage()
    else:
        func = prof_usage()

    print('\nHere we go...\n')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(func)
    loop.close()

    print('\nFinish!\n')
# PROF end

# forward start
async def main(source_chat, target_chat, first_message):
    async with Client('erfan4lx',4924338,'121759c8281541cdb3a75e47656bb0e0') as app:
        app: Client
        print("start")
        for chat in [source_chat, target_chat]:
            try:
                await app.join_chat(chat)
            except:
                pass
        async for message in app.iter_history(source_chat, reverse=True):
            if message.message_id < first_message:
                continue
            print('msg: ', message.message_id)
            try:
                await message.copy(target_chat)
            except errors.FloodWait as e:
                print("sleep", e.x)
                await asyncio.sleep(e.x + 0.4)
            except errors.RPCError as e:
                print('ex:', e)
            except (errors.ChatInvalid, errors.ChatIdInvalid):
                print('bad target!')
                break
            time.sleep(1)
def Telegramchannelpostsforwader(args):
    source_chat = args[1] if len(args)==2 else str(input("Enter the target channel: "))
    target_chat = args[2] if len(args)==3 else str(input("Enter the destination channel: "))
    first_message = args[3] if len(args)==4 else 0
    asyncio.run(main(source_chat, target_chat, first_message))
# forward end

# join start
JOIN_CLIENTS_DIR = './clients'
JOIN_CHATS_FILENAME = 'join-chats.txt'

join_counter = 0

async def join_send(app, chat_ids):
    global join_counter
    for chat_id in chat_ids:
        try:
            join_counter += 1
            await app.join_chat(str(chat_id))
        except Exception as e:
            print(str(e))
        #if join_counter == 5:
        #    time.sleep(1500)
        #    join_counter = 0

        await asyncio.sleep(1)


async def join_main(t=0):
    if os.path.exists(JOIN_CHATS_FILENAME):
        with open(JOIN_CHATS_FILENAME) as file:
            chats = [line.replace("\r", "").replace("\n", "") for line in file.readlines()]
    else:
        return print(f'- File({JOIN_CHATS_FILENAME}) NOT EXISTS')
    if not chats:
        return print(f'- NO CHAT-ID IN FILE({JOIN_CHATS_FILENAME})')

    print('\n- Start Clients:')

    clients = []
    tasks = []
    for f in os.listdir(JOIN_CLIENTS_DIR):
        if not f.endswith(".session"):
            continue

        session_name = f.replace('.session', '')
        print(f'\n- Client({session_name})')
        client = Client(session_name, workdir=JOIN_CLIENTS_DIR)
        try:
            await client.start()
            print(f' - Client({session_name}): Started')
        except RPCError as e:
            print(f' - Client({session_name}) Not Started: {e}')
            continue
        clients.append(client)
        tasks.append(asyncio.ensure_future(join_send(client, chats)))

    await asyncio.gather(*tasks)
    await asyncio.gather(*[client.stop() for client in clients])


async def join_corn_main(sleep_time):
    while True:
        await join_main()
        print(f'Sleep for {sleep_time} seconds')
        await asyncio.sleep(sleep_time)


async def join_add_client():
    session_name = input('Input session name: ')
    async with Client(session_name, workdir=JOIN_CLIENTS_DIR) as new_client:
        print(f'- New Client {new_client.storage.database}')


async def join_usage():
    print('BAD ARGS')


def TelegramMemberAutoJoiner(args):

    if not os.path.exists(JOIN_CLIENTS_DIR):
        os.mkdir(JOIN_CLIENTS_DIR)

    if len(args) == 1:
        func = join_main()
    elif len(args) == 2:
        if args[1].isdigit():
            func = join_corn_main(int(args[1]))
        elif args[1] == '--add':
            func = join_add_client()
        else:
            func = join_usage()
    else:
        func = join_usage()

    print('\nHere we go...\n')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(func)
    loop.close()

    print('\nFinish!\n')
# join end
# checker start
CHECKER_CLIENTS_DIR = './clients'
CHECKER_DEFAULT_FILENAME = 'checker-nums.txt'


async def checker_main(once=True):
    numbers_filename = input(f'- Enter Numbers File Name ({CHECKER_DEFAULT_FILENAME}): ') or CHECKER_DEFAULT_FILENAME
    checkper = input('- Count Of Check Per Account: ')
    MAX_EXPORT_COUNT = int(checkper)
    if os.path.exists(numbers_filename):
        with open(numbers_filename) as file:
            numbers = [line.replace("\r", "").replace("\n", "")[-12:] for line in file.readlines()]
    else:
        print(f'- File({numbers_filename}) NOT EXISTS')
        return
    if not numbers:
        return print(f'- NO NUMBER IN FILE({numbers_filename})')

    print('\n- Start Clients:')
    added_numbers = []
    bad_numbers = []
    in_progress = True
    while in_progress:
        for f in os.listdir(CHECKER_CLIENTS_DIR):
            if not f.endswith(".session"):
                continue
            to_add_numbers = []
            for _ in range(MAX_EXPORT_COUNT):
                try:
                    to_add_numbers.append(numbers.pop(0))
                except IndexError:
                    in_progress = False
                    break
            if to_add_numbers:
                session_name = f.replace('.session', '')
                print(f'\n- Client({session_name})')
                async with Client(session_name, workdir=CHECKER_CLIENTS_DIR) as client:
                    print(f' - Client({session_name}): Started')

                    print(f' - Client({session_name}): ADD[{", ".join(to_add_numbers)}]')
                    while True:
                        try:
                            res = await client.add_contacts(
                                list(InputPhoneContact(phone=num, first_name=num) for num in to_add_numbers)
                            )
                            print(res.retry_contacts)

                            for user in res.users:
                                to_add_numbers.remove(user.phone)
                                added_numbers.append(user.phone)
                            for contact in res.retry_contacts:
                                numbers.append(contact)
                            print(
                                f' - Client({session_name}): Succeed {len(res.imported)}, Limited: {len(res.retry_contacts)}, Not Joined: {len(to_add_numbers)}')
                        except FloodWait as ex:
                            if not once:
                                await asyncio.sleep(ex.x + 1)
                                continue
                        except RPCError as ex:
                            print(f' - Client({session_name}) Exp: {ex}')
                        break
                    bad_numbers.extend(to_add_numbers)

        if once:
            break

    with open(numbers_filename, '+w') as f:
        f.write('\n'.join(numbers))

    def store(file_name, data_list):
        if not os.path.exists(file_name):
            with open(file_name, '+w'):
                pass

        with open(file_name, 'a') as f:
            f.write('\n'.join(data_list))

    # store(numbers_filename, numbers)
    store('Succeed_Numbers.txt', added_numbers)
    store('Bad_Numbers.txt', bad_numbers)


async def checker_report_status():
    clients = []
    for f in os.listdir(CHECKER_CLIENTS_DIR):
        if not f.endswith(".session"):
            continue
        session_name = f.replace('.session', '')
        print(f'\n    - Check Client({session_name})')
        client = Client(session_name, workdir=CHECKER_CLIENTS_DIR)
        clients.append(client)
        await clients[-1].start()
        clients[-1].add_handler(MessageHandler(callback=lambda c, m: print(m.text), filters=filters.user('SpamBot')))
    for client in clients:
        await client.send(
            raw.functions.messages.StartBot(
                bot=await client.resolve_peer('SpamBot'),
                peer=await client.resolve_peer('SpamBot'),
                random_id=client.rnd_id(),
                start_param='start'
            )
        )

    for client in clients:
        await client.stop()


async def checker_add_client():
    session_name = input('Input session name: ')
    async with Client(session_name, workdir=CHECKER_CLIENTS_DIR) as new_client:
        print(f'- New Client {new_client.storage.database}')


def TelegramPhoneChecker(args):

    if not os.path.exists(CHECKER_CLIENTS_DIR):
        os.mkdir(CHECKER_CLIENTS_DIR)

    if len(args) == 1:
        func = checker_main()
    elif len(args) == 2:
        if args[1] == '--add':
            func = checker_add_client()
        elif args[1] == '--check':
            func = checker_report_status()
        elif args[1] == '--continue':
            func = checker_main(once=False)
        else:
            exit('BAD ARGS')
    else:
        exit('BAD ARGS')

    print('\nHere we go...\n')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(func)
    loop.close()

    print('\nFinish!\n')
# checker end
# dmsender start
DMSENDER_CLIENTS_DIR = './clients'
DMSENDER_TEXT_FILENAME = 'dmsender-text.txt'
DMSENDER_MAX_ADD_COUNT = 40
DMSENDER_SLEEP_INTERVALS = 10
DMSENDER_RETRIES = 3
DMSENDER_ORIGIN_CHAT = ''
dmsender_script_id = 1

dmsender_redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)

dmsender__used_ids = set()


class dmsender_FakeClient(Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.participants_q = asyncio.Queue()
        self.send_task = None
        self.extract_task = None

    async def extract_members(self, chat_id: int):
        async for member in self.iter_chat_members(chat_id):
            try:
                user = member.user
                if not (user.is_self or user.is_deleted):
                    member_peer = await self.resolve_peer(user.id)
                    await self.participants_q.put(
                        raw.types.InputUser(user_id=member_peer.user_id, access_hash=member_peer.access_hash)
                    )
            except Exception as e:
                print(f'    - Client({self.session_name}) Exp : {e}')
        await self.participants_q.put(None)

    async def send_progress(self, chat_id, txt, sleep_time=0, once=True):
        global dmsender__used_ids
        sending = True
        user_peers = []

        while sending:
            while len(user_peers) < DMSENDER_MAX_ADD_COUNT:
                user_peer = await self.participants_q.get()
                if user_peer is None:
                    sending = False
                    break
                key = f'bot:{dmsender_script_id}:sent:{chat_id}'
                if dmsender_redis.sismember(key, user_peer.user_id):
                    continue
                else:
                    dmsender_redis.sadd(key, user_peer.user_id)

                user_peers.append(user_peer)

            for user in user_peers:
                for _ in range(DMSENDER_RETRIES):
                    try:
                        await self.send_message(user.user_id, txt)
                        print(f'      - Client({self.session_name}): send {user.user_id}')
                        await asyncio.sleep(sleep_time)
                    except FloodWait as e:
                        await asyncio.sleep(e.x + 1)
                        continue
                    except RPCError as e:
                        print(f'        - Client({self.session_name}) Exception: {e}')
                    break
                await asyncio.sleep(1)

            if once:
                sending = False
            else:
                await asyncio.sleep(DMSENDER_SLEEP_INTERVALS)

        if self.extract_task is not None:
            self.extract_task.cancel()

    async def get_chat_id(self, chat_id):
        try:
            chat_id = int(chat_id)
        except ValueError:
            try:
                return (await self.join_chat(chat_id)).id
            except UserAlreadyParticipant:
                pass

        return (await self.get_chat(chat_id)).id


async def dmsender_main(once=True, sleep_time=0):

    if os.path.exists(DMSENDER_TEXT_FILENAME):
        with open(DMSENDER_TEXT_FILENAME , encoding="utf8") as file:
            text = file.read()
            if not text:
                return print('Empty text file!')
    else:
        return print(f'FILE({DMSENDER_TEXT_FILENAME}) not found!')

    ori_text = 'origin group id or username: '
    if DMSENDER_ORIGIN_CHAT:
        origin_chat = DMSENDER_ORIGIN_CHAT
        print(f'- {ori_text} {DMSENDER_ORIGIN_CHAT}')
    else:
        origin_chat = input(f'- Enter {ori_text}')

    print('\n- Start Send Clients:')

    clients = []

    for f in os.listdir(DMSENDER_CLIENTS_DIR):
        if not f.endswith(".session"):
            continue
        session_name = f.replace('.session', '')
        print(f'\n- Client({session_name})')
        client = dmsender_FakeClient(session_name, workdir=DMSENDER_CLIENTS_DIR)
        await client.start()
        print(f'  - Client({session_name}): Started')
        clients.append(client)

        print(f'  - Client({session_name}): Identify Origin Chat')
        try:
            origin_chat_id = await client.get_chat_id(origin_chat)
        except (KeyError, ValueError, PeerIdInvalid):
            print(f'  - Client({session_name}) Exception: Origin chat not Found')
            continue
        except RPCError as e:
            print(f'  - Client({session_name}) Exception: {e}')
            continue
        print(f'  - Client({session_name}): Origin Chat ID: {origin_chat_id}')

        client.extract_task = asyncio.ensure_future(client.extract_members(origin_chat_id))

        print(f'    - Client({session_name}): Sending...')

        client.send_task = asyncio.ensure_future(client.send_progress(origin_chat, text, once=once, sleep_time=sleep_time))

    await asyncio.gather(*[clt.send_task for clt in clients if clt.send_task is not None], return_exceptions=True)
    await asyncio.gather(*[clt.stop() for clt in clients])


async def dmsender_report_status():
    clients = []
    for f in os.listdir(DMSENDER_CLIENTS_DIR):
        if not f.endswith(".session"):
            continue
        session_name = f.replace('.session', '')
        print(f'\n    - Check Client({session_name})')
        client = Client(session_name, workdir=DMSENDER_CLIENTS_DIR)
        clients.append(client)
        await clients[-1].start()
        clients[-1].add_handler(MessageHandler(callback=lambda c, m: print(m.text), filters=filters.user('SpamBot')))
    for client in clients:
        await client.send(
            raw.functions.messages.StartBot(
                bot=await client.resolve_peer('SpamBot'),
                peer=await client.resolve_peer('SpamBot'),
                random_id=client.rnd_id(),
                start_param='start'
            )
        )

    for client in clients:
        await client.stop()


async def dmsender_add_client():
    session_name = input('Input session name: ')
    async with Client(session_name, workdir=DMSENDER_CLIENTS_DIR) as new_client:
        print(f'- New Client {new_client.storage.database}')


async def dmsender_usage():
    print('BAD ARGS')

def TelegramDmBulkMsgSender(args):

    if not os.path.exists(DMSENDER_CLIENTS_DIR):
        os.mkdir(DMSENDER_CLIENTS_DIR)

    if len(args) == 1:
        func = dmsender_main()
    elif len(args) == 2:
        if args[1] == '--add':
            func = dmsender_add_client()
        elif args[1] == '--check':
            func = dmsender_report_status()
        elif args[1] == '--continue':
            func = dmsender_main(once=False)
        elif args[1].isdigit():
            func = dmsender_main(sleep_time=int(args[2]))
        else:
            func = dmsender_usage()
    elif len(args) == 3 and args[1] == '--continue' and args[2].isdigit():
        func = dmsender_main(sleep_time=int(args[2]), once=False)
    else:
        func = dmsender_usage()

    print('\nHere we go...\n')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(func)
    loop.close()

    print('\nFinish!\n')
# dmsender end
# adder
ADDER_CLIENTS_DIR = './clients'
ADDER_MAX_ADD_COUNT = 30
ADDER_SLEEP_INTERVALS = 5  # seconds
ADDER_RETRIES = 3
ADDER_ORIGIN_CHAT = ''
ADDER_DESTINATION_CHAT = ''
adder_script_id = 1

adder_redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)

adder__used_ids = set()


class adder_FakeClient(Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.participants_q = asyncio.Queue()
        self.add_task = None
        self.extract_task = None

    async def extract_members(self, chat_id: int):
        async for member in self.iter_chat_members(chat_id):
            try:
                user = member.user
                if not (user.is_self or user.is_deleted):
                    member_peer = await self.resolve_peer(user.id)
                    await self.participants_q.put(
                        raw.types.InputUser(user_id=member_peer.user_id, access_hash=member_peer.access_hash)
                    )
            except Exception as e:
                print(f'    - Client({self.session_name}) Exp : {e}')
        await self.participants_q.put(None)

    async def add_progress(self, chat_id, once=True):
        global adder__used_ids
        adding = True
        user_peers = []
        while adding:

            while len(user_peers) < ADDER_MAX_ADD_COUNT:
                user_peer = await self.participants_q.get()
                if user_peer is None:
                    adding = False
                    break
                key = f'bot:{adder_script_id}:added:{chat_id}'
                if adder_redis.sismember(key, user_peer.user_id):
                    continue
                else:
                    adder_redis.sadd(key, user_peer.user_id)

                user_peers.append(user_peer)

            if user_peers:
                for _ in range(ADDER_RETRIES):
                    try:
                        amount = await self.add_chat_members(chat_id, user_peers)
                        print(f'      - Client({self.session_name}): Add {amount}/{len(user_peers)} Users')
                    except FloodWait as e:
                        await asyncio.sleep(e.x + 1)
                        continue
                    except UserAlreadyParticipant:
                        pass
                    except RPCError as e:
                        print(f'        - Client({self.session_name}) Exception: {e}')
                    break
            if once:
                adding = False
            else:
                await asyncio.sleep(ADDER_SLEEP_INTERVALS)

        if self.extract_task is not None:
            self.extract_task.cancel()

    async def get_chat_id(self, chat_id):
        try:
            chat_id = int(chat_id)
        except ValueError:
            try:
                return (await self.join_chat(chat_id)).id
            except UserAlreadyParticipant:
                pass

        return (await self.get_chat(chat_id)).id

    async def add_chat_members(
            self,
            chat_id: Union[int, str],
            user_ids: Union[Union[int, str, 'raw.types.InputUser'], List[Union[int, str, 'raw.types.InputUser']]],
            forward_limit: int = 100
    ) -> int:

        if isinstance(user_ids, raw.types.InputUser):
            user_peers = [user_ids]
        elif isinstance(user_ids, list) and all([isinstance(user_id, raw.types.InputUser) for user_id in user_ids]):
            user_peers = user_ids
        else:
            return await super().add_chat_members(chat_id, user_ids, forward_limit)

        peer = await self.resolve_peer(chat_id)
        amount = 0
        if isinstance(peer, raw.types.InputPeerChat):
            for user_peer in user_peers:
                try:
                    await self.send(
                        raw.functions.messages.AddChatUser(
                            chat_id=peer.chat_id,
                            user_id=user_peer,
                            fwd_limit=forward_limit
                        )
                    )
                    amount += 1
                except UserAlreadyParticipant:
                    amount += 1
                except RPCError as e:
                    raise e

        else:
            res = await self.send(
                raw.functions.channels.InviteToChannel(
                    channel=peer,
                    users=user_peers
                )
            )
            amount += len(res.users)
        return amount


async def adder_main(once=True):
    ori_text = 'origin group id or username: '
    des_text = 'destination group id or username: '
    if ADDER_ORIGIN_CHAT:
        origin_chat = ADDER_ORIGIN_CHAT
        print(f'- {ori_text} {ADDER_ORIGIN_CHAT}')
    else:
        origin_chat = input(f'- Enter {ori_text}')

    if ADDER_DESTINATION_CHAT:
        destination_chat = ADDER_DESTINATION_CHAT
        print(f'- {des_text} {ADDER_DESTINATION_CHAT}')
    else:
        destination_chat = input(f'- Enter {des_text}')

    print('\n- Start Mirror Clients:')

    # session_names = map(lambda f: f.replace('.session', ''),
    # filter(lambda f: f.endswith(".session"), os.listdir(ADDER_CLIENTS_DIR)))
    # for session_name in session_names:

    clients = []

    for f in os.listdir(ADDER_CLIENTS_DIR):
        if not f.endswith(".session"):
            continue
        session_name = f.replace('.session', '')
        print(f'\n- Client({session_name})')
        client = adder_FakeClient(session_name, workdir=ADDER_CLIENTS_DIR)
        await client.start()
        print(f'  - Client({session_name}): Started')
        clients.append(client)

        # Ensure we got origin chat
        print(f'  - Client({session_name}): Identify Origin Chat')
        try:
            origin_chat_id = await client.get_chat_id(origin_chat)
        except (KeyError, ValueError, PeerIdInvalid):
            print(f'  - Client({session_name}) Exception: Origin chat not Found')
            continue
        except RPCError as e:
            print(f'  - Client({session_name}) Exception: {e}')
            continue
        print(f'  - Client({session_name}): Origin Chat ID: {origin_chat_id}')

        client.extract_task = asyncio.ensure_future(client.extract_members(origin_chat_id))

        # Ensure we got destination chat
        print(f'  - Client({session_name}): Identify Destination Chat')
        try:
            target_chat_id = await client.get_chat_id(destination_chat)
        except (KeyError, PeerIdInvalid):
            print(f'  - Client({session_name}) Exception: Destination Chat not Found')
            continue
        except RPCError as e:
            print(f'  - Client({session_name}) Exception: {e.x}')
            continue
        print(f'  - Client({session_name}): Destination Chat ID: {target_chat_id}')

        print(f'    - Client({session_name}): Mirroring...')

        client.add_task = asyncio.ensure_future(client.add_progress(target_chat_id, once=once))

    await asyncio.gather(*[clt.add_task for clt in clients if clt.add_task is not None], return_exceptions=True)
    await asyncio.gather(*[clt.stop() for clt in clients])


async def adder_report_status():
    clients = []
    for f in os.listdir(ADDER_CLIENTS_DIR):
        if not f.endswith(".session"):
            continue
        session_name = f.replace('.session', '')
        print(f'\n    - Check Client({session_name})')
        client = Client(session_name, workdir=ADDER_CLIENTS_DIR)
        clients.append(client)
        await clients[-1].start()
        clients[-1].add_handler(MessageHandler(callback=lambda c, m: print(m.text), filters=filters.user('SpamBot')))
    for client in clients:
        await client.send(
            raw.functions.messages.StartBot(
                bot=await client.resolve_peer('SpamBot'),
                peer=await client.resolve_peer('SpamBot'),
                random_id=client.rnd_id(),
                start_param='start'
            )
        )

    for client in clients:
        await client.stop()


async def adder_add_client():
    session_name = input('Input session name: ')
    async with Client(session_name, workdir=ADDER_CLIENTS_DIR) as new_client:
        print(f'- New Client {new_client.storage.database}')


def TelegramGroupMemberAdder(args):

    if not os.path.exists(ADDER_CLIENTS_DIR):
        os.mkdir(ADDER_CLIENTS_DIR)

    if len(args) == 1:
        func = adder_main()
    elif len(args) == 2:
        if args[1] == '--add':
            func = adder_add_client()
        elif args[1] == '--check':
            func = adder_report_status()
        elif args[1] == '--continue':
            func = adder_main(once=False)
        else:
            exit('BAD ARGS')
    else:
        exit('BAD ARGS')

    print('\nHere we go...\n')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(func)
    loop.close()

    print('\nFinish!\n')
# adder
# gpsender
GPSENDER_CLIENTS_DIR = './clients'
GPSENDER_TEXT_FILENAME = 'gpsender-text.txt'
GPSENDER_CHATS_FILENAME = 'gpsender-groups.txt'


async def gpsender_send(app, chat_ids, msg):
    for chat_id in chat_ids:
        try:
            await app.join_chat(str(chat_id))
            await app.send_message(str(chat_id), msg)
            print(f' - Client({app.session_name}): send to {chat_id}')
        except FloodWait as e:
            await asyncio.sleep(e.x + 1)
        except Exception as e:
            print(f' - Client({app.session_name}) Error: {e}')
        await asyncio.sleep(0.5)


async def gpsender_main(t=0):
    if os.path.exists(GPSENDER_CHATS_FILENAME):
        with open(GPSENDER_CHATS_FILENAME) as file:
            chats = [line.replace("\r", "").replace("\n", "") for line in file.readlines()]
    else:
        return print(f'- File({GPSENDER_CHATS_FILENAME}) NOT EXISTS')
    if not chats:
        return print(f'- NO CHAT-ID IN FILE({GPSENDER_CHATS_FILENAME})')

    if os.path.exists(GPSENDER_TEXT_FILENAME):
        with open(GPSENDER_TEXT_FILENAME) as file:
            text = file.read()
    else:
        return print(f'- File({GPSENDER_TEXT_FILENAME}) NOT EXISTS')
    if not text:
        return print(f'- NO TEXT IN FILE({GPSENDER_TEXT_FILENAME})')

    print('\n- Start Clients:')

    clients = []
    tasks = []
    for f in os.listdir(GPSENDER_CLIENTS_DIR):
        if not f.endswith(".session"):
            continue

        session_name = f.replace('.session', '')
        print(f'\n- Client({session_name})')
        client = Client(session_name, workdir=GPSENDER_CLIENTS_DIR)
        try:
            await client.start()
            print(f' - Client({session_name}): Started')
        except RPCError as e:
            print(f' - Client({session_name}) Not Started: {e}')
            continue
        clients.append(client)
        tasks.append(asyncio.ensure_future(gpsender_send(client, chats, text)))

    await asyncio.gather(*tasks)
    await asyncio.gather(*[client.stop() for client in clients])


async def gpsender_corn_main(sleep_time):
    while True:
        await gpsender_main()
        print(f'Sleep for {sleep_time} seconds')
        await asyncio.sleep(sleep_time)


async def gpsender_add_client():
    session_name = input('Input session name: ')
    async with Client(session_name, workdir=GPSENDER_CLIENTS_DIR) as new_client:
        print(f'- New Client {new_client.storage.database}')


async def gpsender_usage():
    print('BAD ARGS')


def TelegramMultiGroupsMsgSender(args):

    if not os.path.exists(GPSENDER_CLIENTS_DIR):
        os.mkdir(GPSENDER_CLIENTS_DIR)

    if len(args) == 1:
        func = gpsender_main()
    elif len(args) == 2:
        if args[1].isdigit():
            func = gpsender_corn_main(int(args[1]))
        elif args[1] == '--add':
            func = gpsender_add_client()
        else:
            func = gpsender_usage()
    else:
        func = gpsender_usage()

    print('\nHere we go...\n')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(func)
    loop.close()

    print('\nFinish!\n')
# gpsender end
if __name__ == '__main__':
    sysargs = sys.argv
    if len(sysargs) == 1:
        print('Please specify the function')
    elif sysargs[1] == 'prof':
        TelegramBulkAccountProfileChanger(sysargs[1:])
    elif sysargs[1] == 'forward':
        Telegramchannelpostsforwader(sysargs[1:])
    elif sysargs[1] == 'join':
        TelegramMemberAutoJoiner(sysargs[1:])
    elif sysargs[1] == 'checker':
        TelegramPhoneChecker(sysargs[1:])
    elif sysargs[1] == 'dmsender':
        TelegramDmBulkMsgSender(sysargs[1:])
    elif sysargs[1] == 'adder':
        TelegramGroupMemberAdder(sysargs[1:])
    elif sysargs[1] == 'gpsender':
        TelegramMultiGroupsMsgSender(sysargs[1:])
    else:
        print('Wrong function! list:\n prof\n forward\n join\n checker\n dmsender\n adder\n gpsender')
