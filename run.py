from server import *
import socket
import random
import webbrowser

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)


if __name__ == "__main__":
    app.run(host=IPAddr, port=5623)