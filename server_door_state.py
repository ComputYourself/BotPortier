from gpiozero import Button, LED
from signal import pause
from _thread import start_new_thread
import socket
from apscheduler.schedulers.background import BackgroundScheduler

def door_closed():
    global current_door_state 
    current_door_state = '**Closed**'

def door_opened():
    global current_door_state 
    current_door_state = '**Open**'

def close_for_night():
    global current_door_state
    current_door_state = '**Close**'

def on_new_client(connection, client_address):
    try:
        while True:
            data = connection.recv(255).decode('utf-8')
            if data == 'door_state':
                connection.sendall(current_door_state.encode('utf-8'))
            else:
                break
    finally:
        connection.close()

gros_bouton = Button(4)

sched = BackgroundScheduler()
sched.add_job(close_for_night, 'cron', day_of_week='mon-thu,sun', hour=1, timezone='Europe/Paris')
sched.add_job(close_for_night, 'cron', day_of_week='fri-sat', hour=3, timezone='Europe/Paris')
sched.start()

current_door_state = '**Open**' if gros_bouton.is_pressed else '**Closed**'
gros_bouton.when_pressed = door_opened
gros_bouton.when_released = door_closed

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('', 54321)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(3)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    print('new connection from {}'.format(client_address))
    start_new_thread(on_new_client,(connection,client_address))
    print('thread launched')

sock.close()
