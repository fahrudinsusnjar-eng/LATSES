# LAT-CES Session Recovery Protocol

This file defines how an engineering session resumes without reconstructing the project from conversation history.

## Start-of-session order

1. Read `.github/LATCES_PROJECT_STATE.json`.
2. Read `.github/LATCES_PROJECT_STATE.md` for human-readable history.
3. Inspect the active PR listed in the JSON.
4. Inspect the latest commit and its Verification + Windows Installer workflow runs.
5. Continue from `current_blocker` and `next_actions`.

## End-of-session order

After every meaningful change, update the checkpoint with:

- active branch;
- active PR;
- latest commit;
- CI run numbers and status;
- completed work;
- current blocker;
- exact next action;
- decisions that must not be reopened.

## Release evidence rule

A LAT-CES Windows build is not release-ready merely because CI imports the GUI or the executable starts. For the master GUI, the validation path must exercise the user-facing command callbacks, including Reference House, Tlocrt, Presjek, 3D, Provjera and Izvještaj.

## Anti-loop rule

Before opening a new bug-fix branch, compare the failure with the historical decisions and closed PRs recorded in the checkpoint. Reuse the active workstream when the problem was already analysed and has a reproducible existing solution.

## Communicator/GitHub integration

The repository itself does not provide ChatGPT with permanent hidden memory. The persistent hand-off is therefore stored in GitHub. A future session can fetch these files through the GitHub connector and use them as the authoritative project navigation point.
