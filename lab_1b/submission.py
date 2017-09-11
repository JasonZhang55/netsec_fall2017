from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER


class RequestLogIn(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.student_Runjie.RequestLogIn"
    DEFINITION_VERSION = "1.0"


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
              ("TelBox", STRING)]


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
              ("verificationNum", UINT32)]


class Result(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.student_Runjie.Result"
    DEFINITION_VERSION = "1.0"

    FIELDS = [("ID", UINT32),
              ("passfail", STRING)]


def basicUnitTest1():
    packet1 = RequestLogIn()
    packet1Bytes = packet1.__serialize__()
    packet1a = RequestLogIn().Deserialize(packet1Bytes)
    assert packet1 == packet1a

    packet2 = LogInWindow()
    packet2.ID = 1
    packet2.usernameBox = "Please enter your username."
    packet2.passwordsBox = "Please enter your passwords."
    packet2Bytes = packet2.__serialize__()
    packet2a = LogInWindow.Deserialize(packet2Bytes)
    assert packet2 == packet2a

    packet3 = LogInInfo()
    packet3.ID = 1
    packet3.username = "rzhang"
    packet3.passwords = "1123"
    packet3Bytes = packet3.__serialize__()
    packet3a = LogInInfo.Deserialize(packet3Bytes)
    assert packet3 == packet3a

    packet4 = PhoneNumReq()
    packet4.ID = 2
    packet4.passfail = "pass"
    packet4.TelBox = "Please enter your phone number."
    packet4Bytes = packet4.__serialize__()
    packet4a = PhoneNumReq.Deserialize(packet4Bytes)
    assert packet4 == packet4a

    packet5 = Retry()
    packet5.ID = 1
    packet5.passfail = "fail"
    packet5.usernameBox = "Please enter your username again."
    packet5.passwordsBox = "Please enter your passwords again."
    packet5Bytes = packet5.__serialize__()
    packet5a = Retry.Deserialize(packet5Bytes)
    assert packet5 == packet5a

    packet6 = PhoneNum()
    packet6.ID = 2
    packet6.phoneNumber = "4431234567"
    packet6Bytes = packet6.__serialize__()
    packet6a = PhoneNum.Deserialize(packet6Bytes)
    assert packet6 == packet6a

    packet7 = VerificationNumReq()
    packet7.ID = 3
    packet7.verificationNumBox = "Please enter the verification number you see."
    packet7Bytes = packet7.__serialize__()
    packet7a = VerificationNumReq.Deserialize(packet7Bytes)
    assert packet7 == packet7a

    packet8 = VerificationNum()
    packet8.ID = 3
    packet8.verificationNum = 1234
    packet8Bytes = packet8.__serialize__()
    packet8a = VerificationNum.Deserialize(packet8Bytes)
    assert packet8 == packet8a

    packet9 = Result()
    packet9.ID = 3
    packet9.passfail = "pass"
    packet9Bytes = packet9.__serialize__()
    packet9a = Result.Deserialize(packet9Bytes)
    assert packet9 == packet9a
    if packet9 == packet9a:
        print("Wow, these two packets are the same!\n")

#Try Deserializer()
def basicUnitTest2():
    packetA = LogInInfo()
    packetA.ID = 1
    packetA.username = "rzhang1"
    packetA.passwords = "1123"

    packetB = LogInInfo()
    packetB.ID = 2
    packetB.username = "rzhang2"
    packetB.passwords = "1123"

    packetC = LogInInfo()
    packetC.ID = 3
    packetC.username = "rzhang3"
    packetC.passwords = "1123"

    pktBytes = packetA.__serialize__() + packetB.__serialize__() + packetC.__serialize__()

    deserializer = PacketType.Deserializer()
    print("Starting with {} bytes of data".format(len(pktBytes)))
    while len(pktBytes) > 0:
        chunk, pktBytes = pktBytes[:10], pktBytes[10:]
        deserializer.update(chunk)
        print("Another 10 bytes loaded into deserializer. Left bytes={}".format(len(pktBytes)))
        for packet in deserializer.nextPackets():
            print("got a packet!")
            if packet == packetA:
                print("It's packet A")
            elif packet == packetB:
                print("It's packet B")
            elif packet == packetC:
                print("It's packet C")


if __name__ == "__main__":
    basicUnitTest1()
    basicUnitTest2()  #try deserializer