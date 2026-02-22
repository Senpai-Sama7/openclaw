# PART-DOD.md — Definition of Done (per part)

Every part-completion PR must include the following in its description.

## Required Checklist

- [ ] **Commands run**: list exact commands executed
- [ ] **Key output evidence**: paste or screenshot proving success (verification procedure output)
- [ ] **Risks / rollback note**: what could go wrong, how to undo
- [ ] **BUILD-STATUS.md updated**: ⬜ → ✅ with notes
- [ ] **Build log entry appended**: timestamped entry in `workspace/memory/build-log-YYYY-MM-DD.md`
- [ ] **Verification procedure passed**: ran the check from AGENTS.md for this part

## PR Description Template

```markdown
## Part N — [Title]

### Commands Run
- `command 1`
- `command 2`

### Evidence
<paste verification output>

### Risks & Rollback
- Risk: ...
- Rollback: ...

### Status Updates
- [x] BUILD-STATUS.md updated
- [x] Build log entry appended
- [x] Verification passed
```
