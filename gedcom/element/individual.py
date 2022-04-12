# -*- coding: utf-8 -*-

# Python GEDCOM Parser
#
# Copyright (C) 2022 Mark Wing (mark @ markwing.net)
# Copyright (C) 2018 Damon Brodie (damon.brodie at gmail.com)
# Copyright (C) 2018-2019 Nicklas Reincke (contact at reynke.com)
# Copyright (C) 2016 Andreas Oberritter
# Copyright (C) 2012 Madeleine Price Ball
# Copyright (C) 2005 Daniel Zappala (zappala at cs.byu.edu)
# Copyright (C) 2005 Brigham Young University
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Further information about the license: http://www.gnu.org/licenses/gpl-2.0.html

"""GEDCOM element consisting of tag `gedcom.tags.GEDCOM_TAG_INDIVIDUAL`"""

import re as regex
from gedcom.element.element import Element
from gedcom.helpers import deprecated
import gedcom.tags


class NotAnActualIndividualError(Exception):
    pass


class IndividualElement(Element):

    def get_tag(self):
        """Returns the tag of this element from within the GEDCOM file
        
        :rtype: str
        """
        return gedcom.tags.GEDCOM_TAG_INDIVIDUAL

    def is_deceased(self):
        """Checks if this individual is deceased
        
        :rtype: bool
        """
        for child in self.get_child_elements():
            if child.get_tag() == gedcom.tags.GEDCOM_TAG_DEATH:
                return True

        return False

    def is_child(self):
        """Checks if this element is a child of a family
        
        :rtype: bool
        """
        found_child = False

        for child in self.get_child_elements():
            if child.get_tag() == gedcom.tags.GEDCOM_TAG_FAMILY_CHILD:
                found_child = True

        return found_child

    def is_private(self):
        """Checks if this individual is marked private
        
        :rtype: bool
        """
        for child in self.get_child_elements():
            if child.get_tag() == gedcom.tags.GEDCOM_TAG_PRIVATE:
                private = child.get_value()
                if private == 'Y':
                    return True

        return False

    def get_name(self):
        """Returns an individual's names as a tuple: (`str` given_name, `str` surname)
        
        :rtype: tuple
        """
        name_data = self.get_name_data()
        
        return name_data[0], name_data[1]

    def get_name_data(self):
        """Returns an individual's name data including sources as a tuple: (`str` given_name, `str` surname, `str` suffix, `list` sources)
        
        :rtype: tuple
        """
        given_name = ""
        surname = ""
        suffix = ""
        sources = []

        # Return the first gedcom.tags.GEDCOM_TAG_NAME that is found.
        # Alternatively as soon as we have both the gedcom.tags.GEDCOM_TAG_GIVEN_NAME and _SURNAME return those.

        for child in self.get_child_elements():
            if child.get_tag() == gedcom.tags.GEDCOM_TAG_NAME:
                # Some GEDCOM files don't use child tags but instead
                # place the name in the value of the NAME tag.
                if child.get_value() != "":
                    name = child.get_value().split('/')

                    if len(name) > 0:
                        given_name = name[0].strip()
                        if len(name) > 1:
                            surname = name[1].strip()
                        if len(name) > 2:
                            suffix = name[2].strip()

                for childOfChild in child.get_child_elements():

                    if childOfChild.get_tag() == gedcom.tags.GEDCOM_TAG_GIVEN_NAME:
                        given_name = childOfChild.get_value()

                    if childOfChild.get_tag() == gedcom.tags.GEDCOM_TAG_SURNAME:
                        surname = childOfChild.get_value()

                    if childOfChild.get_tag() == gedcom.tags.GEDCOM_TAG_SUFFIX:
                        suffix = childOfChild.get_value()
                        
                    if childOfChild.get_tag() == gedcom.tags.GEDCOM_TAG_SOURCE:
                        sources.append(childOfChild)

                return given_name, surname, suffix, sources
                
        # If we reach here we are probably returning empty strings
        return given_name, surname, suffix, sources
    
    def get_all_names(self):
        """Returns list of individual's names
        
        :rtype: list
        """
        return [a.get_value() for a in self.get_child_elements() if a.get_tag() == gedcom.tags.GEDCOM_TAG_NAME]

    def get_first_name(self):
        """Returns an individual's first name 
        
        :rtype: str
        """
        result = self.get_name_data()[0].split(" ")
        return result[0] 

    def surname_match(self, surname_to_match):
        """Matches a string with the surname of an individual
        
        :type surname_to_match: str
        
        :rtype: bool
        """
        (given_name, surname) = self.get_name()
        return regex.search(surname_to_match, surname, regex.IGNORECASE)

    @deprecated
    def given_match(self, name):
        """Matches a string with the given name of an individual
        ::deprecated:: As of version 1.0.0 use `given_name_match()` method instead
        :type name: str
        :rtype: bool
        """
        return self.given_name_match(name)

    def given_name_match(self, given_name_to_match):
        """Matches a string with the given name of an individual
        
        :type given_name_to_match: str
        
        :rtype: bool
        """
        (given_name, surname) = self.get_name()
        return regex.search(given_name_to_match, given_name, regex.IGNORECASE)

    def get_gender(self):
        """Returns the gender of a person in string format
        
        :rtype: str
        """
        gender = ""

        for child in self.get_child_elements():
            if child.get_tag() == gedcom.tags.GEDCOM_TAG_SEX:
                gender = child.get_value()

        return gender

    def get_event_by_tag(self, tag=gedcom.tags.GEDCOM_TAG_BIRTH):
        """Returns the data of a person formatted as a tuple: (`str` date, `str` place, `list` sources)
        
        :rtype: tuple
        """
        date = ""
        place = ""
        sources = []
        
        # get primary date, place and sources
        for child in self.get_child_elements():
            if child.get_tag() == tag:
                for childOfChild in child.get_child_elements():
                    if childOfChild.get_tag() == gedcom.tags.GEDCOM_TAG_DATE:
                        date = childOfChild.get_value()

                    if childOfChild.get_tag() == gedcom.tags.GEDCOM_TAG_PLACE:
                        place = childOfChild.get_value()

                    if childOfChild.get_tag() == gedcom.tags.GEDCOM_TAG_SOURCE:
                        sources.append(childOfChild)
                
                break;

        return date, place, sources

    def get_event_year_by_tag(self, tag=gedcom.tags.GEDCOM_TAG_BIRTH):
        """Returns the year for the tag of a person in integer format
        
        :rtype: int
        """
        date_split = self.get_event_by_tag(tag)[0].split()

        if len(date_split) == 0:
            return -1
        
        date = date_split[len(date_split) - 1]

        if date == "":
            return -1
        try:
            return int(date)
        except ValueError:
            return -1

    def get_sources_by_tag_and_date(self, tag, date):
        """Returns the sources for a tag and date
        
        :rtype: list
        """
        return self.get_sources_by_tag_and_values(tag, date=date)

    def get_sources_by_tag_and_place(self, tag, place):
        """Returns the sources for a tag and place
        
        :rtype: list
        """
        return self.get_sources_by_tag_and_values(tag, place=place)
    
    def get_sources_by_tag_and_values(self, tag, date=None, place=None):
        """Returns the sources for a tag, date and place.  Set date or place to None if
        this value should be ignored
        
        :rtype: list
        """
        sources = []
        
        # get primary date, place and sources
        for child in self.get_child_elements():
            if child.get_tag() == tag:
                tag_sources = []
                tag_date = ""
                tag_place = ""

                for childOfChild in child.get_child_elements():
                    if childOfChild.get_tag() == gedcom.tags.GEDCOM_TAG_DATE:
                        tag_date = childOfChild.get_value()

                    if childOfChild.get_tag() == gedcom.tags.GEDCOM_TAG_PLACE:
                        tag_place = childOfChild.get_value()

                    if childOfChild.get_tag() == gedcom.tags.GEDCOM_TAG_SOURCE:
                        tag_sources.append(childOfChild)

                if (date == None or date == tag_date) and (place == None or place == tag_place):
                    sources += tag_sources

        return sources

    def get_birth_data(self):
        """Returns the birth data of a person formatted as a tuple: (`str` date, `str` place, `list` sources)
        
        :rtype: tuple
        """
        return self.get_event_by_tag(tag=gedcom.tags.GEDCOM_TAG_BIRTH)

    def get_birth_year(self):
        """Returns the birth year of a person in integer format
        
        :rtype: int
        """
        return self.get_event_year_by_tag(tag=gedcom.tags.GEDCOM_TAG_BIRTH)

    def get_birth_date(self):
        """Returns the birth date of a person as a str
        
        :rtype: str
        """
        return self.get_event_by_tag(tag=gedcom.tags.GEDCOM_TAG_BIRTH)[0]        

    def get_birth_place(self):
        """Returns the birth date of a person as a str
        
        :rtype: str
        """
        return self.get_event_by_tag(tag=gedcom.tags.GEDCOM_TAG_BIRTH)[1]        

    def get_death_data(self):
        """Returns the death data of a person formatted as a tuple: (`str` date, `str` place, `list` sources)
        
        :rtype: tuple
        """
        return self.get_event_by_tag(tag=gedcom.tags.GEDCOM_TAG_DEATH)

    def get_death_year(self):
        """Returns the death year of a person in integer format
        
        :rtype: int
        """
        return self.get_event_year_by_tag(tag=gedcom.tags.GEDCOM_TAG_DEATH)

    def get_death_date(self):
        """Returns the birth date of a person as a str
        
        :rtype: str
        """
        return self.get_event_by_tag(tag=gedcom.tags.GEDCOM_TAG_DEATH)[0]        

    def get_death_place(self):
        """Returns the birth date of a person as a str
        
        :rtype: str
        """
        return self.get_event_by_tag(tag=gedcom.tags.GEDCOM_TAG_DEATH)[1]        

    @deprecated
    def get_burial(self):
        """Returns the burial data of a person formatted as a tuple: (`str` date, `str´ place, `list` sources)
        ::deprecated:: As of version 1.0.0 use `get_burial_data()` method instead
        :rtype: tuple
        """
        self.get_burial_data()

    def get_burial_data(self):
        """Returns the burial data of a person formatted as a tuple: (`str` date, `str´ place, `list` sources)
        
        :rtype: tuple
        """
        return self.get_event_by_tag(tag="BURI")

    @deprecated
    def get_census(self):
        """Returns a list of censuses of an individual formatted as tuples: (`str` date, `str´ place, `list` sources)
        ::deprecated:: As of version 1.0.0 use `get_census_data()` method instead
        :rtype: list of tuple
        """
        self.get_census_data()

    def get_census_data(self):
        """Returns a list of censuses of an individual formatted as tuples: (`str` date, `str´ place, `list` sources)
        
        :rtype: list of tuple
        """
        census = []

        for child in self.get_child_elements():
            if child.get_tag() == gedcom.tags.GEDCOM_TAG_CENSUS:

                date = ''
                place = ''
                sources = []

                for childOfChild in child.get_child_elements():

                    if childOfChild.get_tag() == gedcom.tags.GEDCOM_TAG_DATE:
                        date = childOfChild.get_value()

                    if childOfChild.get_tag() == gedcom.tags.GEDCOM_TAG_PLACE:
                        place = childOfChild.get_value()

                    if childOfChild.get_tag() == gedcom.tags.GEDCOM_TAG_SOURCE:
                        sources.append(childOfChild.get_value())

                census.append((date, place, sources))

        return census

    def get_last_change_date(self):
        """Returns the date of when the person data was last changed formatted as a string
        
        :rtype: str
        """
        date = ""

        for child in self.get_child_elements():
            if child.get_tag() == gedcom.tags.GEDCOM_TAG_CHANGE:
                for childOfChild in child.get_child_elements():
                    if childOfChild.get_tag() == gedcom.tags.GEDCOM_TAG_DATE:
                        date = childOfChild.get_value()

        return date

    def get_occupation(self):
        """Returns the occupation of a person
        
        :rtype: str
        """
        occupation = ""

        for child in self.get_child_elements():
            if child.get_tag() == gedcom.tags.GEDCOM_TAG_OCCUPATION:
                occupation = child.get_value()

        return occupation

    def birth_year_match(self, year):
        """Returns `True` if the given year matches the birth year of this person
        
        :type year: int
        
        :rtype: bool
        """
        return self.get_birth_year() == year

    def birth_range_match(self, from_year, to_year):
        """Checks if the birth year of a person lies within the given range
        
        :type from_year: int
        
        :type to_year: int
        
        :rtype: bool
        """
        birth_year = self.get_birth_year()

        if from_year <= birth_year <= to_year:
            return True

        return False

    def death_year_match(self, year):
        """Returns `True` if the given year matches the death year of this person
        
        :type year: int
        
        :rtype: bool
        """
        return self.get_death_year() == year

    def death_range_match(self, from_year, to_year):
        """Checks if the death year of a person lies within the given range
        
        :type from_year: int
        
        :type to_year: int
        
        :rtype: bool
        """
        death_year = self.get_death_year()

        if from_year <= death_year <= to_year:
            return True

        return False

    def criteria_match(self, criteria):
        """Checks if this individual matches all of the given criteria
        `criteria` is a colon-separated list, where each item in the
        list has the form [name]=[value]. The following criteria are supported:
        
        surname=[name] - Match a person with [name] in any part of the `surname`.
        
        given_name=[given_name] - Match a person with [given_name] in any part of the given `given_name`.
        
        birth=[year] - Match a person whose birth year is a four-digit [year].
        
        birth_range=[from_year-to_year] - Match a person whose birth year is in the range of years from
        [from_year] to [to_year], including both [from_year] and [to_year].

        death=[year] - Match a person whose death year is a four-digit [year].
        
        death_range=[from_year-to_year] - Match a person whose death year is in the range of years from
        [from_year] to [to_year], including both [from_year] and [to_year].

        :type criteria: str
        
        :rtype: bool
        """

        # Check if criteria is a valid criteria and can be split by `:` and `=` characters
        try:
            for criterion in criteria.split(':'):
                criterion.split('=')
        except ValueError:
            return False

        match = True

        for criterion in criteria.split(':'):
            key, value = criterion.split('=')

            if key == "surname" and not self.surname_match(value):
                match = False
            elif (key == "name" or key == "given_name") and not self.given_name_match(value):
                match = False
            elif key == "birth":

                try:
                    year = int(value)
                    if not self.birth_year_match(year):
                        match = False
                except ValueError:
                    match = False

            elif key == "birth_range":

                try:
                    from_year, to_year = value.split('-')
                    from_year = int(from_year)
                    to_year = int(to_year)
                    if not self.birth_range_match(from_year, to_year):
                        match = False
                except ValueError:
                    match = False

            elif key == "death":

                try:
                    year = int(value)
                    if not self.death_year_match(year):
                        match = False
                except ValueError:
                    match = False

            elif key == "death_range":

                try:
                    from_year, to_year = value.split('-')
                    from_year = int(from_year)
                    to_year = int(to_year)
                    if not self.death_range_match(from_year, to_year):
                        match = False
                except ValueError:
                    match = False

        return match