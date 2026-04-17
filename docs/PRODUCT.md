# Product Notes

## Chosen stack
Python

## Selected idea
`retry-after-utils`: a tiny dependency-free utility package for parsing HTTP `Retry-After` headers and computing safe backoff delays.

## Why this idea won
- Small enough for a strong one-run MVP
- Broad utility for API clients, SDKs, crawlers, and integrations
- Clear publishable scope with minimal maintenance burden

## MVP
- Parse numeric and HTTP-date Retry-After values
- Expose a tiny public API
- Support bounded delay computation with fallback and jitter
- Include tests, README, and CI

## Release checklist
- [x] Pick stack and package idea
- [x] Define MVP
- [x] Define API and architecture
- [x] Implement package
- [x] Add tests
- [x] Write English README
- [x] Add CI workflow
- [x] Verify package builds
- [x] Publish public GitHub repository
- [ ] Publish to PyPI (out of scope for this run)
