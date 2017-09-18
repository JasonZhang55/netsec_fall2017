from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER


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