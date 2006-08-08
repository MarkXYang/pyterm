
.SUFFIXES :

# default install directories
include INSTALL

#
VERSION := $(shell grep "^version" pyterm | cut -d \"  -f 2)
RELEASE := pyterm-$(VERSION)
BROWSER := firefox
SPECIALS := pyterm paths.py
.PHONY:all
all: $(addsuffix .install,$(SPECIALS)) pyterm.desktop
	@$(MAKE) -C locale
	@$(MAKE) -C help

.PHONY:clean
clean: 
	@echo 'Cleaning up...'
	@-rm -f *.pyc *.install *.bak glade2/*.bak  pyterm.desktop
	@$(MAKE) -C locale clean
	@$(MAKE) -C help clean

.PHONY:install
install: $(addsuffix .install,$(SPECIALS)) pyterm.desktop
	@echo 'Preparing directories'
	@mkdir -m 755 -p \
		$(DESTDIR)$(bindir) \
		$(DESTDIR)$(libdir_) \
		$(DESTDIR)$(libdir_)/pte \
		$(DESTDIR)$(sharedir_)/glade \
		$(DESTDIR)$(docdir_) \
		$(DESTDIR)$(sharedir)/applications \
		$(DESTDIR)$(sharedir)/application-registry \
		$(DESTDIR)$(sharedir)/pixmaps \
		$(DESTDIR)$(helpdir_)
	@echo "Copying files"
	@install -m 755 pyterm.install \
		$(DESTDIR)$(bindir)/pyterm
	@install -m 644 *.py \
		$(DESTDIR)$(libdir_)
	@install -m 644 pte/*.py \
		$(DESTDIR)$(libdir_)/pte
	@install -m 644 paths.py.install \
		$(DESTDIR)$(libdir_)/paths.py
	@install -m 644 pyterm.applications \
		$(DESTDIR)$(sharedir)/application-registry/pyterm.applications
	@install -m 644 pyterm.desktop \
		$(DESTDIR)$(sharedir)/applications
	@echo 'Precompiling PY files'
	@$(PYTHON) -c 'import compileall; compileall.compile_dir("$(DESTDIR)$(libdir_)")'
	@$(PYTHON) -O -c 'import compileall; compileall.compile_dir("$(DESTDIR)$(libdir_)")'
	@-install -m 644 \
		glade/*.glade \
		$(DESTDIR)$(sharedir_)/glade
	@-install -m 644 \
		glade/pixmaps/*.xpm \
		glade/pixmaps/*.png \
		$(DESTDIR)$(sharedir_)/glade/pixmaps
	@-install -m 644 glade/pixmaps/icon.png \
		$(DESTDIR)$(sharedir)/pixmaps/pyterm.png
	@$(MAKE) -C locale install
	@$(MAKE) -C help install

pyterm.desktop: pyterm.desktop.in
	@intltool-merge -d locale pyterm.desktop.in pyterm.desktop

%.install: %
	@echo 'Patching paths in $<'
	@$(PYTHON) tools/install_paths \
		libdir=$(libdir_) \
		localedir=$(localedir) \
		helpdir=$(helpdir_) \
		sharedir=$(sharedir_) \
		< $< > $@

.PHONY:uninstall
uninstall:
	@-rm -rf \
		$(sharedir_) \
		$(docdir_) \
		$(helpdir_) \
		$(libdir_) \
		$(bindir)/pyterm \
		$(sharedir)/applications/pyterm.desktop \
		$(sharedir)/pixmaps/pyterm.png
	@$(MAKE) -C locale uninstall
	@$(MAKE) -C help uninstall

.PHONY:changelog
changelog:
	@tools/buildcl.sh > changelog
.PHONY:check
check:
	@tools/check_release

.PHONY:release
release: check changelog upload announce

upload:
	cvs tag release-$(subst .,_,$(VERSION))
	scp tools/make_release stevek@master.gnome.org:
	ssh stevek@master.gnome.org python make_release $(VERSION)

.PHONY:announce
announce:
	$(BROWSER) http://freshmeat.net/add-release/29735/ &
	$(BROWSER) http://www.gnomefiles.org/devs/newversion.php?soft_id=203 &
	$(BROWSER) http://www.gnome.org/project/admin/newrelease.php?group_id=506 &
	$(BROWSER) http://sourceforge.net/project/admin/editpackages.php?group_id=53725 &
	
.PHONY:backup
backup:
	tar cvfz ~/archive/pyterm-`date -I`.tgz --exclude='*.pyc' --exclude='*.bak' --exclude='*.swp' .
	@echo Created ~/archive/pyterm-`date -I`.tgz
