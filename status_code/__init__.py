# all op_code and error_code of this project is defined here

class _const:
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value


class OpCode(_const):
    def __init__(self):
        self.GET_ALL_COMMENT = 1
        self.GET_TODAY_COMMENT = 2
        self.SET_PUBLIC_OPNION = 3
        self.SET_INCREASE_RATE = 4
        self.SET_INDEX_PREDICTION = 5
        self.SET_INDEX_INFO = 6
        self.SET_STOCK_INFO = 7
        self.SET_INDEX_DAILY = 8
        self.SET_STOCK_DAILY = 9
        self.SET_STOCK_COMMENT = 10
        self.SET_INDEX_COMMENT = 11
        self.GET_USER_INFO = 12
        self.SET_USER_INFO = 13
        self.UPDATE_USER_INFO = 14
        self.DELETE_USER_INFO = 15
        self.GET_INDUSTRY_INDEX_PREDICTION = 16
        self.GET_MARKET_INDEX_PREDICTION = 17
        self.GET_STOCK_PREDICTION = 18
        self.GET_FEATURE = 19
        self.GET_STOCK = 20
        self.GET_STOCK_SELECTION = 21
        self.GET_STOCK_INFO = 22
        self.SET_COLLECTION = 23
        self.DELETE_COLLECTION = 24


class ErrorCode(_const):
    def __init__(self):
        self.SUCCESS = 0
        self.JSON_PARSING_ERROR = 1
        self.EMPTY_PARAMETER = 2
        self.ILLEGAL_PARAMETER = 3
        self.OPCODE_NOT_MATCH = 4
        self.OPCODE_NOT_EXIST = 5
        self.DB_ERROR = 6
        self.INTERNAL_ERROR = 7
        self.ITERATE_EN = 8

