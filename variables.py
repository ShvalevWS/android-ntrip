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