include config.mk

BINARY     = chi

CHIOBJ     = chi.pyo
ERROBJ     = error.pyo
LEXOBJ     = lexer.pyo

OBJECTS    = $(CHIOBJ) $(ERROBJ) $(LEXOBJ)

all: $(BINARY)

$(BINARY): $(OBJECTS) runscript
	chmod +x chi.py chi

%.pyo: %.py
	$(COMPILER) $(CFLAGS) -o $@ $<

runscript:
	sed 's+DESTDIRPREFIX+$(DESTDIR)$(PREFIX)+g' chi.run > chi

install: all
	mkdir -p $(DESTDIR)$(PREFIX)/bin/chilang
	cp -f $(OBJECTS) $(BINARY).py $(DESTDIR)$(PREFIX)/bin/chilang
	cp -f $(BINARY) $(DESTDIR)$(PREFIX)/bin/$(BINARY)

uninstall:
	rm -rf $(DESTDIR)$(PREFIX)/bin/chilang
	rm -f  $(DESTDIR)$(PREFIX)/bin/$(BINARY)

dist: clean
	mkdir -p $(BINARY)-$(VERSION)
	cp LICENSE Makefile README.md *.py $(BINARY)-$(VERSION)
	tar -cf $(BINARY)-$(VERSION).tar $(BINARY)-$(VERSION)
	gzip $(BINARY)-$(VERSION).tar
	rm -rf $(BINARY)-$(VERSION)

clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	rm -f $(BINARY)-$(VERSION).tar.gz chi

.PHONY:
	all install uninstall dist clean
