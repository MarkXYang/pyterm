#!/usr/bin/env python
    
#----------------------------------------------------------------------
# settings_window.py
# Eli Yukelzon
# 08/14/2006
#----------------------------------------------------------------------

import sys

from GladeWindow import *
import gtk,gobject,pango
import settings 

#----------------------------------------------------------------------

class SettingsWindow(GladeWindow):

    #----------------------------------------------------------------------

    def __init__(self, prefix='.'):

        filename = prefix+'/glade/settings.glade'
        self.loading = False

        widget_list = [
            'helpbutton1',
            'cancelbutton1',
            'okbutton1',
            'chkSaveSessions',
            'btnAddProfile',
            'btnDelProfile',
            'btnRenameProfile',
            'lstProfiles',
            'lstBindings',
            'cmbTabPos',
            'edtName',
            'edtTitle',
            'edtCmd',
            'edtCwd',
            'edtFont',
            'edtIcon'
            ]

        handlers = [
            'on_chkSaveSessions_toggled',
            'on_cmbTabPos_changed',
            'on_profileData_changed',
            'on_btnAddProfile_activate',
            'on_btnDelProfile_activate',
            'on_btnRenameProfile_activate',
            'on_lstProfiles_row_activated',
            'on_lstBindings_row_activated'
            ]

        top_window = 'dlgSettings'
        GladeWindow.__init__(self, filename, top_window, widget_list, handlers)
        self.widgets['edtCmd'].connect("selection-changed", self.on_profileData_changed)
        self.widgets['edtCwd'].connect("selection-changed", self.on_profileData_changed)

    #----------------------------------------------------------------------

    def read_settings(self, conf):
        self.conf = conf
        self.widgets['chkSaveSessions'].set_active(conf.save_sessions)
        for i,l in enumerate(self.widgets['cmbTabPos'].get_model()):
            if l[0] == conf.tab_position:
                self.widgets['cmbTabPos'].set_active(i)
                break

        self.show_bindings()
        self.show_profiles()

    def show_profiles(self):
        model = gtk.TreeStore(gobject.TYPE_PYOBJECT, gobject.TYPE_STRING)
        for name,profile in self.conf.profiles.items():
            iter = model.insert_before(None, None)
            model.set_value(iter, 0, profile)
            model.set_value(iter, 1, name)
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Profiles", renderer, text=1)
        self.widgets['lstProfiles'].set_model(model)
        self.widgets['lstProfiles'].append_column(column)
        self.widgets['lstProfiles'].get_selection().select_iter(model.get_iter_root())
        self.on_lstProfiles_row_activated()

    def show_bindings(self):
        g = {}
        for (bname,b) in settings.default_bindings.items():
            if not b['group'] in g:
                g[b['group']] = []
            g[b['group']] += [ (b,bname) ]
        model = gtk.TreeStore(gobject.TYPE_PYOBJECT, gobject.TYPE_STRING, gobject.TYPE_STRING,)
        for (gname,b) in g.items():
            iter = model.insert_before(None, None)
            model.set_value(iter, 1, gname)
            for (bind,bindname) in b:
                sub_iter = model.insert_after(iter, None)
                model.set_value(sub_iter, 0, bind)
                model.set_value(sub_iter, 1, bind['title'])
                model.set_value(sub_iter, 2, bind['key'])
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Title", renderer, text=1)
        column2 = gtk.TreeViewColumn("Binding", renderer, text=2)
        self.widgets['lstBindings'].set_model(model)
        self.widgets['lstBindings'].append_column(column)
        self.widgets['lstBindings'].append_column(column2)
        self.widgets['lstBindings'].expand_all()


            
        
    def write_settings(self):
        idx = self.widgets['cmbTabPos'].get_active()
        lbl = self.widgets['cmbTabPos'].get_model()[idx][0]
        self.conf.tab_position = lbl
        self.conf.save_sessions = self.widgets['chkSaveSessions'].get_active()
        p = {}
        for i in self.widgets['lstProfiles'].get_model():
            profile,name = i[0], i[1]
            p[name] = profile
        self.conf.profiles = p

    def on_chkSaveSessions_toggled(self, *args):
        pass

    #----------------------------------------------------------------------

    def on_cmbTabPos_changed(self, *args):
        pass

    #----------------------------------------------------------------------

    def on_btnAddProfile_activate(self, *args):
        pass

    #----------------------------------------------------------------------

    def on_btnDelProfile_activate(self, *args):
        pass

    #----------------------------------------------------------------------

    def on_btnRenameProfile_activate(self, *args):
        pass

    #----------------------------------------------------------------------

       

    def on_profileData_changed(self, *args):
        if self.loading:
            return
        model, old_iter = self.widgets['lstProfiles'].get_selection().get_selected()
        name,profile = model.get_value(old_iter,1), model.get_value(old_iter,0)
        name = self.widgets['edtName'].get_text()
        profile['title']=self.widgets['edtTitle'].get_text()
        profile['cwd']=self.widgets['edtCwd'].get_filename()
        profile['cmd']=self.widgets['edtCmd'].get_filename()
        profile['font']=pango.FontDescription(self.widgets['edtFont'].get_font_name())
        profile['icon'] = self.widgets['edtIcon'].get_filename() or None
        model.set_value(old_iter,1,name)
        model.set_value(old_iter,0,profile)
       
    def on_lstProfiles_row_activated(self, *args):
        model, old_iter = self.widgets['lstProfiles'].get_selection().get_selected()
        name,profile = model.get_value(old_iter,1), model.get_value(old_iter,0)
        self.loading = True

        self.widgets['edtName'].set_editable(not profile['sacred'])
        self.widgets['edtName'].set_text(name)
        self.widgets['edtTitle'].set_text(profile['title'] or name)
        self.widgets['edtCwd'].set_filename(profile['cwd'])
        self.widgets['edtCmd'].set_filename(profile['cmd'])
        self.widgets['edtFont'].set_font_name(profile['font'].to_string())
        if profile['icon']:
            self.widgets['edtIcon'].set_filename(profile['icon'])
        self.loading = False

    def on_lstBindings_row_activated(self, *args):
        pass


    


#----------------------------------------------------------------------

def main(argv):

    w = SettingsWindow()
    w.show()
    gtk.main()

#----------------------------------------------------------------------

if __name__ == '__main__':
    main(sys.argv)
