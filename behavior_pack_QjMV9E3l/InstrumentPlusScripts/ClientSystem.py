# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
from mod.client.ui.screenNode import ScreenNode
from mod_log import logger
import modConfig
import api

ClientSystem = clientApi.GetClientSystemCls()


class InstrumentPlusClientSystem(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        logger.info("客户端系统初始化成功")
        self.ListenEvent()

    # 监听引擎ScriptTickClientEvent事件，引擎会执行该tick回调，1秒钟30帧
    def OnTickClient(self):
        """
        Driven by event, One tick way
        """
        pass

    # 被引擎直接执行的父类的重写函数，引擎会执行该Update回调，1秒钟30帧
    def Update(self):
        """
        Driven by system manager, Two tick way
        """
        pass

    def Destroy(self):
        pass

    def ListenEvent(self):
        eventDict = {
            "UiInitFinished": self.UiInitFinishedCallback,
            "OnCarriedNewItemChangedClientEvent": self.ShowInstrumentOpenScreen

        }
        for eventItem in eventDict.items():
            self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), eventItem[0], self, eventItem[1])
        self.ListenForEvent(modConfig.modName, modConfig.ServerSystemName, "ServerSoundEvent", self, self.OnServerSoundEvent)
        self.ListenForEvent(modConfig.modName, modConfig.ServerSystemName, "ServerMusicEvent", self, self.OnServerMusicEvent)

    def UiInitFinishedCallback(self, data):
        uiKey = "instrument_0_screen"
        clientApi.RegisterUI(modConfig.modName, uiKey, "InstrumentPlusScripts.InstrumentScreen.InstrumentScreen", uiKey + ".main")
        clientApi.CreateUI(modConfig.modName, uiKey, {"isHud": 1})
        self.InstrumentScreen = clientApi.GetUI(modConfig.modName, uiKey)

        self.ShowInstrumentOpenScreen()

    def ShowInstrumentOpenScreen(self, *args):
        item = clientApi.GetEngineCompFactory().CreateItem(clientApi.GetLocalPlayerId()).GetCarriedItem()
        self.back = self.InstrumentScreen.GetBaseUIControl("/back_button").asButton()
        if item is not None and "sfkm:instrument" in item["itemName"]:
            self.InstrumentScreen.GetBaseUIControl("/open_button").SetVisible(True)
        else:
            self.InstrumentScreen.GetBaseUIControl("/keyboard_panel").SetVisible(False)
            self.InstrumentScreen.GetBaseUIControl("/open_button").SetVisible(False)
            self.InstrumentScreen.GetBaseUIControl("/close_button").SetVisible(False)
            self.InstrumentScreen.GetBaseUIControl("/back_button").SetVisible(False)
            api.hideGUI(hide=False)
            clientApi.GetEngineCompFactory().CreateCustomAudio(clientApi.GetLocalPlayerId()).DisableOriginMusic(False)
        del item

    def OnServerSoundEvent(self, data):
        comp = clientApi.GetEngineCompFactory().CreateCustomAudio(clientApi.GetLocalPlayerId())
        if clientApi.GetLocalPlayerId() != data["playerId"]:
            comp.Play(data["sound_name"], data["pos"], 1.0, 1.0)

    def OnServerMusicEvent(self, data):
        # 玩家开启乐器时暂停音乐
        comp = clientApi.GetEngineCompFactory().CreateCustomAudio(clientApi.GetLocalPlayerId())
        comp.DisableOriginMusic(data["stop"])
