#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 13:13:13 2022

@author: fatih
"""
from pathlib import Path
import configparser


class UserSettings(object):
    def __init__(self):

        self.user_home = Path.home()
        self.user_config_dir = Path.joinpath(self.user_home, Path(".config/pardus-mycomputer"))
        self.user_config_file = Path.joinpath(self.user_config_dir, Path("settings.ini"))

        self.config = configparser.ConfigParser(strict=False)
        self.config_closeapp_pardus = None
        self.config_closeapp_hdd = None
        self.config_closeapp_usb = None
        self.config_autorefresh = None
        self.config_autorefresh_time = None


    def createDefaultConfig(self, force=False):
        self.config['MAIN'] = {
            'CloseAppPardus': 'no',
            'CloseAppHDD': 'no',
            'CloseAppUSB': 'no',
            'AutoRefresh': 'no',
            'AutoRefreshTime': 5
        }

        if not Path.is_file(self.user_config_file) or force:
            if self.createDir(self.user_config_dir):
                with open(self.user_config_file, "w") as cf:
                    self.config.write(cf)

    def readConfig(self):
        try:
            self.config.read(self.user_config_file)
            self.config_closeapp_pardus = self.config.getboolean('MAIN', 'CloseAppPardus')
            self.config_closeapp_hdd = self.config.getboolean('MAIN', 'CloseAppHDD')
            self.config_closeapp_usb = self.config.getboolean('MAIN', 'CloseAppUSB')
            self.config_autorefresh = self.config.getboolean('MAIN', 'AutoRefresh')
            self.config_autorefresh_time = self.config.getfloat('MAIN', 'AutoRefreshTime')

        except Exception as e:
            print("{}".format(e))
            print("user config read error ! Trying create defaults")
            # if not read; try to create defaults
            self.config_closeapp_pardus = False
            self.config_closeapp_hdd = False
            self.config_closeapp_usb = False
            self.config_autorefresh = False
            self.config_autorefresh_time = 5.0
            try:
                self.createDefaultConfig(force=True)
            except Exception as e:
                print("self.createDefaultConfig(force=True) : {}".format(e))

    def writeConfig(self, closeapppardus, closeapphdd, closeappusb, autorefresh, autorefreshtime):
        self.config['MAIN'] = {
            'CloseAppPardus': closeapppardus,
            'CloseAppHDD': closeapphdd,
            'CloseAppUSB': closeappusb,
            'AutoRefresh': autorefresh,
            'AutoRefreshTime': autorefreshtime
        }
        if self.createDir(self.user_config_dir):
            with open(self.user_config_file, "w") as cf:
                self.config.write(cf)
                return True
        return False

    def createDir(self, dir):
        try:
            Path(dir).mkdir(parents=True, exist_ok=True)
            return True
        except:
            print("{} : {}".format("mkdir error", dir))
            return False