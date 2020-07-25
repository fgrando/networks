import struct
import socket
import datetime

class Packer:
    def __init__(self):
        ''' data in this self.dict must have at least 2 values:
        o: order of this field in the struct (necessary while iterating the dictionary because dict.keys() has arbitrary order)
        p: 'c', where c is the respective field size (https://docs.python.org/3/library/struct.html#format-characters)
        v: <value> the value stored for this member
        '''
        self.data = {}

    def pack(self):
        return b"".join( [struct.pack('!'+self.data[k]['p'], self.data[k]['v']) for k in sorted( self.data.keys(), key=lambda item: self.data[item]['o'] )] )


class Pianno:

    # Piano keys:
    class Key (Packer):
        def __init__(self):
            self.data = {\
            "code" :{'p': 'i', 'o': 1, 'v': 0},            
            "note" :{'p': 'c', 'o': 2, 'v': 'A'},
            "freq" :{'p': 'i', 'o': 3, 'v': 0},
            }

    def __init__(self):
        self.data = {\
            "model"   :{'p': '6s', 'o': 1, 'v': "Yamaha"},
            "pressed" :{'p': 'i' , 'o': 2, 'v': 0},
        }
        self.pressedKeys = []


    def readPressedKeys(self):
        # pretend some pressed keys are read

        k1 = self.Key()
        k1.data["code"]["v"] = 1
        k1.data["note"]["v"] = "C"
        k1.data["freq"]["v"] = 10
        self.pressedKeys.append(k1)
        
        k2 = self.Key()
        k2.data["code"]["v"] = 2
        k2.data["note"]["v"] = "D"
        k2.data["freq"]["v"] = 11
        self.pressedKeys.append(k2)
        
        k3 = self.Key()
        k3.data["code"]["v"] = 3
        k3.data["note"]["v"] = "G"
        k3.data["freq"]["v"] = 12
        self.pressedKeys.append(k3)

    def pack(self):
        self.data["pressed"]["v"] = len(self.pressedKeys)

        header = b"".join( [struct.pack('!'+self.data[k]['p'], self.data[k]['v']) for k in sorted( self.data.keys(), key=lambda item: self.data[item]['o'] )] )
        items = b"".join( [s.pack() for s in self.pressedKeys] )
        return header + items
    
    def __str__(self):
        return " ".join(("%02x"%ord(b)) for b in self.pack())


def send(payload, ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return sock.sendto(payload, (ip, port))

pianno = Pianno()
pianno.readPressedKeys()

msg = pianno.pack()
print(pianno)
send(msg, "127.0.0.1", 50001)