import network
from threading import Thread
import json
from DB import *
# loads: python <= json
# dumps: python => json

sockIn = network.connect_InSocket()
sockTcpIn = network.connect_tcpInSocket()
running = True
clients = dict()
players = dict()
messages = list()
network.alive = True
udp_reader = Thread(target=network.socket_reader, args=(sockIn, messages))
udp_reader.start()
while running:
    if not messages:
        continue
    data, address = messages.pop()
    msg = json.loads(data)
    print(msg, "mes")
    key = msg['key']
    if key == 'login':
        msg = bd_for_login()
    if key == 'bad_try_login':
        add_bad_try_login(msg["login"], msg["password"], msg["time"])
        msg = []
    if key == 'admin_download':
        msg = admin_download()
    if key == 'hotels_download':
        msg = hotels_download()
    if key == "ban_admin":
        msg = bann_admin(msg["login"], msg["reason"])
    if key == "delete_admin":
        msg = delete_admin(msg["login"])
    if key == "delete_hotel":
        msg = delete_hotel(msg["name"])
    if key == "add_admin":
        admin = msg['login'].split('|||')
        msg = add_admin(admin)
    if key == "change_info_admin":
        admin = msg['login'].split('|||')
        msg = change_info_about_admin(admin)
    if key == "change_info_hotel":
        hotel = msg['name'].split('|||')
        msg = change_info_about_hotel(hotel)
    if key == "add_hotel":
        hotel = msg['name'].split('|||')
        msg = add_hotel(hotel)
    if key == "bad_try_download":
        msg = bad_try_download()
    if key == "rooms":
        msg = rooms_download()
    if key == "guests":
        msg = download_guests()
    if key == "get_hotel":
        msg = get_hotel(msg["login"])
    if key == "mowe_out_guest":
        msg = mowe_out_guest(msg["passport"])
    if key == "get_info_about_one_admin":
        msg = get_info_about_one_admin(msg["login"])
    if key == "check_in_hotel_guest":
        msg = check_in_hotel_guest(msg["passport"], msg["hotel"], msg["room"])
    if key == "delete_room":
        msg = delete_room(msg["hotel"], msg["number"])
    if key == "add_room":
        msg = add_room([msg["hotel"], msg["number"], msg["rooms"], msg["s"]])
    if key == "change_info_about_room":
        msg = change_info_about_room(msg["hotel"], msg["number"], msg["rooms"], msg["s"])
    if key == "delete_guest":
        msg = delete_guest(msg["passport"])
    if key == "add_guest":
        msg = add_guest(list(msg.values())[1:])
    if key == "change_info_about_guest":
        msg = change_info_about_guest(list(msg.values()))
    address = network.connect_OutSocket(address=address[0], port=5556)
    msg = json.dumps(msg)
    network.sock_send(address, msg)


network.close_sock(sockIn)
network.alive = False
