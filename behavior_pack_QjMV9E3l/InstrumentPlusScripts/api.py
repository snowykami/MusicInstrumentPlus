import mod.client.extraClientApi as clientApi


def getInstrumentId(itemName):
    if "sfkm:instrument" in itemName:
        return int(itemName.split("_")[-1])
    else:
        return -1


def hideGUI(hide=True):
    clientApi.HideHudGUI(hide)
    clientApi.HideArmorGui(hide)
    clientApi.HideChangePersonGui(hide)
    clientApi.HideExpGui(hide)
    clientApi.HideHealthGui(hide)
    clientApi.HideHorseHealthGui(hide)
    clientApi.HideHudGUI(hide)
    clientApi.HideHungerGui(hide)
    clientApi.HideInteractGui(hide)
    clientApi.HideJumpGui(hide)
    clientApi.HideMoveGui(hide)
    clientApi.HideSlotBarGui(hide)
    clientApi.HideSneakGui(hide)
    clientApi.HideSwimGui(hide)
    clientApi.HideWalkGui(hide)

