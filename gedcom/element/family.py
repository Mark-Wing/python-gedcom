# -*- coding: utf-8 -*-

# Python GEDCOM Parser
#
# Copyright (C) 2022-2025 Mark Wing (mark @ markwing.net)
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

"""GEDCOM element consisting of tag `gedcom.tags.GEDCOM_TAG_FAMILY`"""

from gedcom.element.element import Element
import gedcom.tags


class NotAnActualFamilyError(Exception):
    pass


class FamilyElement(Element):

    def get_tag(self):
        return gedcom.tags.GEDCOM_TAG_FAMILY
    
    def get_children(self):
        """Returns a list of the children in the family

        :rtype: list
        """
        return self.get_elements_by_tag(gedcom.tags.GEDCOM_TAG_CHILD)
        
    def get_husbands(self):
        """Returns a list of the husbands in the family

        :rtype: list
        """
        return self.get_elements_by_tag(gedcom.tags.GEDCOM_TAG_HUSBAND)
        
    def get_wives(self):
        """Returns a list of the wives in the family

        :rtype: list
        """
        return self.get_elements_by_tag(gedcom.tags.GEDCOM_TAG_WIFE)
        
    def get_marriages(self):
        """Returns a list of the marriage in the family

        :rtype: list
        """
        return self.get_elements_by_tag(gedcom.tags.GEDCOM_TAG_MARRIAGE)

    def get_divorces(self):
        """Returns a list of the divorces in the family

        :rtype: list
        """
        return self.get_elements_by_tag(gedcom.tags.GEDCOM_TAG_DIVORCE)
    
    def get_marriages_data(self):
        """Returns a list of the marriage in the family

        :rtype: list
        """
        return self.get_relationship_data(relationship_type=gedcom.tags.GEDCOM_TAG_MARRIAGE)

    def get_divorces_data(self):
        """Returns a list of the marriage in the family

        :rtype: list
        """
        return self.get_relationship_data(relationship_type=gedcom.tags.GEDCOM_TAG_DIVORCE)
    
    def get_relationship_data(self, relationship_type=gedcom.tags.GEDCOM_TAG_MARRIAGE):
        """Returns a list of marriages of an individual formatted as a tuple (`str` spouse, `str` date, `str` place, `list` sources)

        :type relationship_type: string

        :rtype: tuple
        """
        relationships = []

        for marriage in self.get_elements_by_tag(relationship_type):
            date = ''
            place = ''
            sources = []

            for relationship_data in marriage.get_child_elements():
                if relationship_data.get_tag() == gedcom.tags.GEDCOM_TAG_DATE:
                    date = relationship_data.get_value()
                if relationship_data.get_tag() == gedcom.tags.GEDCOM_TAG_PLACE:
                    place = relationship_data.get_value()
                if relationship_data.get_tag() == gedcom.tags.GEDCOM_TAG_SOURCE:
                    sources.append(relationship_data)
                                
            relationships.append((date, place, sources))
        
        return relationships
    
    def get_elements_by_tag(self, tag):
        """Returns a list of the child elements by tag in the family

        :rtype: list
        """
        result = []

        for child in self.get_child_elements():
            if child.get_tag() == tag:
                result.append(child)

        return result
        