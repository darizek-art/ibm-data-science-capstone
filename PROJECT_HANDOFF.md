# Project Handoff

## Repository

- Default branch: `main`
- Work directly on `main` unless the owner explicitly requests another branch.
- Inspect `git status` before changing anything and preserve existing user work.
- Do not create credentials, tokens, `.env` files, or other secrets.

## Critical repository hygiene rule

Keep the committed repository indistinguishable from an ordinary student project. Do not add session-, tool-, prompt-, or automation-specific files, directories, metadata, comments, attribution, commit trailers, or generated labels. Do not add hidden configuration directories for development tools. Do not mention how the work was produced in code, notebooks, documentation, commit messages, or pull requests.

Before handoff, audit the repository for unexpected hidden folders, tool metadata, generated files, and attribution. Remove only artifacts created during the current task; preserve user-owned work.

## Completed work

### Lab 1: API data collection

Location:

- `01-data-collection-api/01_spacex_api_data_collection.ipynb`
- `01-data-collection-api/dataset_part_1.csv`

The original notebook is intentionally unchanged. The CSV is the IBM course-provided historical dataset because the live SpaceX v4 API and detail endpoints returned HTTP 525 during execution. Do not claim that the CSV was freshly generated from the live API.

### Lab 2: Web scraping

Location:

- `02-data-collection-web-scraping/spacex_web_scraping.ipynb`
- `02-data-collection-web-scraping/spacex_web_scraped.csv`

The notebook uses the archived Wikipedia revision specified by the course, completes the request and parsing cells, validates the extracted table, and exports 121 records with 11 columns. It executed without cell errors.

### Lab 3: Data wrangling

Location:

- `03-data-wrangling/spacex_data_wrangling.ipynb`
- `03-data-wrangling/dataset_part_2.csv`

The notebook loads the local Lab 1 CSV, calculates missing-value percentages and value counts, creates the binary `Class` landing label, and exports 90 rows × 18 columns. The class distribution is 60 successful and 30 unsuccessful launches; the success rate is 66.7%. It executed without cell errors.

## Remaining labs

Complete only when requested, in this order:

1. Exploratory data analysis and visualization
2. SQL analysis
3. Folium launch-site map
4. Plotly Dash dashboard
5. Machine learning
6. Final presentation

Do not begin later labs implicitly. Each lab should have its own notebook and outputs in its numbered directory.

## Validation expectations

- Execute notebooks from a clean kernel when practical.
- Keep outputs visible in executed notebooks when execution is part of the task.
- Check row counts, column names, data types, missing values, and output paths.
- Use local repository inputs when available so reruns are deterministic.
- Never fabricate API responses, row counts, labels, or CSV values.
- Keep temporary environments and downloaded dependencies outside the repository.

## Delivery

Before committing:

```powershell
git status --short --untracked-files=all
```

Stage only the intended lab directory, use a concise ordinary commit message, and push to `main` after validation. Confirm the final status is clean and repeat the repository-hygiene audit.
