# Docker Compose service + container naming
# Service name must match docker-compose.yml
DOCS_SERVICE_NAME ?= infinito_docs

# Optional explicit container_name (used by compose via env var if you set it)
DOCS_CONTAINER_NAME ?= infinito_docs

# PARAMETER (with default values)

# Directory which contains the Makefile
SPHINX_EXEC_DIR         ?= .

# Directory which contains the built files
SPHINX_OUTPUT_DIR       ?= ./output

# Sphinx conf.py location after refactor
SPHINX_CONF_DIR         ?= $(SPHINX_EXEC_DIR)/src/infinito_docs

# Args passed to sphinx-build
SPHINXOPTS              ?= -c $(SPHINX_CONF_DIR)

# Directory which will hold auto-generated files
SPHINX_GENERATED_DIR    = $(SPHINX_OUTPUT_DIR)/../generated

# Directory which contains extracted requirement files
SPHINX_REQUIREMENTS_DIR = $(SPHINX_EXEC_DIR)/requirements

# If not provided externally, default to the known infinito container path
INFINITO_SRC_DIR        ?= /opt/src/infinito

# Sphinx static assets live in the package (conf.py uses src/infinito_docs/assets)
SPHINX_ASSETS_DIR        = $(SPHINX_CONF_DIR)/assets
ASSETS_SRC               = $(INFINITO_SRC_DIR)/assets/img/
ASSETS_DST               = $(SPHINX_ASSETS_DIR)/img/

.PHONY: \
	help \
	copy-images \
	generate-apidoc \
	generate-yaml-index \
	generate-ansible-roles \
	generate-roles-index \
	generate-readmes \
	generate \
	clean \
	html \
	just-html \
	up \
	test test-unit \
	build-no-cache

# Copy images into the documented source tree so that Sphinx can resolve them.
copy-images:
	@echo "Copying images from $(ASSETS_SRC) to $(ASSETS_DST)..."
	mkdir -p "$(ASSETS_DST)"
	cp -vr "$(ASSETS_SRC)." "$(ASSETS_DST)" || true

# Generate reStructuredText files from Python modules with sphinx-apidoc
generate-apidoc:
	@echo "Running sphinx-apidoc..."
	sphinx-apidoc -f -o "$(SPHINX_GENERATED_DIR)/modules" "$(INFINITO_SRC_DIR)"

# Generate the YAML index (via installed package CLI)
generate-yaml-index:
	@echo "Generating YAML index..."
	infinito-docs-generate-yaml-index \
		--source-dir "$(INFINITO_SRC_DIR)" \
		--output-file "$(SPHINX_GENERATED_DIR)/yaml_index.rst"

# Generate Ansible roles documentation (via installed package CLI)
generate-ansible-roles:
	@echo "Generating Ansible roles documentation..."
	infinito-docs-generate-ansible-roles \
		--roles-dir "$(INFINITO_SRC_DIR)/roles" \
		--output-dir "$(SPHINX_GENERATED_DIR)/roles"

# Generate Ansible roles index (via installed package CLI)
generate-roles-index:
	@echo "Generating Ansible roles index..."
	infinito-docs-generate-roles-index \
		--roles-dir "$(SPHINX_GENERATED_DIR)/roles" \
		--output-file "$(INFINITO_SRC_DIR)/roles/ansible_role_glosar.rst" \
		--caption "Ansible Role Glossary"

# Create required README.md files for the index (via installed package CLI)
generate-readmes:
	@echo "Creating required README.md files for index..."
	infinito-docs-generate-readmes \
		--generated-dir "$(SPHINX_GENERATED_DIR)"

# Run all generation steps
generate: generate-apidoc generate-yaml-index generate-ansible-roles generate-roles-index generate-readmes

# Show help for all Makefile targets
help:
	- sphinx-build -M help "$(INFINITO_SRC_DIR)" "$(SPHINX_OUTPUT_DIR)" $(SPHINXOPTS) $(O)

# Build the HTML documentation (includes copying images and generation)
html: copy-images generate
	@echo "Building Sphinx documentation..."
	- sphinx-build -M html "$(INFINITO_SRC_DIR)" "$(SPHINX_OUTPUT_DIR)" $(SPHINXOPTS)

# Build just HTML, without prior generation or copying
just-html:
	- sphinx-build -M html "$(INFINITO_SRC_DIR)" "$(SPHINX_OUTPUT_DIR)" $(SPHINXOPTS)

# Start (or restart) the Docker container.
# This will only build if the image is missing/outdated (default compose behavior).
up:
	- DOCS_CONTAINER_NAME="$(DOCS_CONTAINER_NAME)" docker compose up -d --force-recreate --build "$(DOCS_SERVICE_NAME)"

# Explicit: rebuild image with no-cache (does NOT automatically run)
build-no-cache:
	- DOCS_CONTAINER_NAME="$(DOCS_CONTAINER_NAME)" docker compose build --no-cache "$(DOCS_SERVICE_NAME)"

# Unit tests inside container.
# Uses "up" so it only builds when needed.
test test-unit: up
	@echo "Running unit tests inside container (infinito-sphinx repo)..."
	docker compose exec -T "$(DOCS_SERVICE_NAME)" \
		bash -lc ' \
			cd "$${SPHINX_EXEC_DIR}" && \
			PYTHONPATH=src \
			python -m unittest discover \
				-s tests/unit \
				-t . \
				-p "test_*.py" \
				-v \
		'

