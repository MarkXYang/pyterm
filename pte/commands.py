### Copyright (C) 2002-2006 Eli Yukelzon <reflog@gmail.com>

### This program is free software; you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
### the Free Software Foundation; either version 2 of the License, or
### (at your option) any later version.

### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.

### You should have received a copy of the GNU General Public License
### along with this program; if not, write to the Free Software
### Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


# GTK/Gnome imports
import pygtk
pygtk.require('2.0')
import gtk,pango,vte

import gui

def tab_move_left(main, sender, event):
    pn = main.nb.get_current_page()
    main.nb.reorder_child(main.nb.get_nth_page(pn),pn-1)

def tab_move_right(main, sender, event):
    pn = main.nb.get_current_page()
    if pn+1 == main.nb.get_n_pages():
        main.nb.reorder_child(main.nb.get_nth_page(pn),0)
    else:
        main.nb.reorder_child(main.nb.get_nth_page(pn),pn+1)

def tab_shift_left(main, sender, event):
    pn = main.nb.get_current_page() - 1
    main.nb.set_current_page(pn)

def tab_shift_right(main, sender, event):
    pn = main.nb.get_current_page() + 1
    if pn == main.nb.get_n_pages():
        pn = 0
    main.nb.set_current_page(pn)

def tab_select(n, main, sender, event):
    main.nb.set_current_page(n-1)

def show_settings(main, sender, event):
    main.settings_dlg.read_settings(main.conf)
    r = main.settings_dlg.run(1,main.window)
    main.settings_dlg.hide()
    if r == gtk.RESPONSE_OK:
        main.settings_dlg.write_settings()
        main.update_ui()

we_are_fs = False

def fullscreen(main, sender, event):
    global we_are_fs
    we_are_fs = not we_are_fs
    if we_are_fs:
        main.window.fullscreen()
    else:
        main.window.unfullscreen()

def tab_new(main, sender, event):
    t = main.nb.add_terminal()
    main.nb.set_current_page(t['page_n'])
    main.window.set_focus(t['term'])

def get_action_tab(main, sender):
    pn = -1
    if type(sender) is gtk.Window:
        pn = main.nb.get_current_page()
    else:
        for (i,p) in enumerate(main.nb.get_children()):
            if main.nb.get_tab_label(p) == sender:
                pn = i
    return pn

def get_action_term(main, sender):
    if type(sender) is gtk.Window:
        pn = main.nb.get_current_page()
        for (i,p) in enumerate(main.nb.get_children()):
            if pn == i:
                return p
    else:
        for (i,p) in enumerate(main.nb.get_children()):
            if main.nb.get_tab_label(p) == sender:
                return p
                
    return None


def tab_rename(main, sender, event):
    tabn = get_action_term(main, sender)
    prof = None
    for t in main.terms:
        if t['widget'] == tabn:
            prof = t['profile']
    if prof:
        main.nb.set_tab_label(tabn,gui.create_custom_tab(main.nb, event, prof, main.remove_book))
        t['title'] = event

def tab_close(main, sender, event):
    main.remove_book_by_n( get_action_tab(main, sender) )

def tab_lock(main, sender, event):
    pass

def tab_duplicate(main, sender, event):
    t = main.nb.get_nth_page( get_action_tab(main, sender) )
    for term in main.terms:
        if term['widget'] == t:
            ta = dict ( title=term['title'], profile=term['profile'], widget=None )  
            ta['widget'] = main.new_tab(term['profile'], term['title'])
            main.terms += [ ta ]

def command_by_key(b, key, state):
    for v in b.values():
        (k,s) = gtk.accelerator_parse(v['key'])
        if k == key and ((s == state) or (s|gtk.gdk.MOD2_MASK == state)):
            return v['command']
    

def handle_key_press(main, sender, event):
    cmd = command_by_key(main.conf.bindings, event.keyval, event.state)
    if cmd:
        cmd(main, sender,event)
        return True
    return False
