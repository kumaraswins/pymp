#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This file is part of pymp.

    pymp is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pymp is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with pymp.  If not, see <http://www.gnu.org/licenses/>.
"""
import subprocess

def getMaemoString():
  try:
    p=subprocess.Popen(["osso-product-info","-q","OSSO_PRODUCT_RELEASE_NAME"],
                       stderr=subprocess.PIPE,
                       stdout=subprocess.PIPE)
    maemoVersion=p.communicate()
    return maemoVersion[0].strip()
  except OSError:
    return ""

def isMaemo5():
  maemoVersion=getMaemoString()
  if maemoVersion == "Maemo 5":
    return True
  else:
    return False
