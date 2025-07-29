# PARAMETER (with default values)

# Directory which contains the Makefile
SPHINX_EXEC_DIR         ?= .

# Directory from which the sources will be read
SPHINX_SOURCE_DIR       ?= ./source

# Directory which contains the built files
SPHINX_OUTPUT_DIR       ?= ./output

# Args passed to the sphinx-build command
SPHINXOPTS              ?= -c $(SPHINX_EXEC_DIR)

# Directory which will hold auto-generated files
SPHINX_GENERATED_DIR    = $(SPHINX_OUTPUT_DIR)/../generated

# Directory which contains extracted requirement files
SPHINX_REQUIREMENTS_DIR = $(SPHINX_EXEC_DIR)/requirements

ASSETS_IMG = $(SPHINX_SOURCE_DIR)/assets/img/

.PHONY: help install copy-images apidoc clean html generate Makefile up

# Copy images before running any Sphinx command (except help)
copy-images:
	@echo "Copying images from $(ASSETS_IMG) to ./assets/img/..."
	cp -vr $(ASSETS_IMG)* ./assets/img/

# Installation routine for the package manager (do not run inside container)
install: clean
	cp -vr --no-dereference $(shell pkgmgr path infinito)/* ./source/

# Generate reStructuredText files from Python modules with sphinx-apidoc
generate-apidoc:
	@echo "Running sphinx-apidoc..."
	sphinx-apidoc -f -o $(SPHINX_GENERATED_DIR)/modules $(SPHINX_SOURCE_DIR)

# Generate the YAML index
generate-yaml-index:
	@echo "Generating YAML index..."
	python generators/yaml_index.py --source-dir $(SPHINX_SOURCE_DIR) --output-file $(SPHINX_GENERATED_DIR)/yaml_index.rst

# Generate Ansible roles documentation
generate-ansible-roles:
	@echo "Generating Ansible roles documentation..."
	python generators/ansible_roles.py --roles-dir $(SPHINX_SOURCE_DIR)/roles --output-dir $(SPHINX_GENERATED_DIR)/roles
	@echo "Generating Ansible roles index..."
	python generators/index.py --roles-dir generated/roles --output-file $(SPHINX_SOURCE_DIR)/roles/ansible_role_glosar.rst --caption "Ansible Role Glossary"

# Create required README.md files for the index
generate-readmes:
	@echo "Creating required README.md files for index..."
	python generators/readmes.py --generated-dir $(SPHINX_GENERATED_DIR)

# Run all generation steps
generate: generate-apidoc generate-yaml-index generate-ansible-roles generate-readmes

# Remove generated files
clean:
	@echo "Removing generated files..."
	- git clean -fdX

# Show help for all Makefile targets
help:
	- sphinx-build -M help "$(SPHINX_SOURCE_DIR)" "$(SPHINX_OUTPUT_DIR)" $(SPHINXOPTS) $(O)

# Build the HTML documentation (includes copying images and generation)
html: copy-images generate
	@echo "Building Sphinx documentation..."
	- sphinx-build -M html "$(SPHINX_SOURCE_DIR)" "$(SPHINX_OUTPUT_DIR)" $(SPHINXOPTS)

# Build just HTML, without prior generation or copying
just-html:
	- sphinx-build -M html "$(SPHINX_SOURCE_DIR)" "$(SPHINX_OUTPUT_DIR)" $(SPHINXOPTS)

# Start (or restart) the Docker container with a fresh build
up: install
	- docker compose up -d --force-recreate --build

# Catch-all: forward any unspecified targets to Sphinx
%: Makefile
	- sphinx-build -M $@ "$(SPHINX_SOURCE_DIR)" "$(SPHINX_OUTPUT_DIR)" $(SPHINXOPTS) $(O)
