#!/usr/bin/env python3

import getopt
import re
import subprocess
import sys
from typing import Set

if __name__ == "__main__":
  # Default arguments
  adbPath: str = "adb"
  user: str = "0"
  pmOption: str = ""
  availablePmOption: Set[str] = {"disable-user", "clear", "disable-clear", "enable"}

  packageListFilePath: str = ""

  # Get user list
  userList: set = set()
  command = "adb shell pm list users"
  output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode()
  for line in output[1:]:
    regex = r"UserInfo{\{(.*?)\:"
    tempUser: str = re.findall(regex, line)
    if tempUser != "":
      userList.add(user)

  # Parse arguments
  options, arguments = getopt.getopt(sys.argv[1:], "u:a:i:", longopts=["user", "adb", "input"])
  for option, argument in options:
    # Check user ID
    if option in ("-u", "--user"):
      if argument.isdigit() and argument in userList:
        user = argument
      else:
        print("Wrong user ID: " + argument)
        sys.exit(1)
    elif option in ("-a", "--adb"):
      adbPath = argument
    elif option in ("-i", "--input"):
      packageListFilePath = argument

  # Parse option
  pmOption: str = arguments[0]
  if pmOption == "disable":
    pmOption = "disable-user"
  if pmOption not in availablePmOption:
    print("Wrong option: " + pmOption)
    print("Support option: disable-user(disable), clear, disable-clear, enable")
    sys.exit(1)

  # Get package list
  packageList: set = set()
  if packageListFilePath != "":
    with open(packageListFilePath, "r") as file:
      for line in file.readlines():
        packageList.add(line.strip())
      file.close()
  else:
    packageList = set(arguments[1:])

  # Run command
  for package in packageList:
    print(pmOption + " " + package + ":")
    if pmOption == "disable-clear":
      command = adbPath + " shell pm disable-user --user " + user + " " + package
      output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode()
      command = adbPath + " shell pm clear --user " + user + " " + package
      subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode()
      print(output)
    else:
      command = adbPath + " shell pm " + pmOption + " --user " + user + " " + package
      output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode()
      print(output)
