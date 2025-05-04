LOCALBIN = $(HOME)/.local/bin
CURDIR = $(PWD)
PYSCRIPT = tfc.py
BIN = tfc

.PHONY: install linkinst uninstall

$(LOCALBIN):
	@mkdir -p $@

install:
	@chmod +x $(CURDIR)/$(PYSCRIPT)
	@cp $(CURDIR)/$(PYSCRIPT) $(LOCALBIN)/$(BIN)
	@echo Installation done! You can now invoke $(BIN)

linkinst:
	@chmod +x $(CURDIR)/$(PYSCRIPT)
	@ln -s $(CURDIR)/$(PYSCRIPT) $(LOCALBIN)/$(BIN)
	@echo Installation done! You can now invoke $(BIN)

uninstall:
	@rm -f $(LOCALBIN)/$(BIN)
	@echo Desintallation done!
