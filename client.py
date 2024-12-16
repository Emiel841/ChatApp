import socket
import threading
import flet as ft

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect(ip, port):
    client.connect((ip, port))

connect('127.0.0.1', 55555)

nickname = input("Enter nickname: ")


def main(page):


    def send_button_clicked(e):
        message_in_box = text_input.value
        send_msg(message_in_box)
        maincol.controls.append(ft.Text(message_in_box, color="purple"))
        text_input.value = ""
        page.update()

    def recive():
        while True:
            try:
                message = client.recv(1024).decode('ascii')
                if message == "WHOAREYOU":
                    client.send(nickname.encode('Ascii'))
                else:
                    display_message(message)
            except:
                display_message("Error")
                client.close()
                break

    def display_message(message):
        maincol.controls.append(ft.Text(message, color="blue"))
        page.update()


    def send_msg(msg):
        msg_list = []
        iterate = msg.split(" ")

        for word in iterate:
            found = False
            for swear_word in banned_words:
                if swear_word == word:
                    found = True
            if found:
                hashtags = []
                for i in range(len(word)):
                    hashtags.append("#")
                filtered = ''.join(hashtags)
                msg_list.append(filtered)
            else:
                msg_list.append(word)


        msg = ' '.join(msg_list)
        client.send((nickname + ": " + msg).encode('ascii'))

    f = open("banned_words.txt", "r")
    banned_words = []
    for line in f:
        banned_words.append(line.strip('\n'))

    recive_thread = threading.Thread(target=recive)
    recive_thread.start()
    

    maincol = ft.Column()
    text_input = ft.TextField(hint_text="Start chatting")
    send_button = ft.ElevatedButton(text="Submit", on_click=send_button_clicked)
    page.add(maincol, ft.Row(controls=[text_input, send_button]))

ft.app(main)

