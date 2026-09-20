## [1.0.1]

- Fixed processing of valid CSVs with quoted headers so rows are no longer skipped due to header mismatches.
- Expanded description-column handling to support lowercase and numbered headers such as `description`, `description1`, and `reasonDescription2`.
- Fixed invalid output file path when `obscure_schema = False`.
- Fixed the `p_dup_char` mutation path so duplicate-character typos are applied instead of calling the transpose logic twice.
- Added a root `VERSION` file and Bitbucket pipeline validation so release tags must match the declared repo version.
- Fixed stale test/docs issues and closed CSV file handles cleanly during processing and tests.

## [1.0.0]

- Initial release: schema-driven CSV transformation and obfuscation.
- Includes CLI (`main.py`), core modules (`confuser/*.py`), and tests.
