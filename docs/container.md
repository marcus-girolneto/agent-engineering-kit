# Container environment

The optional Dev Container uses digest-pinned Python and uv images, installs Git and certificates, and runs as the `dev` user. It drops Linux capabilities and sets `no-new-privileges`. The host checkout is mounted at `/workspaces/kit`; named volumes keep the Linux virtual environment and uv cache separate from the host.

Open the folder in a client supporting `devcontainer.json` and choose **Reopen in Container**. After the image builds, `postCreateCommand` runs the ordinary setup script. Inside the container, run `uv run --locked kit check`.

No Docker socket, SSH directory, cloud credentials or API keys are mounted by this configuration. Review the client itself for additional credential forwarding. Containers share a kernel with their host environment and are not an absolute boundary for hostile code. Do not mount sensitive host directories to make a task convenient.

The example server remains bound to loopback. No port is automatically published. Use the container terminal to call the API, or configure client port forwarding deliberately for local use.

Build and inspect the image without a Dev Container client:

```bash
docker build -f .devcontainer/Dockerfile -t agent-engineering-kit:dev .
docker run --rm --cap-drop=ALL --security-opt=no-new-privileges \
  agent-engineering-kit:dev sh -c 'id && python --version && uv --version && git --version'
```

Digest pins make the selected images identifiable. The OS package index can change during a rebuild, so this is not a bit-for-bit reproducible operating-system image. Review image and dependency updates regularly.
