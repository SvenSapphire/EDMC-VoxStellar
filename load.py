#!/usr/bin/env python
# vim: textwidth=0 wrapmargin=0 tabstop=4 shiftwidth=4 softtabstop=4 smartindent smarttab
"""Plugin that tests that modules we bundle for plugins are present and working."""

import logging
import os

from voxstellar.voxstellar import VoxStellar
from voxstellar.debug import Debug

PLUGIN_NAME = "EDMC-VoxStellar"

this: VoxStellar = VoxStellar(PLUGIN_NAME)


def plugin_start3(plugin_dir: str) -> str:
    """
    Plugin startup method.
    """
    this.plugin_start(plugin_dir)

    return this.plugin_name


def plugin_stop():
    """
    Plugin stop method.

    :return:
    """
    return this.plugin_stop


def journal_entry(cmdrname: str, is_beta: bool, system: str, station: str, entry: dict, state: dict) -> None:
    """
    Handle the given journal entry.

    :param cmdrname:
    :param is_beta:
    :param system:
    :param station:
    :param entry:
    :param state:
    :return: None
    """

    this.journal_entry(cmdrname, is_beta, system, station, entry, state)
