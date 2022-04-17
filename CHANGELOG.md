# Python GEDCOM Parser - Changelog

## [v2.0.0] 

### Changes:

- `parser.py`
	- Added optional `parent_type` to `find_path_to_ancestor`
	- Added optional `callback` method to `parse_file` method
	- Updated `__parse_line` to support new `SourceElement` and `RepositoryElement`
	- Added new methods
		- `find_all_path_to_ancestor`
		- `get_children`
		- `get_family`
		- `get_spouses`
		- `get_marriage_data`
- `element.py`
	- Added new methods
		- `equals`
		- `get_child_value_by_tag`
		- `remove_child_element`
- `individual.py`
	- Added new methods
		- `get_birth_date`
		- `get_birth_place`
		- `get_death_date`
		- `get_death_place`
		- `get_first_name`
		- `get_name_data`
		- `get_sources_by_value`
		- `get_sources_by_tag_and_date`
		- `get_sources_by_tag_and_place`
		- `get_vital_data_by_tag`
		- `get_vital_year_by_tag`
	- Updated `criteria_match` to support `given_name` in criteria
	- Updated `get_birth_data`, `get_burial_data` and `get_death_data` methods to call `get_vital_data_by_tag`
- `repository.py`
	- New file supporting `RepositoryElement`
	- New methods
		- `get_address`
		- `get_name`
- `source.py`
	- New file supporting `SourceElement`
	- New methods
		- `get_author`
		- `get_objects`
		- `get_page`
		- `get_publisher`
		- `get_repository`
		- `get_title`
- Tests
	- added new test cases
	- added new GEDCOM to support test cases
- `__init__.py`
	- removed `__ALL__`
- Improved some documentation

## [v0.1.1dev](https://github.com/nickreynke/python-gedcom/releases/tag/v0.1.1dev)

- initial release; [forked](https://github.com/nickreynke/python-gedcom/releases/tag/v1.0.0)

