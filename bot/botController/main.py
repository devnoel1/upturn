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


async def adder_main(destination_chat, origin_chat, once=True):

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


async def adder_add_client(session_name):
    async with Client(session_name, workdir=ADDER_CLIENTS_DIR) as new_client:
        print(f'- New Client {new_client.storage.database}')

def TelegramGroupMemberAdder(destination_chat, origin_chat,args,session_name):

    if not os.path.exists(ADDER_CLIENTS_DIR):
        os.mkdir(ADDER_CLIENTS_DIR)

    if len(args) == 1:
        func = adder_main(destination_chat, origin_chat)
    elif len(args) == 2:
        if args[1] == '--add':
            func = adder_add_client(session_name)
        elif args[1] == '--check':
            func = adder_report_status()
        elif args[1] == '--continue':
            func = adder_main(destination_chat, origin_chat,once=False)
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
