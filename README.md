# hhs-vision-productmgmt

Product management workspace for HHS VISION.

## Status

Active — Release 1 (Happy Path) is in progress. Currently in **Milestone 3** (Aug 5 – Sep 1, 2026).

## Artifacts

| File | Description |
| ---- | ----------- |
| `roadmap.html` | Interactive Gantt-style feature roadmap. Open in a browser. Uses repository snapshot data that is automatically refreshed by GitHub Actions, so all viewers see updates after each sync/deploy. Supports expand/collapse of sub-features and per-release + milestone filtering. |
| `Source/roadmap-data.csv` | Source data snapshot exported from the Google Sheet (`VISION Feature Inventory`, Roadmap view). This replaces `Source/Roadmap data.pdf` as the roadmap data source moving forward. |

## Releases

| Release | Name | Scope | Milestones |
| ------- | ---- | ----- | ---------- |
| 1 | Dec 14 | Happy Path | M1 – M6 (Jun 10 – Nov 24, 2026) |
| 2 | 2027 Go-Live | MVP | TBD |

## Related

- `../hhs-vision-intake` — requirements intake pipeline (MDDs, BRDs, epics, stories)

## Team Access

To make the roadmap available to the project team via URL, this repo now includes a GitHub Pages workflow:

- Workflow file: `.github/workflows/deploy-roadmap.yml`
- Sync workflow: `.github/workflows/sync-roadmap-data.yml`
- Entry page: `index.html` (redirects to `roadmap.html`)

### Enable once in GitHub

1. Open repository **Settings** > **Pages**.
2. Under **Build and deployment**, choose **Source: GitHub Actions**.
3. Push to `main` (or run the workflow manually from **Actions** > **Deploy Roadmap**).
4. Share the Pages URL: `https://chrisstone-hhsvision.github.io/hhs-vision-productmgmt/`.

If this URL returns a temporary 404 right after an account rename, run **Deploy Roadmap** once from **Actions** and wait a few minutes for GitHub Pages host mapping to propagate.

### Live updates for all viewers

Roadmap data sync now runs server-side in GitHub Actions and commits updated snapshot data to this repo. Pages then serves that updated snapshot to every viewer.

Default sync cadence:

- Every 30 minutes
- Manual run available in **Actions** > **Sync Roadmap Data**

### Data source configuration

The sync workflow supports two modes:

1. `GOOGLE_SERVICE_ACCOUNT_JSON` secret (recommended for private sheet access)
: Share the source sheet with the service account email in this JSON credential.
2. `ROADMAP_CSV_URL` repository variable
: Use a public/exportable CSV URL if available.

Optional repository variables:

- `GOOGLE_SHEET_ID` (default already set in workflow)
- `GOOGLE_WORKSHEET_GID` (default `0`)
- `ROADMAP_CSV_URL`

### Source Sheet Access (Google Drive Sign-In)

Viewer access to the private source sheet uses normal Google authorization, not custom OAuth setup in the roadmap app.

1. Click **Open Source Sheet** in the Live Sync controls.
2. If prompted, sign in through the standard Google/Drive sign-in flow.
3. If access is denied, request sheet access from the sheet owner.

The roadmap itself remains available via GitHub Pages using repository snapshot data that is refreshed by GitHub Actions.

| Milestone | Start Date                    | End Date                    | Duration          |
| --------- | ----------------------------- | --------------------------- | ----------------- |
| **1**     | Wednesday, June 10, 2026      | Tuesday, July 7, 2026       | 4 weeks / 28 days |
| **2**     | Wednesday, July 8, 2026       | Tuesday, August 4, 2026     | 4 weeks / 28 days |
| **3**     | **Wednesday, August 5, 2026** | Tuesday, September 1, 2026  | 4 weeks / 28 days |
| **4**     | Wednesday, September 2, 2026  | Tuesday, September 29, 2026 | 4 weeks / 28 days |
| **5**     | Wednesday, September 30, 2026 | Tuesday, October 27, 2026   | 4 weeks / 28 days |
| **6**     | Wednesday, October 28, 2026   | Tuesday, November 24, 2026  | 4 weeks / 28 days |
| **7**     | Wednesday, November 25, 2026  | Tuesday, December 22, 2026  | 4 weeks / 28 days |
| **8**     | Wednesday, December 23, 2026  | Tuesday, January 19, 2027   | 4 weeks / 28 days |
