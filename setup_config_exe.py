from distutils.core import setup
import py2exe

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        # for the versioninfo resources
        self.version = "1.0"
        self.company_name = "CloudMill Games"
        self.copyright = ""
        self.name = "BattleCity Remake Config"
		
BattleCityTgt = Target(
    # used for the versioninfo resource
    description = "BattleCity Remake Config",

    # what to build
    script = "battlecityconfig.py",
    icon_resources = [(1, "icon.ico")],
    dest_base = "Config")
	
setup(windows=[BattleCityTgt],
     options = {'py2exe': {'compressed': 1, 'optimize': 2, 'bundle_files':1} },
     zipfile=None
	 )
