# GTK/Gnome imports
import pygtk
pygtk.require('2.0')
import gtk,pango,vte,gconf


import settings as conf    

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
    print 'hey hey'

we_are_fs = False

def fullscreen(main, sender, event):
    global we_are_fs
    we_are_fs = not we_are_fs
    if we_are_fs:
        main.window.fullscreen()
    else:
        main.window.unfullscreen()

def tab_new(main, sender, event):
    w = main.new_tab()
    pn = main.nb.page_num(w)
    main.nb.set_current_page(pn)
    main.window.set_focus(w)

def __get_action_tab(main, sender):
    pn = -1
    if type(sender) is gtk.Window:
        pn = main.nb.get_current_page()
    else:
        for (i,p) in enumerate(main.nb.get_children()):
            if main.nb.get_tab_label(p) == sender:
                pn = i
    return pn

def tab_close(main, sender, event):
    main.remove_book_by_n( __get_action_tab(main, sender) )

def tab_lock(main, sender, event):
    pass

def tab_duplicate(main, sender, event):
    t = main.nb.get_nth_page( __get_action_tab(main, sender) )
    for term in main.terms:
        if term['widget'] == t:
            ta = dict ( title=term['title'], profile=term['profile'], widget=None )  
            ta['widget'] = main.new_tab(term['profile'], term['title'])
            main.terms += [ ta ]

def command_by_key(b, key, state):
    for v in b.values():
        (k,s) = gtk.accelerator_parse(v['key'])
        if k == key and s == state:
            return v['command']
    

def handle_key_press(main, sender, event):
    cmd = command_by_key(conf.read_bindings(), event.keyval, event.state)
    if cmd:
        cmd(main, sender,event)
        return True
    return False
