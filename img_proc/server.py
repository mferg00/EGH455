from random import randrange
import time
import requests

# class Server:
#     def __init__(self, ip, port):
#         self.URL = str(ip) + ':' + str(port) + '/process'
#         self.server_URL = 'http://172.19.33.44:5000/process'

#     def send(self, num_corrosive, num_dangerous_goods, aruco_markers):
#         res = requests.post(self.server_URL, 
#             json = {'corrosive': str(num_corrosive), 
#              'dangerous_goods': str(num_dangerous_goods), 
#              'aruco': str(aruco_markers) }
#         )
#         if(res.ok):
#             print(res.json())

#     def test(self):
#         try:
#             self.send(randrange(100), randrange(100), [randrange(1000) for _ in range(randrange(100))])
#         except Exception as e:
#             print(e)

#         time.sleep(1)

# if __name__ == '__main__':
#     server = Server('localhost', 5000)

#     while(True):
#         server.test()

server_URL = 'http://172.19.33.44:5000/process'
res = requests.post(server_URL, 
            json = {'corrosive': 1, 
             'dangerous_goods': 2, 
             'aruco': [1, 2, 3] }
        )
if(res.ok):
    print(res.json())