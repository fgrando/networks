import socket

host = ("127.0.0.1", 50001)
replyMaxSize = 1024

payload = str.encode("hello server!")

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

n = sock.sendto(payload, host)
print("sent: '{}' ({} bytes)".format(payload, n))

reply = sock.recvfrom(replyMaxSize)[0]
print("rcvd: '{}'".format(reply))

