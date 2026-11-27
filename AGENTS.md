# AGENTS.md

## Project Overview

`openvpn-status-reader` parses OpenVPN status-version-1 logs into Python data
structures.

Core code lives in `openvpn_status/`:

- `parser.py`, `models.py`, and `descriptors.py` implement the status parser.
- `utils.py` contains conversion helpers for timestamps, addresses, and sizes.
- Tests live in `tests/`.
- Documentation sources live in `docs/`; `docs/_build/` contains generated
  output.

## Source of Truth

- Use `README.rst` and `docs/` for installation, package usage, and baseline
  test commands.
- Use `.github/workflows/ci.yml` for CI-tested dependencies, QA/test commands,
  environment variables, and supported Python versions.
- Use GitHub issue and pull request templates when asked to open issues or PRs.

If instructions conflict, repository configuration and CI workflows win first,
documentation next, and this file is supplemental.

## Contributing Guidelines

- Before editing, inspect the relevant implementation, tests, documentation,
  and configuration. Follow existing repository patterns and do not invent
  behavior or requirements.
- Keep each contribution focused and change only the lines necessary for its
  goal. Do not include unrelated refactors, formatting churn, or generated and
  dependency-file changes unless explicitly required.
- Preserve the `openvpn_status` import API, parser output, and supported input
  formats unless explicitly required.
- Add or update tests for every behavior change. For bug fixes, write the
  regression test first and confirm it fails before implementing the fix.
- Run `openwisp-qa-format` after each change when available.
- Run the relevant targeted tests, builds, and documented QA checks, including
  `./run-qa-checks` when provided. Do not claim a change is complete when
  verification fails; report the failure or blocker.
- When requirements, intended behavior, or an unexpected failure are unclear,
  stop and seek clarification instead of making speculative changes.
- When starting work on a new issue, create a branch from `master`. Use
  `issues/<issue-number>-<short-title>` for issue work. Otherwise, use a short,
  descriptive branch name.
- Commit messages must be descriptive and use past tense. For issue work, use
  an allowed prefix and a capitalized, past-tense subject ending with
  `#<issue-number>`. Repeat the issue reference in the body with `Fixes`,
  `Closes`, `Resolves`, or `Related to` as appropriate.
- Send new commits in response to review feedback instead of amending existing
  commits.

## Development Rules

- Follow the DRY principle. Do not duplicate information or code across files.
- Preserve support for both legacy and current OpenVPN status-version-1
  timestamps.
- Preserve public APIs, parser outputs, error behavior, and supported input
  formats unless explicitly required.
- Edit documentation sources and regenerate `docs/_build/` instead of editing
  generated documentation directly.
- Process large logs and parser input incrementally or in bounded batches when
  the operation permits it. Avoid unnecessary full-size intermediate
  collections.
- Place imports at the top of the file. Defer imports only when necessary.
- Avoid unnecessary blank lines inside functions and methods.
- Prefer short, precise names that rely on their nearest meaningful scope.
- Add comments and docstrings only when they explain non-obvious constraints,
  compatibility, security, side effects, or unavoidable complexity. Place
  comments before the relevant code block.
- Update documentation when behavior, settings, public APIs, setup steps, or
  supported versions change.
- Add CI dependencies to `./install-ci-deps.sh` and cache them. Keep cache
  inputs in sync with the installer and dependency files. Follow the shared
  structure and internal naming in `.github/workflows/ci.yml` so OpenWISP
  automation works across repositories.

## Testing and QA

- Use targeted tests while iterating, then run the documented full test command
  before considering the change complete.
- Prefer in-process tests so coverage tools can measure changed code.
- Keep helpers used by only one test method inside that method. Promote them to
  class or module scope only when genuinely reused.
- Keep tests quiet on success. Capture and assert code-under-test output rather
  than leaving it unasserted.
- Use `./runtests` as the test entry point in CI, documentation, and local
  work. Pass a test path to run a focused test. Enforce an explicit allowlist
  of reviewed, safe flags and reject all others: test runner options can execute
  code outside the selected tests.

## Security Rules

- Treat status logs as untrusted input. Watch for malformed parser input, unsafe
  file paths, excessive parsing costs, and secrets in fixtures or logs.
- Preserve validation around malformed records, addresses, dates, numeric
  values, and parser errors.
- Do not log status-file contents, which can contain client addresses and
  certificate common names.

## Troubleshooting

- If documentation and CI commands differ, use CI for verification and report
  the exact documentation path, CI workflow path, and differing commands. Do
  not change documentation until the user explicitly chooses whether to update
  it in the current change or leave it for a follow-up.
