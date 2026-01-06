# Infinito.Nexus Sphinx
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-blue?logo=github)](https://github.com/sponsors/kevinveenbirkenbach) [![Patreon](https://img.shields.io/badge/Support-Patreon-orange?logo=patreon)](https://www.patreon.com/c/kevinveenbirkenbach) [![Buy Me a Coffee](https://img.shields.io/badge/Buy%20me%20a%20Coffee-Funding-yellow?logo=buymeacoffee)](https://buymeacoffee.com/kevinveenbirkenbach) [![PayPal](https://img.shields.io/badge/Donate-PayPal-blue?logo=paypal)](https://s.veen.world/paypaldonate)


[Infinito.Nexus](https://infinito.nexus/) uses [Sphinx](https://www.sphinx-doc.org/) to automatically generate its documentation and leverages the [Awesome Sphinx Theme](https://sphinxawesome.xyz/) for a sleek and responsive design. Enjoy a seamless, visually engaging experience 🚀✨.  
You can access the generated documentation [here](https://docs.infinito.nexus/) 🔗. Browse the latest updates and guides to get started.

---

## About This Tool

This documentation project is developed by [Kevin Veen-Birkenbach](https://www.veen.world/) and is a part of the Infinito.Nexus ecosystem. It is created to provide clear, maintainable, and interactive documentation for the project. The tool is licensed under the [MIT License](https://opensource.org/licenses/MIT) and welcomes community contributions!

---

## Docker Image

The container image is published on **GitHub Container Registry (GHCR)**:

```bash
docker pull ghcr.io/kevinveenbirkenbach/infinito-sphinx:latest
```

What the image does:

1. Uses the `infinito` base image
2. Installs required build tools (e.g. `pandoc`)
3. Runs `make setup` inside the Infinito source tree
4. Builds the Sphinx HTML documentation
5. Serves the generated docs via `http.server`

---

## Running the Documentation Server

### Using `docker run`

```bash
docker run --rm -p 127.0.0.1:80:8000 \
  ghcr.io/kevinveenbirkenbach/infinito-sphinx:latest
```

Then open:

```
http://127.0.0.1/
```

---

### Using `docker-compose`

```yaml
services:
  infinito_docs:
    image: ghcr.io/kevinveenbirkenbach/infinito-sphinx:latest
    container_name: infinito_docs
    ports:
      - "127.0.0.1:80:8000"
```

Start the service:

```bash
docker compose up -d
```

---

## Commands

To view all the available commands and options for starting and configuring the **Infinito.Nexus Sphinx** tool, simply run the following command:

```bash
infinito-sphinx --help
```

This command provides an easy way to access all the options needed to work with **Infinito.Nexus Sphinx** and manage the project’s documentation. Whether you're setting up the environment or generating documentation, the `--help` command will guide you through all available functionalities. 🚀

## Contributing

Contributions are welcome! If you have any suggestions or encounter issues, feel free to open an issue or submit a pull request on [GitHub](https://github.com/kevinveenbirkenbach/infinito-nexus-sphinx).
