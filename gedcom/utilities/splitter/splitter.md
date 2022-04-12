## Introduction

The Splitter module extends Parser and creates a new GEDCOM including only specific person, their descendants, their descendant's spouses and the their descendant's spouses' parents.  Many software packages can export descendants and spouses, but do not include in-laws.  Splitter completes the following steps when creating a new GEDCOM.

* Identify specific person that will be the root ancestor
* Collect the IDs of the following people related to the root ancestor:
	* Spouse(s) and their parents
	* Descendants
	* Spouses of descendants and their parents
	* Parents of descendants (should there be no marriage) and their parents
 Remove anyone from the tree who was not identified in the previous step
* Identify and remove any sources that are no longer referenced by remaining people
* Identify and remove any repositories that are no longer referenced by remaining sources
* Identify and remove any objects that are no longer referenced by remaining sources or people

Splitter modifies the tree in the computer's memorial.  This tree must be saved to create a new GEDCOM file.  If the removed information is needed, the tree must be parsed again.

There are three ways to use the Splitter module:

* Use the Splitter app
* Run the module from the command line
* Incorporate it in into new Python program 

## Running Splitter 
### Command Line

```
python splitter.py -i <gedcom-input-file> [-h | -b <year-of-birth> | -d <year-of-death> | -g <given-name> | -l <last-name> | -o <gedcom-output-file> | -n]
```

Options and arguments (and corresponding environment variables):

>  -b : root person's year of birth

>  -d : root person's year of death

>  -g : part of all of the root person's given name

>  -h : print this help message and exit

>  -i : file name of the source GEDCOM file

>  -l : part of all of the root person's last name

>  -n : exclude father-in-law and mother-in-law of descendants

>  -o : file name of output GEDCOM file; if not included, adds "_split" to the input file name

>  -s : does not enforce strict parsing of GEDCOM file

### With the App


### Python Script

#### Example 1

```python
from gedcom.utilities.splitter.splitter import Splitter
from gedcom.element import individual

from gedcom.element.individual import IndividualElement

import gedcom.tags

# Path to your ".ged" file
file_path = ''

# Name of your ".ged" file
file_name = ''

# Name of your new ".ged" file
output_file_name = ''

# Initialize the parser
parser = Splitter()
parser.parse_file(file_path + file_name)

# Use criteria to find person.  Only one field is required.  The search returns the first match.  
criteria = "given_name=[first name]:surname=[last name]:birth=[birth year]:death=[death year]"
ancestor = parser.find_person(criteria)

if ancestor == "":
    print('Person not found')
else:
	parser.split_gedcom(ancestor)
	parser.write_file(output_file_name)

```

## License

Licensed under the [GNU General Public License v2](http://www.gnu.org/licenses/gpl-2.0.html)

**Python GEDCOM Parser**
<br>Copyright (C) 2022 Mark Wing (mark at markwing.net)
<br>Copyright (C) 2018 Damon Brodie (damon.brodie at gmail.com)
<br>Copyright (C) 2018-2019 Nicklas Reincke (contact at reynke.com)
<br>Copyright (C) 2016 Andreas Oberritter
<br>Copyright (C) 2012 Madeleine Price Ball
<br>Copyright (C) 2005 Daniel Zappala (zappala at cs.byu.edu)
<br>Copyright (C) 2005 Brigham Young University

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
