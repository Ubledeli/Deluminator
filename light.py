import socket
import json, time
from machine import Pin, PWM
from ws_connection import ClientClosedError
from ws_server import WebSocketServer, WebSocketClient


# B, R, G, 12v, B, R, G, 12v W, 12v W, 12v
pwm = [14,12,13,15,2,4,5]
pins = [PWM(Pin(i)) for i in pwm]

class TestClient(WebSocketClient):
    def __init__(self, conn, pins = pins):
        super().__init__(conn)
        self._pins = pins

    def process(self):
        try:
            msg = self.connection.read()
            if not msg:
                return
            print(msg)
            try:
                data = json.loads(msg.decode())
                self.connection.write(msg)
                for i,p in enumerate(pins):
                    p.duty(data[i])
            except:
                self.connection.write(msg+ "exception")
        except ClientClosedError:
            self.connection.close()


class TestServer(WebSocketServer):
    def __init__(self):
        super().__init__(page="test.html", max_connections=5)

    def _make_client(self, conn):
        return TestClient(conn)


server = TestServer()
server.start()
try:
    while True:
        server.process_all()
except KeyboardInterrupt:
    pass
server.stop()
