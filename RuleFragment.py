from enum import Enum


class StringPosition(Enum):
    HEAD = 1
    TAIL = 2
    ANY = 3


class RuleFragment:

    flagString: str
    flagType: StringPosition
    isPositiveRule: bool

    def __init__(self, flagString: str, flagType: StringPosition, isPositiveRule: bool) -> None:
        self.flagString = flagString
        self.flagType = flagType
        self.isPositiveRule = isPositiveRule

    def test(self, inString: str) -> bool:
        r = None
        if self.flagType == StringPosition.HEAD:
            r = inString.startswith(self.flagString)
        elif self.flagType == StringPosition.TAIL:
            r = inString.endswith(self.flagString)
        elif self.flagType == StringPosition.ANY:
            r = self.flagString in inString

        if self.isPositiveRule:
            return r
        else:
            return not r

    @staticmethod
    def fromDict(inData: dict):
        flagType = None
        try:
            flagType = StringPosition[inData["type"]]
        except KeyError as ke:
            print(
                "Position type paramenter in this item is invalid, skip. Only 'HEAD' or 'TAIL' or 'ANY' is currently supportted. | {}".format(inData))
            return None
        return RuleFragment(inData["flag"], flagType, inData["isPositiveRule"])


if __name__ == "__main__":
    tRule = RuleFragment("haha:", StringPosition["HEAD"], True)

    tstr = "haha: miao!"
    print(tstr, " - ", tRule.test(tstr))

    tRule = RuleFragment("haha:", StringPosition["TAIL"], False)

    print(tstr, " - ", tRule.test(tstr))

    tRule = RuleFragment("haha:", StringPosition.ANY, True)
    tstr = "lalala haha: miao!"
    print(tstr, " - ", tRule.test(tstr))

    print(StringPosition["ERROR"])
