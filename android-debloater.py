#!/usr/bin/env python3

import getopt
import subprocess
import sys
from typing import Dict, Set

if __name__ == "__main__":
  # Default arguments
  adbPath: str = "adb"
  user: str = "0"
  pmOption: str = ""
  availablePmOption: Set[str] = {"disable-user", "clear", "disable-clear", "enable"}

  packageListFilePath: str = ""

  # Get user list
  userList: Set[str] = set()
  command = "adb shell pm list users"
  process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  process.wait()
  if process.returncode != 0:
    print("Error:")
    print(process.stdout.read().decode().strip())
    sys.exit(1)
  for line in process.stdout.read().decode().splitlines()[1:]:
    if "UserInfo{" in line:
      userList.add(line[line.index("{") + 1:line.index(":")])

  # Parse arguments
  options, arguments = getopt.getopt(sys.argv[1:], "u:a:i:", longopts=["user", "adb", "input"])
  for option, argument in options:
    # Check user ID
    if option in ("-u", "--user"):
      if argument.isdigit() and argument in userList:
        user = argument
      else:
        print("Error: Wrong user ID: " + argument)
        sys.exit(1)
    elif option in ("-a", "--adb"):
      adbPath = argument
    elif option in ("-i", "--input"):
      packageListFilePath = argument

  # Parse option
  if len(arguments) == 0:
    print("Error: Empty argument!")
    sys.exit(1)
  pmOption: str = arguments[0]
  if pmOption == "disable":
    pmOption = "disable-user"
  if pmOption not in availablePmOption:
    print("Error: Wrong option: " + pmOption)
    print("Support option: disable-user(disable), clear, disable-clear, enable")
    sys.exit(1)

  # Get package list
  packageList: set = set()
  if packageListFilePath != "":
    with open(packageListFilePath, "r") as file:
      for line in file.readlines():
        packageList.add(line.strip())
  else:
    packageList = set(arguments[1:])
  if packageList == set():
    print("Error: Empty package!")
    sys.exit(1)

  # Run command
  processAdb: Dict[str, subprocess.Popen] = {}
  for package in packageList:
    print(f"{pmOption.capitalize()} {package}...")
    if pmOption == "disable-clear":
      command = f"{adbPath} shell pm disable-user --user {user} {package}"
      processAdb[f"disable-user {package} for user {user}"] = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      command = f"{adbPath} shell pm clear --user {user} {package}"
      processAdb[f"clear {package} for user {user}"] = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else:
      command = f"{adbPath} shell pm {pmOption} --user {user} {package}"
      processAdb[f"{pmOption} {package} for user {user}"] = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

  # Wait all adb subprocess
  error = False
  for op, process in processAdb.items():
    process.wait()
    # Print ADB output if return code is not 0
    if process.returncode != 0:
      error = True
      print(f"Error: Fail to {op}:")
      print(process.stdout.read().decode().strip())
  if error:
    print("Complete with error!\n")
  else:
    print("Complete!\n")
