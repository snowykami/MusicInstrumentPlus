# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
from mod_log import logger

import modConfig

ServerSystem = serverApi.GetServerSystemCls()


class InstrumentPlusServerSystem(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        logger.info("服务端系统初始化成功")
        self.ListenEvent()

    # ScriptTickServerEvent的回调函数，会在引擎tick的时候调用，1秒30帧（被调用30次）
    def OnTickServer(self):
        """
        Driven by event, One tick way
        """
        pass

    # 这个Update函数是基类的方法，同样会在引擎tick的时候被调用，1秒30帧（被调用30次）
    def Update(self):
        """
        Driven by system manager, Two tick way
        """
        pass

    def Destroy(self):
        pass

    def ListenEvent(self):
        self.ListenForEvent(modConfig.modName, modConfig.ClientSystemName, "ClientSoundEvent", self, self.OnClientSoundEvent)
        self.ListenForEvent(modConfig.modName, modConfig.ClientSystemName, "ClientMusicEvent", self, self.OnClientMusicEvent)

    def OnClientSoundEvent(self, data):
        self.BroadcastToAllClient(eventName="ServerSoundEvent", eventData=data)

    def OnClientMusicEvent(self, data):
        self.BroadcastToAllClient(eventName="ServerMusicEvent", eventData=data)
