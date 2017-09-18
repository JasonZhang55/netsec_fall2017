from Packets import *

from playground.network.testing import  MockTransportToProtocol
import asyncio
import playground


# Protocol realize
class EchoClientProtocol():
    def __init__(self):
        self.transport = None

        self.packet1 = RequestLogIn()
        self.packet1.ID = 1
        self.packet1.requestLogIn = "I want to log in my account."
        self.packet1Bytes = self.packet1.__serialize__()

        self.packet3 = LogInInfo()
        self.packet3.ID = 2
        self.packet3.username = "rzhang"
        self.packet3.passwords = "1123"
        self.packet3Bytes = self.packet3.__serialize__()

        self.packet6 = PhoneNum()
        self.packet6.ID = 3
        self.packet6.phoneNumber = "4431234567"
        self.packet6Bytes = self.packet6.__serialize__()

        self.packet8 = VerificationNum()
        self.packet8.ID = 4
        self.packet8.verificationNum = "1234"
        self.packet8Bytes = self.packet8.__serialize__()

        self.deserializer = PacketType.Deserializer()

    def connection_made(self, transport):
        print("Echo client connected to server!")
        self.transport = transport
        print(self.packet1.requestLogIn, self.packet1.ID)
        self.transport.write(self.packet1Bytes)

    def data_received(self, data):
        # print("Client is receiving data")

        self.deserializer.update(data)
        for pkt in self.deserializer.nextPackets():

            if isinstance(pkt, LogInWindow):
                print(self.packet3.username, self.packet3.passwords, self.packet3.ID)
                self.transport.write(self.packet3Bytes)

            elif isinstance(pkt, PhoneNumReq):
                print(self.packet6.phoneNumber, self.packet6.ID)
                self.transport.write(self.packet6Bytes)

            elif isinstance(pkt, Retry):
                print(self.packet3.username, self.packet3.passwords, self.packet3.ID)
                self.transport.write(self.packet3Bytes)

            elif isinstance(pkt, VerificationNumReq):
                print(self.packet8.verificationNum, self.packet8.ID)
                self.transport.write(self.packet8Bytes)

            elif isinstance(pkt, Result):
                print("Log in finish.")

        # self.transport.close()

    def send_request(self):
        print(self.packet1.requestLogIn, self.packet1.ID)
        self.transport.write(self.packet1Bytes)

    def connection_lost(self, exc):
        self.transport = None


def basicClientTest():
    loop = asyncio.get_event_loop()
    coro = playground.getConnector().create_playground_connection(lambda: EchoClientProtocol(), '20174.1.1.1', 8888)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    basicClientTest()