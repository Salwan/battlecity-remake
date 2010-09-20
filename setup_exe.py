from distutils.core import setup
import py2exe

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        # for the versioninfo resources
        self.version = "0.9.0"
        self.company_name = "CloudMill Games"
        self.copyright = "Copyright 1985 NAMCO LTD"
        self.name = "BattleCity Arabic Remake"
		
BattleCityTgt = Target(
    # used for the versioninfo resource
    description = "BattleCity Arabic Remake",

    # what to build
    script = "battlecity.py",
    icon_resources = [(1, "icon.ico")],
    dest_base = "BattleCity")
	
setup(windows=[BattleCityTgt],
     options = {'py2exe': {'compressed': 1, 'optimize': 2, 'bundle_files':1} },
     zipfile=None
	 )
