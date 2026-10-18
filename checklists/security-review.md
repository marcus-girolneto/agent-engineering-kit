# Security review checklist

- What data, credentials and actions are reachable from this entry point?
- Are authentication and per-object authorization appropriate for the actual deployment?
- Is untrusted input kept out of executable SQL, shell syntax and unrestricted paths?
- Are parsers, request sizes, pagination and retries bounded?
- Can logs, prompts, exceptions or artifacts expose sensitive data?
- Are external tools, network destinations and MCP permissions necessary and scoped?
- Are dependencies locked, actions pinned, and known advisories checked?
- Is the secret baseline narrowly reviewed rather than regenerated automatically?
- Are abuse cases tested with synthetic input?
- What important control is manual or outside this repository?
