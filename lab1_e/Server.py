from Packets import *
from playground.network.common import  StackingProtocol, StackingTransport, StackingProtocolFactory
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import  MockTransportToProtocol
import asyncio
import playground


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


class PassThrough1(StackingProtocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        print("This is passthrough1")
        self.transport = transport
        higherTransport = StackingTransport(self.transport)
        self.higherProtocol().connection_made(higherTransport)

    def data_received(self, data):
        self.higherProtocol().data_received(data)


class PassThrough2(StackingProtocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        print("This is passthrough2")
        self.transport = transport
        higherTransport = StackingTransport(self.transport)
        self.higherProtocol().connection_made(higherTransport)

    def data_received(self, data):
        self.higherProtocol().data_received(data)


def basicServerTest():
    loop = asyncio.get_event_loop()

    f = StackingProtocolFactory(lambda: PassThrough1(), lambda: PassThrough2())
    ptConnector = playground.Connector(protocolStack=f)
    playground.setConnector("passthrough", ptConnector)

    # loop.set_debug(enabled=True)
    coro = playground.getConnector('passthrough').create_playground_server(lambda: EchoServerProtocol(), 8888)
    server = loop.run_until_complete(coro)

    print("Serving on ...")
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    basicServerTest()