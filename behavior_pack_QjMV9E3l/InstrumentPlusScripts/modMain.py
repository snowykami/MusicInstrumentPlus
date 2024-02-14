# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi
import modConfig


@Mod.Binding(name="InstrumentPlusScripts", version="0.0.1")
class InstrumentPlusMod(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def ServerInit(self):
        serverApi.RegisterSystem(modConfig.modName, modConfig.ServerSystemName, modConfig.ServerSystemClsPath)

    @Mod.DestroyServer()
    def ServerDestroy(self):
        pass

    @Mod.InitClient()
    def ModClientInit(self):
        clientApi.RegisterSystem(modConfig.modName, modConfig.ClientSystemName, modConfig.ClientSystemClsPath)

    @Mod.DestroyClient()
    def eModClientDestroy(self):
        pass
