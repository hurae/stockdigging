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
        self.SET_PUBLIC_OPINION = 3
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
        self.GET_INDEX_FEATURE_HISTORY = 19
        self.GET_STOCK_FEATURE_HISTORY = 20
        self.GET_INDEX_FEATURE_TODAY = 21
        self.GET_STOCK_FEATURE_TODAY = 22
        self.SEARCH = 23
        self.FILTER = 24
        self.GET_STOCK_INFO = 25
        self.SET_COLLECTION = 26
        self.DELETE_COLLECTION = 27
        self.GET_CATEGORY_BY_CODE = 28
        self.GET_INFO_BY_CATEGORY = 29

    def route(self, code):
        if code in [1, 2, 16, 17, 18, 19, 20, 21, 22]:
            return "/"
        elif code == 3:
            return "/opinion"
        elif code in [4, 5]:
            return "/increase"
        elif code in [6, 7, 8, 9]:
            return "/info"
        elif code in [10, 11]:
            return "/comment"
        elif code in [12, 15]:
            return "/userid"
        elif code == 13:
            return "/new"
        elif code == 14:
            return "/update"
        elif code == 23:
            return "/search"
        elif code == 24:
            return "/filter"
        elif code == 25:
            return "/stock"
        elif code in [26, 27]:
            return "/collection"
        else:
            return "error"


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
        self.ITERATE_END = 8
        self.COMMENT_NOT_UPDATED = 9
        self.error_msg = [
            'success',
            'error in JSON parsing',
            'parameter cannot be empty',
            'illegal parameter',
            'opcode not match',
            'opcode not exist',
            'database connection failed',
            'system internal error',
            'iterate ended',
            'Comments not updated today'
        ]


_global_dict = {}

def _init():  # 初始化
    global _global_dict
    _global_dict = {}


def set_value(key, value):
    """ 定义一个全局变量 """
    _global_dict[key] = value


def get_value(key, defValue=None):
    """ 获得一个全局变量,不存在则返回默认值 """
    try:
        return _global_dict[key]
    except KeyError:
        return defValue
