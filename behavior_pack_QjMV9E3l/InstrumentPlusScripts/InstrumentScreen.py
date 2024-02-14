# coding=utf-8
import mod.client.extraClientApi as clientApi
import api, modConfig

ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()
Comp = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()

key_list = [
    [48, 50, 52, 53, 55, 57, 59],
    [60, 62, 64, 65, 67, 69, 71],
    [72, 74, 76, 77, 79, 81, 83]
]
note_name_list = "CDEFGAB"

class InstrumentScreen(ScreenNode):

    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)

    def Init(self):
        pass

    def Create(self):
        self.musicComp = clientApi.GetEngineCompFactory().CreateCustomAudio(clientApi.GetLocalPlayerId())
        self.open_button = self.GetBaseUIControl("/open_button").asButton()
        self.open_button.AddTouchEventParams({"isSwallow": True})
        self.open_button.SetButtonTouchUpCallback(self.OpenButtonCallback)
        self.open_button.SetVisible(False)
        self.close_button = self.GetBaseUIControl("/close_button").asButton()
        self.close_button.AddTouchEventParams({"isSwallow": True})
        self.close_button.SetButtonTouchUpCallback(self.CloseButtonCallback)
        self.close_button.SetVisible(False)
        self.GetBaseUIControl("/keyboard_panel").SetVisible(False)
        self.back = self.GetBaseUIControl("/back_button").asButton()
        self.back.AddTouchEventParams({"isSwallow": True})
        self.back.SetVisible(False)

        for line in range(1, 4):
            for key in range(1, 8):
                tempButton = self.GetBaseUIControl("/keyboard_panel/line_%s_panel/key_%s_button" % (line, key)).asButton()
                tempButton.AddTouchEventParams({"isSwallow": True})
                tempButton.SetButtonTouchDownCallback(self.OnKeyButtonCallback)

    def OpenButtonCallback(self, data):
        self.SetVisible("/open_button", False)
        self.SetVisible("/close_button", True)
        self.SetVisible("/keyboard_panel", True)
        self.back.SetVisible(True)
        api.hideGUI(True)
        item = clientApi.GetEngineCompFactory().CreateItem(clientApi.GetLocalPlayerId()).GetCarriedItem()
        self.pos = clientApi.GetEngineCompFactory().CreatePos(clientApi.GetLocalPlayerId()).GetPos()
        self.ins_id = api.getInstrumentId(item["itemName"])
        clientApi.GetSystem(modConfig.modName, modConfig.ClientSystemName).NotifyToServer("ClientMusicEvent", {"stop": True})
        comp = clientApi.GetEngineCompFactory().CreateItem(levelId)
        itemData = comp.GetItemBasicInfo(item["itemName"])
        print(itemData)
        self.GetBaseUIControl("/keyboard_panel/Instrument_name_text").asLabel().SetText(text=itemData["itemName"])

    def CloseButtonCallback(self, data):
        self.SetVisible("/open_button", True)
        self.SetVisible("/close_button", False)
        self.SetVisible("/keyboard_panel", False)
        self.back.SetVisible(False)
        api.hideGUI(False)
        clientApi.GetSystem(modConfig.modName, modConfig.ClientSystemName).NotifyToServer("ClientMusicEvent", {"stop": False})

    def OnKeyButtonCallback(self, data):
        buttonPath = data["ButtonPath"]
        print(buttonPath)
        line = int(buttonPath.split("/")[2].split("_")[1])
        key = int(buttonPath.split("/")[3].split("_")[1])
        note = key_list[line-1][key-1]
        sound_name = "%sd.%s" % (self.ins_id, note)
        self.musicComp.Play(sound_name, self.pos, 1.0, 1.0)
        clientApi.GetSystem(modConfig.modName, modConfig.ClientSystemName).NotifyToServer("ClientSoundEvent", {"sound_name": sound_name, "pos": self.pos, "playerId": clientApi.GetLocalPlayerId()})

        self.GetBaseUIControl("/keyboard_panel/pressed_key_text").asLabel().SetText("当前：%s" % note_name_list[key-1])



