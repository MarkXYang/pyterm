# GTK/Gnome imports
import pygtk
pygtk.require('2.0')
import gtk,pango,vte,gconf

# Python imports
import os

# Local imports
import commands


__me__ = None # god forgive me for this...
__confinst__ = None
MAIN_PATH = "/apps/pyterm"
PROFILES_PATH = "%s/profiles"%MAIN_PATH
SESSIONS_PATH = "%s/saved"%MAIN_PATH
BINDINGS_PATH = "%s/bindings"%MAIN_PATH
SAVE_SESSIONS_PATH = "%s/save_sessions"%MAIN_PATH

default_profile =   dict(
                        title="Shell",
                        font=pango.FontDescription("monospace"),
                        cmd=os.environ['SHELL'],
                        cwd=os.environ['HOME'],
                        name='Default',
                        icon=None
                    )

default_bindings = dict(
        show_settings   = { "key":'F12', "command": commands.show_settings },
        fullscreen      = { "key":'F11', "command": commands.fullscreen },
        tab_new         = { "key":'<Control>N', "command": commands.tab_new },
        tab_close       = { "key":'<Control>W', "command": commands.tab_close },
        tab_duplicate   = { "key":'<Control><Shift>D', "command": commands.tab_duplicate },
        tab_move_left   = { "key":'<Control><Shift>Left', "command": commands.tab_move_left },
        tab_move_right  = { "key":'<Control><Shift>Right', "command": commands.tab_move_right },
        tab_shift_left  = { "key":'<Shift>Left', "command": commands.tab_shift_left },
        tab_shift_right = { "key":'<Shift>Right', "command": commands.tab_shift_right },
        tab_select_1    = { "key":'<Alt>1', "command": lambda a,b,c: commands.tab_select(1,a,b,c) },
        tab_select_2    = { "key":'<Alt>2', "command": lambda a,b,c: commands.tab_select(2,a,b,c) },
        tab_select_3    = { "key":'<Alt>3', "command": lambda a,b,c: commands.tab_select(3,a,b,c) },
        tab_select_4    = { "key":'<Alt>4', "command": lambda a,b,c: commands.tab_select(4,a,b,c) },
        tab_select_5    = { "key":'<Alt>5', "command": lambda a,b,c: commands.tab_select(5,a,b,c) },
        tab_select_6    = { "key":'<Alt>6', "command": lambda a,b,c: commands.tab_select(6,a,b,c) },
        tab_select_7    = { "key":'<Alt>7', "command": lambda a,b,c: commands.tab_select(7,a,b,c) },
        tab_select_8    = { "key":'<Alt>8', "command": lambda a,b,c: commands.tab_select(8,a,b,c) },
        tab_select_9    = { "key":'<Alt>9', "command": lambda a,b,c: commands.tab_select(9,a,b,c) },
        )


c = gconf.client_get_default()

class Configuration(object):
    @staticmethod
    def inst():
        global __confinst__
        if not __confinst__:
            __confinst__ = Configuration()
        return __confinst__

    def get_profile(self, name):
        path = "%s/%s"%(PROFILES_PATH,name)
        return dict(
                    name=name,
                    title=c.get_string(path+"/title"),
                    font=pango.FontDescription(c.get_string(path+"/font")),
                    cmd=c.get_string(path+"/cmd"),
                    cwd=c.get_string(path+"/cwd"),
                    icon=c.get_int(path+"/icon")
                )

    def get_profiles(self):
        ret = {}
        for i in c.all_dirs(PROFILES_PATH):
            name = i[i.rfind('/')+1:]
            ret [name] = self.get_profile(name)
        if not ret:
            ret["Default"] = self.save_profile("Default",  default_profile) 
        return ret
     
   
    def save_profile(self, name, d):
        path = "%s/%s"%(PROFILES_PATH,name)
        c.set_string(path+"/title",d['title'])
        c.set_string(path+"/cmd",d['cmd'])
        c.set_string(path+"/cwd",d['cwd'])
        c.set_string(path+"/font",d['font'].to_string())
        c.set_int(path+"/icon",d['icon'] or 0)
        d['name'] = name
        return d
            
    def set_profiles(self, profs):
        for (pname, prof) in profs.items():
            save_profile(pname, prof)

    def get_sessions(self):
        ret = []
        if c.dir_exists(SESSIONS_PATH):
            for i in c.all_dirs(SESSIONS_PATH):
                t=c.get_string(i+"/title")
                p=self.get_profile(c.get_string(i+"/profile"))
                ret += [ dict(title=t, profile=p, widget=None) ]
        return ret

    def set_sessions(self,terms):    
        if c.dir_exists(SESSIONS_PATH):
            c.remove_dir(SESSIONS_PATH)
        if c.get_bool(SAVE_SESSIONS_PATH) or True: #FIXME
            for (i,t) in enumerate(terms):
                c.set_string("%s/%d/title"%(SESSIONS_PATH,i), t['title'] or t['profile']['title'])
                c.set_string("%s/%d/profile"%(SESSIONS_PATH,i), t['profile']['name'])

    def set_bindings(self,b):
        for abind in b.keys():
            c.set_string("%s/%s"%(BINDINGS_PATH,abind),b[abind]['key'])

    def get_bindings(self):
        ret = {}
        if not c.dir_exists(BINDINGS_PATH):
            self.set_bindings(default_bindings)
            return default_bindings

        for abind in default_bindings.keys():
            key = c.get_string("%s/%s"%(BINDINGS_PATH,abind))
            if key:
                ret[abind] = { 'key' : key, 'command' : default_bindings[abind]['command'] }
        return ret

    profiles = property(get_profiles, set_profiles, doc = "Dict of profiles")
    sessions = property(get_sessions, set_sessions, doc = "List of sessions")
    bindings = property(get_bindings, set_bindings, doc = "Dict of bindings")
    main     = None


conf = Configuration.inst

__all__ = [ conf ]
