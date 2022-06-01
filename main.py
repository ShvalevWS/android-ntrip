from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
import time, base64, socket

KV = """
MyBL:
    orientation: "vertical"
    size_hint: (0.95, 0.95)
    pos_hint: {"center_x": 0.5, "center_y": 0.5}
    GridLayout:
        cols: 2
        rows: 7
        Label:
            font_size: "30sp"
            text: root.mount_label
        TextInput:
            id: Mount_inp
            multiline: False

        Label:
            font_size: "30sp"
            text: root.server_label
        TextInput:
            id: Serv_inp
            multiline: False    

        Label:
            font_size: "30sp"
            text: root.port_label
        TextInput:
            id: Port_inp
            multiline: False    

        Label:
            font_size: "30sp"
            text: root.login_label
        TextInput:
            id: Login_inp
            multiline: False    

        Label:
            font_size: "30sp"
            text: root.pass_label
        TextInput:
            id: Pass_inp
            multiline: False    

        Button:
            text: "Start"
            bold: True
            background_color: '#00FFCE'
            on_press: root.send_nmea()
        Button:
            text: "Stop"
            bold: True
            background_color: '#00FFCE'
            on_press: root.stop_stream()
        Label:
            font_size: "30sp"
            text: root.resp_label
        Label:
            font_size: "15sp"
            multiline: True
            text_size: self.width*0.98, None
            size_hint_x: 1.0
            size_hint_y: None
            height: self.texture_size[1] + 15            
            text: root.resp_body
"""


class MyBL(BoxLayout):
    mount_label = StringProperty("Mountpoint")
    server_label = StringProperty("Host")
    port_label = StringProperty("Port")
    login_label = StringProperty("Login")
    pass_label = StringProperty("Pass")
    resp_label = StringProperty("Response:")
    resp_body = StringProperty(" ")

    def send_nmea(self):
        string = '$GNGGA,203441.00,5036.93769,N,03635.53378,E,1,03,5.99,191.5,M,16.2,M,,*46'
        mount = self.ids.Mount_inp.text
        username = self.ids.Login_inp.text
        password = self.ids.Pass_inp.text
        port = self.ids.Port_inp.text
        host = self.ids.Serv_inp.text
        pwd = base64.b64encode("{}:{}".format(username, password).encode('ascii'))
        pwd = pwd.decode('ascii')
        header = \
            f"GET /{mount} HTTP/1.1\r\n" + \
            f"Host: {host}\r\n" + \
            "Ntrip-Version: Ntrip/2.0\r\n" + \
            "User-Agent: NTRIP NtripClientPOSIX/1.51\r\n" + \
            "Connection: close\r\n" + \
            "Authorization: Basic {}\r\n\r\n".format(pwd)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        s.send(header.encode('ascii') + string.encode('ascii'))
        time.sleep(2)
        data = s.recv(2048)
        print(data)
        self.set_data_label(data=data)
        print(header)
        return data

    def set_data_label(self, data):
        self.resp_body = str(data)


class MyApp(App):
    running = True

    def build(self):
        return Builder.load_string(KV)

    def stop(self):
        self.running = False


MyApp().run()
