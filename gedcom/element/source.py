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

"""GEDCOM element consisting of tag `gedcom.tags.GEDCOM_TAG_SOURCE`"""

from gedcom.element.element import Element
import gedcom.tags


class NotAnActualSourceError(Exception):
    pass


class SourceElement(Element):

    def get_tag(self):
        return gedcom.tags.GEDCOM_TAG_SOURCE

    def get_objects(self):
        """Returns the objects of a person formatted as a list
        
        :rtype: list
        """
        sources = []

        for child in self.get_child_elements():
            if child.get_tag() == gedcom.tags.GEDCOM_TAG_OBJECT:
                sources.append(child)

        return sources
    
    def get_author(self):
        """Returns name of author
        
        :rtype: str
        """
        return self.get_child_value_by_tag(gedcom.tags.GEDCOM_TAG_AUTHOR)
    
    def get_page(self):
        """Returns page of source
        
        :rtype: str
        """
        return self.get_child_value_by_tag(gedcom.tags.GEDCOM_TAG_PAGE)

    def get_publisher(self):
        """Returns publisher of source
        
        :rtype: str
        """
        return self.get_child_value_by_tag(gedcom.tags.GEDCOM_TAG_PUBLISHER)

    def get_repository(self):
        """Returns pointer of source's repository
        
        :rtype: str
        """
        return self.get_child_value_by_tag(gedcom.tags.GEDCOM_TAG_REPOSITORY)

    def get_title(self):
        """Returns title of source
        
        :rtype: str
        """
        return self.get_child_value_by_tag(gedcom.tags.GEDCOM_TAG_TITLE)