# ADR 0001: Keep instructions separate from executable checks

Status: accepted

A coding assistant needs enough context to navigate a project, but a long automatic prompt is easy to ignore and expensive to maintain. Prose also cannot establish whether tests ran or whether a vulnerability exists.

Keep the root instruction file small. Put task-specific procedures in on-demand documents. Put repeatable checks in a versioned command catalog and run that catalog in CI. Use schemas to validate structured deliverables, while explicitly leaving semantic review to humans and behavioral evidence.

Use uv with one workspace lockfile and an exact uv version. Ship one real Python example rather than nominal support for many stacks. Avoid a framework-specific agent runtime and global client settings so adoption does not silently expand permissions.

Consequences: other stacks need a deliberate task-catalog replacement; users still configure client permissions and GitHub rules. The kit can verify its own mechanics without API credentials, but cannot claim improved agent accuracy without separately measuring agent runs.
