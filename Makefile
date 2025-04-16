# Directory and environment definitions
VENV_DIR := venv
PYTHON := python3

# Colors for messages
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

# Help
help:
	@echo "${BLUE}Available commands:${NC}"
	@echo "  ${GREEN}make setup${NC}           - Set up virtual environment and install all dependencies"
	@echo "  ${GREEN}make venv${NC}            - Create only the virtual environment without installing dependencies"
	@echo "  ${GREEN}make run${NC}             - Run program"
	@echo "  ${GREEN}make test${NC}            - Run all tests"
	@echo "  ${GREEN}make test-verbose${NC}    - Run all tests in verbose mode"

# Complete setup: virtual environment + dependencies
setup: venv
	@echo "${BLUE}Installing dependencies...${NC}"
	@for dir in $(APP_DIRS); do \
		echo "${YELLOW}Installing dependencies from $${dir}...${NC}"; \
		$(VENV_DIR)/bin/pip install -r $${dir}/requirements.txt; \
	done
	@echo "${GREEN}Environment successfully configured!${NC}"

# Create virtual environment if it doesn't exist
venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "${BLUE}Creating virtual environment...${NC}"; \
		$(PYTHON) -m venv $(VENV_DIR); \
		$(VENV_DIR)/bin/pip install --upgrade pip; \
		echo "${GREEN}Virtual environment created in $(VENV_DIR)${NC}"; \
	else \
		echo "${YELLOW}Virtual environment already exists${NC}"; \
	fi

run: test
	@echo "${BLUE}Starting program...${NC}"
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "${YELLOW}Virtual environment not found. Run 'make setup' first${NC}"; \
		exit 1; \
	fi
	$(VENV_DIR)/bin/python src/main.py

test:
	$(VENV_DIR)/bin/python -m unittest discover -s tests

test-verbose:
	$(VENV_DIR)/bin/python -m unittest discover -s tests -v