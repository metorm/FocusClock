from RuleFragment import RuleFragment


class WhiteListRule:

    processNameRule: RuleFragment
    windowTiltleRule: RuleFragment

    def __init__(self, processNameRule, windowTiltleRule) -> None:
        self.processNameRule = processNameRule
        self.windowTiltleRule = windowTiltleRule
        pass

    def test(self, procName, winName) -> bool:
        return self.processNameRule.test(procName) and self.windowTiltleRule.test(winName)


class WhiteList:

    whiteListItems: list[WhiteListRule]

    def __init__(self) -> None:
        self.whiteListItems = []

    def test(self, procName, winName) -> bool:
        rList = [rule.test(procName, winName) for rule in self.whiteListItems]
        return any(rList)

    def buildFromDict(self, whiteListConfigData: dict):
        for item in whiteListConfigData:
            processNameRule = RuleFragment.fromDict(item["process"])
            windowTiltleRule = RuleFragment.fromDict(item["title"])
            if (processNameRule is not None) and (windowTiltleRule is not None):
                self.whiteListItems.append(WhiteListRule(
                    processNameRule, windowTiltleRule))


if __name__ == "__main__":
    import json
    with open("SampleConfig.json") as jFile:
        configData = json.load(jFile)

        whiteList = WhiteList()
        whiteList.buildFromDict(configData["whiteList"])
