include config.mk

BINARY     = chi

CHIOBJ     = chi.pyo
ERROBJ     = error.pyo
LEXOBJ     = lexer.pyo

OBJECTS    = $(CHIOBJ) $(ERROBJ) $(LEXOBJ)

all: $(BINARY)

$(BINARY): $(OBJECTS)
	chmod +x chi.pyo chi.py

%.pyo: %.py
	$(COMPILER) $(CFLAGS) -o $@ $<

install: all
	mkdir -p $(DESTDIR)$(PREFIX)/bin/chilang/__pycache__
	cp -f $(OBJECTS) $(DESTDIR)$(PREFIX)/bin/chilang/__pycache__
	cp -f $(BINARY).py $(DESTDIR)$(PREFIX)/bin/chilang
	ln -sf $(DESTDIR)$(PREFIX)/bin/chilang/$(BINARY).py $(DESTDIR)$(PREFIX)/bin/$(BINARY)

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
	rm -f $(BINARY)-$(VERSION).tar.gz

.PHONY:
	all install uninstall dist clean
