#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

