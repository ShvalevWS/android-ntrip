#!/usr/bin/kivy
from variables import *


class NtripScreen(Screen):
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
        self.set_data_label(data=data)
        return data

    def set_data_label(self, data):
        if "HTTP/1.1 200 OK" in str(data):
            self.resp_body = "HTTP/1.1 200 OK"
        else:
            self.resp_body = "Something went wrong :("


class BluetoothScreen(Screen):
    def discover_devices(self):
        service = DiscoveryService()
        devices = service.discover(2)
        for address, name in devices.items():
            print("Name: {}, Address: {}".format(name, address))




buildKV = Builder.load_file('app.kv')


class MyApp(App):
    running = True

    def build(self):
        return buildKV

    def stop(self):
        self.running = False


if __name__ == "__main__":
    MyApp().run()
