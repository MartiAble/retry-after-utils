# Acceptance Notes

## Repository structure verified
- `pyproject.toml`
- `README.md`
- `LICENSE`
- `src/retry_after_utils/`
- `tests/`
- `.github/workflows/ci.yml`
- `docs/`

## Verification performed
- Editable install in a clean venv
- `pytest` => passing
- `python -m build` => sdist and wheel built successfully

## Limitations
- Constant jitter only; no randomized backoff helpers
- No built-in integration with `requests`, `httpx`, or asyncio clients
- No PyPI publish step in this run

## Unverified runtime assumptions
- GitHub Actions workflow execution was not validated post-push inside GitHub UI
- Package install was validated on local host Python only; CI matrix is prepared but not observed running yet
- Downstream consumers may expect more permissive date parsing than Python stdlib provides
