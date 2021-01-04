from twisted.internet.protocol import ReconnectingClientFactory
from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory
import json
import subprocess
import multiprocessing

server = "127.0.0.1"  # Server IP Address or domain eg: tabvn.com
# server = "18.217.115.28"
port = 3001  # Server Port
id_cam = 'stream'
seri = '5#57Vx'

streaming_process = None


class App:

    def __init__(self):

        print("App is initial.")

    def stop_camera(self):
        global streaming_process

        if streaming_process is not None:

            print("Begin stopping camera")

            streaming_process.kill
            streaming_process.terminate
            streaming_process = None
        else:
            streaming_process.terminate
            print("No streaming process so we dont need to do stop")

    def show_camera(self, is_bool):

        global streaming_process

        print("We need to show camera {0}".format(is_bool))

        if is_bool:

            print("--------------------------------",streaming_process)

            if streaming_process is None:
                # ffmpeg_command = 'ffmpeg -re -i /home/iwin/Documents/react/video-streaming-service/storage/ayo.mp4 -c:v libx264 -preset veryfast -maxrate 3000k -bufsize 6000k -pix_fmt yuv420p -g 50 -c:a aac -b:a 160k -ac 2 -ar 44100 -f flv rtmp://localhost/live/'+id_cam
                # ffmpeg_command = 'ffmpeg -f lavfi -i anullsrc -rtsp_transport udp -i rtsp://admin:FRCCYL@192.168.18.209:554 -tune zerolatency -vcodec libx264 -t 12:00:00 -pix_fmt + -c:v copy -c:a aac -strict experimental -f flv rtmp://localhost/live/'+id_cam
                ffmpeg_command = 'ffmpeg -f lavfi -i anullsrc -rtsp_transport udp -i rtsp://admin:FRCCYL@192.168.18.209:554 -tune zerolatency -vcodec libx264 -t 12:00:00 -pix_fmt + -c:v copy -c:a aac -strict experimental -f flv rtmp://18.217.115.28/live/'+id_cam
                # ffmpeg_command = 'ffmpeg -re -i /home/iwin/Documents/react/video-streaming-service/storage/ayo.mp4 -c:v libx264 -preset veryfast -maxrate 3000k -bufsize 6000k -pix_fmt yuv420p -g 50 -c:a aac -b:a 160k -ac 2 -ar 44100 -f flv rtmp://18.217.115.28/live/'+id_cam

                streaming_process = subprocess.Popen(ffmpeg_command, shell=True, stdin=subprocess.PIPE)
                # streaming_process.communicate()
                
            else:

                print("Streaming is in process we are not accept more streaming.")
        else:

            self.stop_camera()

    def decode_message(self, payload):

        print("Got message need to decode {0}".format(payload))
        json_message = json.loads(payload)
        action = json_message.get('action')
        payload_value = json_message.get('payload')

        if action == 'stream':
            self.show_camera(payload_value)


class AppProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Connected to the server")
        self.factory.resetDelay()

    def onOpen(self):
        print("Connection is open.")

        # when connection is open we send a test message the the server.

        def hello_server():
            # message = {"action": "pi_online", "payload": {"id": "tabvn", "secret": "key"}}

            # self.sendMessage(json.dumps(message))
            self.sendMessage(u"Gateway 01 connected".encode('utf8'))
            # self.factory.reactor.callLater(1, hello_server)

        hello_server()

    def onMessage(self, payload, isBinary):
        if (isBinary):
            print("Got Binary message {0} bytes".format(len(payload)))
        else:
            print("Got Text message from the server {0}".format(payload.decode('utf8')))
            # need to decode this message and know what is server command
            app = App()
            app.decode_message(payload)

    def onClose(self, wasClean, code, reason):
        print("Connect closed {0}".format(reason))


class AppFactory(WebSocketClientFactory, ReconnectingClientFactory):
    protocol = AppProtocol

    def clientConnectionFailed(self, connector, reason):
        print("Unable connect to the server {0}".format(reason))
        self.retry(connector)

    def clientConnectionLost(self, connector, reason):
        print("Lost connection and retrying... {0}".format(reason))
        self.retry(connector)


if __name__ == '__main__':
    import sys
    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)
    factory = AppFactory(u"ws://{0}".format(server).format(":").format(port))
    reactor.connectTCP(server, port, factory)
    reactor.run()
