from channels.consumer import SyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
import json

class MySyncConsumer(SyncConsumer):

    def websocket_connect(self, event):  # this handler(client) requests to create connection with the server.
        print("websocket connected",event)

        self.send({                      # this method accepts the connection from server side. 
            "type": "websocket.accept",
        })

    # def websocket_receive(self, event):  # msg is recieved from client to server  (client sends the data to server and server recieves the data)
    #     print("msg recieved from client....",event)
    #     print("msg recieved from client....",event['text'])

    #     for i in range(10):
    #         self.send({                   
    #             "type": "websocket.send",
    #             "text": str(i),
    #         })
    #         sleep(1)

            ## self.send({                   #this method is used to send the data from server to client.(server send the data to the client.)
            ##     "type": "websocket.send",
            ##     "text": 'msg from server to client async consumer,
            ## })

    def websocket_receive(self, event):  # msg is recieved from client to server  (client sends the data to server and server recieves the data)
       
        print("msg recieved from client....",event)
        print("msg recieved from client....",event['text'])

        for i in range(10):
            self.send({                   
                "type": "websocket.send",
                "text": json.dumps({'count':i}),  #convert dictionary to string bcz we can not send python object to client,,,so we have to use json.dumps()
            })
            sleep(1)        

    def websocket_disconnect(self,event):
        print("websocket discconnected")    
        raise StopConsumer()


#Async consumer
from channels.consumer import AsyncConsumer
class MyAsyncConsumer(AsyncConsumer):

    '''
    Connect - receive event
    send to the application when the client initailly opens a connection and is about to finish the websocekt handshake
    "type":"websocket.connect"
    ''' 

    async def websocket_connect(self, event):  
        print("websocket connected",event)

        '''
        Accept - send event  (application sne d the client ko ki hnm mujhe connection accept krna hai)
        semd by the application(server) when it wishes to accept an incoming connections.
        "type":"wesocket.connect"
        "subprotocols:None
        "headers":[name,value]
        '''
        await self.send({
            "type": "websocket.accept",
        })


    '''
    Recieve - recieve event
    sent to the application when data is recived from the client.
    "type":websocket.recieve
    "bytes":None (the msg content,if it was binary mode or None,optional; if missing equivalent to None.) # additional parameter
    "text":None # additional parameter
    '''
    async def websocket_receive(self, event):
        print("websocket recieved",event)

        '''
        Send - send event
        sent by the application (to send a data msg to the client) 
        "type":"websocket.send"
        "bytes":None (the msg content,if it was binary mode or None,optional; if missing equivalent to None.) # additional parameter
        "text":None # additional parameter
        '''
        for i in range(50):
            await self.send({
            "type": "websocket.send",
            "text": str(i),
            })
            await asyncio.sleep(1)
        # await self.send({
        #     "type": "websocket.send",
        #     "text": 'msg from server to client async consumer',
        # })


    '''
    Disconnect - recieve event
    "type":"websocket.disconnect"
    "code":"you can write your own code when socket is disconnected".
    '''
    async def websocket_disconnect(self,event):
        print("websocket discconnected")   
        raise StopConsumer()


'''
Close - send event
send by the application to tell the server to close the connection
'''

import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))