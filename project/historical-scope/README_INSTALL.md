# Survival Guide | Gate A handoff package

These are the actual files originally created in ChatGPT. They have not been present in the user's `/home/jd/Survival_Guide` Linux directory until copied there.

## Destination

`/home/jd/Survival_Guide/handoff/`

## Install (after downloading ZIP to ~/Downloads)

```bash
mkdir -p /home/jd/Survival_Guide
cd /home/jd/Survival_Guide
unzip -n "$HOME/Downloads/Survival_Guide_Gate_A_Package.zip"
ls -lah handoff/
(cd handoff && sha256sum -c SHA256SUMS.txt)
```

`unzip -n` prevents overwriting pre-existing files. If the browser saves ZIP elsewhere, substitute the downloaded ZIP's absolute path.

## Files
- `SURVIVAL_FIELD_ENCYCLOPEDIA_ASTRA_CLI_HANDOFF.md` — production contract, schemas, 16 zones, safety rules, gates, output requirements.
- `Survival_Field_Encyclopedia_Master_Sprint_Plan_v1.md` — 16 sprints, milestones and acceptance criteria.
- `Survival_Field_Encyclopedia_Sprint_Tracker_v1.xlsx` — corresponding editable Excel tracker.
- `SHA256SUMS.txt` — integrity check for all three.

## Project state
The latest CLI audit found only `/home/jd/Survival_Guide/BASELINE_AUDIT_20261116.md`, with no Git repository and no other implementation. This package does not change that audit. **Do not assume the source-tracked encyclopedia or a completed Gate A already exists.**

## Decision authorization
User previously requested project implementation. For this isolated new project, CLI may initialize a fresh Git repository in `/home/jd/Survival_Guide` **only after** it rechecks that the project path is not already inside a Git worktree. Do not initialize or modify any DCTS/Nova/other project; do not add a remote or push. Keep existing audit unchanged. Proceed with Gate A scaffolding only, per handoff.
