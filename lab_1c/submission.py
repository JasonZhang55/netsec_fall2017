from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER
from playground.asyncio_lib.testing import  TestLoopEx
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import  MockTransportToProtocol
import asyncio


# Packet definition
class RequestLogIn(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.student_Runjie.RequestLogIn"
    DEFINITION_VERSION = "1.0"

    FIELDS = [("ID", UINT32),
              ("requestLogIn", STRING)]


class LogInWindow(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.student_Runjie.LogInWindow"
    DEFINITION_VERSION = "1.0"

    FIELDS = [("ID", UINT32),
              ("usernameBox", STRING),
              ("passwordsBox", STRING)]


class LogInInfo(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.student_Runjie.LogInInfo"
    DEFINITION_VERSION = "1.0"

    FIELDS = [("ID", UINT32),
              ("username", STRING),
              ("passwords", STRING)]


class PhoneNumReq(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.student_Runjie.PhoneNumReq"
    DEFINITION_VERSION = "1.0"

    FIELDS = [("ID", UINT32),
              ("passfail", STRING),
              ("telBox", STRING)]


class Retry(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.student_Runjie.Retry"
    DEFINITION_VERSION = "1.0"

    FIELDS = [("ID", UINT32),
              ("passfail", STRING),
              ("usernameBox", STRING),
              ("passwordsBox", STRING)]


class PhoneNum(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.student_Runjie.PhoneNum"
    DEFINITION_VERSION = "1.0"

    FIELDS = [("ID", UINT32),
              ("phoneNumber", STRING)]


class VerificationNumReq(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.student_Runjie.VerificationNumReq"
    DEFINITION_VERSION = "1.0"

    FIELDS = [("ID", UINT32),
              ("verificationNumBox", STRING)]


class VerificationNum(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.student_Runjie.VerificationNum"
    DEFINITION_VERSION = "1.0"

    FIELDS = [("ID", UINT32),
              ("verificationNum", STRING)]


class Result(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.student_Runjie.Result"
    DEFINITION_VERSION = "1.0"

    FIELDS = [("ID", UINT32),
              ("passfail", STRING)]


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
        # print(self.packet1.requestLogIn, self.packet1.ID)
        # self.transport.write(self.packet1Bytes)

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


class EchoServerProtocol():
    def __init__(self):
        self.transport = None

        self.packet2 = LogInWindow()
        self.packet2.ID = 1
        self.packet2.usernameBox = "Please enter your username."
        self.packet2.passwordsBox = "Please enter your passwords."
        self.packet2Bytes = self.packet2.__serialize__()

        self.packet4 = PhoneNumReq()
        self.packet4.ID = 2
        self.packet4.passfail = "pass"
        self.packet4.telBox = "Please enter your phone number."
        self.packet4Bytes = self.packet4.__serialize__()

        self.packet5 = Retry()
        self.packet5.ID = 2
        self.packet5.passfail = "fail"
        self.packet5.usernameBox = "Please enter your username again."
        self.packet5.passwordsBox = "Please enter your passwords again."
        self.packet5Bytes = self.packet5.__serialize__()

        self.packet7 = VerificationNumReq()
        self.packet7.ID = 3
        self.packet7.verificationNumBox = "Please enter the verification number you see."
        self.packet7Bytes = self.packet7.__serialize__()

        self.packet9 = Result()
        self.packet9.ID = 4
        self.packet9.passfail = "pass"
        self.packet9Bytes = self.packet9.__serialize__()

        self.deserializer = PacketType.Deserializer()

    def connection_made(self, transport):
        print("Echo server connected to client!")
        self.transport = transport
        # self.deserializer = PacketType.Deserializer()

    def data_received(self, data):
        # print("Server is receiving data")
        self.deserializer.update(data)
        for pkt in self.deserializer.nextPackets():
            if isinstance(pkt, RequestLogIn):
                print(self.packet2.usernameBox, self.packet2.passwordsBox, self.packet2.ID)
                self.transport.write(self.packet2Bytes)

            elif isinstance(pkt, LogInInfo):
                if pkt.username == "rzhang" and pkt.passwords == "1123":
                    print(self.packet4.passfail, "\n", self.packet4.telBox, self.packet4.ID)
                    self.transport.write(self.packet4Bytes)
                else:
                    print(self.packet5.passfail, "\n", self.packet5.usernameBox, self.packet5.passwordsBox, self.packet5.ID)
                    self.transport.write(self.packet5Bytes)

            elif isinstance(pkt, Retry):
                if pkt.username == "rzhang" and pkt.passwords == "1123":
                    print(self.packet4.passfail, "\n", self.packet4.telBox, self.packet4.ID)
                    self.transport.write(self.packet4Bytes)
                else:
                    print(self.packet5.passfail, "\n", self.packet5.usernameBox, self.packet5.passwordsBox, self.packet5.ID)
                    self.transport.write(self.packet5Bytes)

            elif isinstance(pkt, PhoneNum):
                print(self.packet7.verificationNumBox, self.packet7.ID)
                self.transport.write(self.packet7Bytes)

            elif isinstance(pkt, VerificationNum):
                if pkt.verificationNum == "1234":
                    print(self.packet9.passfail, self.packet9.ID)
                    self.transport.write(self.packet9Bytes)
                else:
                    print("Fail", self.packet9.ID)
                    self.transport.write(self.packet9Bytes)

    def connection_lost(self, exc):
        self.transport = None



def basicProtocolTest():
    asyncio.set_event_loop(TestLoopEx())
    clientProtocol = EchoClientProtocol()
    serverProtocol = EchoServerProtocol()
    cTransport, sTransport = MockTransportToProtocol.CreateTransportPair(clientProtocol, serverProtocol)
    clientProtocol.connection_made(cTransport)
    serverProtocol.connection_made(sTransport)

    clientProtocol.send_request()


if __name__ == "__main__":
    basicProtocolTest()