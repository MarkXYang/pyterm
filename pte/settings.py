# GTK/Gnome imports
import pygtk
pygtk.require('2.0')
import gtk,pango,vte,gconf

# Python imports
import os

# Local imports
import commands

c = gconf.client_get_default()

__me__ = None # god forgive me for this...

def get_main():
    return __me__

def set_main(klass):
    global __me__
    __me__ = klass

default_dict = dict(
            title="Shell",
            font=pango.FontDescription("monospace"),
            cmd=os.environ['SHELL'],
            cwd=os.environ['HOME'],
            icon=None
        )

MAIN_PATH = "/apps/pyterm"
PROFILES_PATH = "%s/profiles"%MAIN_PATH
SAVED_TABS_PATH = "%s/saved"%MAIN_PATH
BINDINGS_PATH = "%s/bindings"%MAIN_PATH
PROFILES_COUNT_PATH = "%s/count"%PROFILES_PATH
SAVED_TABS_ALLOW_PATH = "%s/allow_savetabs"%MAIN_PATH

def get_default_profile():
   return get_profile(0)
   
def new_profile(d):
    pcount = c.get_int(PROFILES_COUNT_PATH)
    c.set_int(PROFILES_COUNT_PATH,pcount+1)
    path = "%s/%d"%(PROFILES_PATH,pcount)
    c.set_string(path+"/title",d['title'])
    c.set_string(path+"/cmd",d['cmd'])
    c.set_string(path+"/cwd",d['cwd'])
    c.set_string(path+"/font",d['font'].to_string())
    c.set_int(path+"/icon",d['icon'] or 0)
    d['id'] = pcount
    return d
            
   
def get_profile(pid):
    path = "%s/%d"%(PROFILES_PATH,pid)
    if not c.dir_exists(path):
        return new_profile(default_dict)
    return dict(
            id=pid,
            title=c.get_string(path+"/title"),
            font=pango.FontDescription(c.get_string(path+"/font")),
            cmd=c.get_string(path+"/cmd"),
            cwd=c.get_string(path+"/cwd"),
            icon=c.get_int(path+"/icon")
        )

def get_profiles():
    ret = {}
    for i in c.all_dirs(PROFILES_PATH):
        ret[i] = get_profile(int(i[i.rfind('/')+1:]))
    return ret

def get_saved_tabs():
    ret = []
    for i in c.all_dirs(SAVED_TABS_PATH):
        t=c.get_string(i+"/title")
        p=get_profile(c.get_int(i+"/profile"))
        ret += [ dict(title=t, profile=p, widget=None) ]
    return ret

def save_tabs(terms):    
    if c.dir_exists(SAVED_TABS_PATH):
        c.remove_dir(SAVED_TABS_PATH)
    if c.get_bool(SAVED_TABS_ALLOW_PATH):
        for (i,t) in enumerate(terms):
            c.set_string("%s/%d/title"%(SAVED_TABS_PATH,i), t['title'] or t['profile']['title'])
            c.set_int("%s/%d/profile"%(SAVED_TABS_PATH,i), t['profile']['id'])


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

def write_bindings(b):
    for abind in b.keys():
        c.set_string("%s/%s"%(BINDINGS_PATH,abind),b[abind]['key'])


def read_bindings():
    ret = {}
    if not c.dir_exists(BINDINGS_PATH):
        write_bindings(default_bindings)
        return default_bindings

    for abind in default_bindings.keys():
        ret[abind] = { 'key' : c.get_string("%s/%s"%(BINDINGS_PATH,abind)),
                       'command' : default_bindings[abind]['command'] }
    return ret
