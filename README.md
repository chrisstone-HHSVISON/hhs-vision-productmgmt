# hhs-vision-productmgmt

Product management workspace for HHS VISION.

## Status

Active — Release 1 (Happy Path) is in progress. Currently in **Milestone 3** (Aug 5 – Sep 1, 2026).

## Artifacts

| File | Description |
| ---- | ----------- |
| `roadmap.html` | Interactive Gantt-style feature roadmap. Open in a browser. Loads data dynamically from the hosted Google Sheet export and auto-refreshes every 2 minutes; falls back to embedded snapshot data if live sync is unavailable. Supports expand/collapse of sub-features and per-release filtering. |
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
- Entry page: `index.html` (redirects to `roadmap.html`)

### Enable once in GitHub

1. Open repository **Settings** > **Pages**.
2. Under **Build and deployment**, choose **Source: GitHub Actions**.
3. Push to `main` (or run the workflow manually from **Actions** > **Deploy Roadmap**).
4. Share the Pages URL (typically `https://<org-or-user>.github.io/<repo>/`).

### Important access note

`roadmap.html` live sync reads from the hosted Google Sheet export URL. Team members viewing the roadmap must also have permission to access the source sheet; otherwise the page will use embedded fallback snapshot data.
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
