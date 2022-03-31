#!/usr/bin/env python3

import getopt
import subprocess
import sys
from typing import Dict, Set

if __name__ == "__main__":
  # Default parameters
  adbPath: str = "adb"
  user: str = "0"
  pmOption: str = ""
  availablePmOption: Set[str] = {"disable-user", "clear", "disable-clear", "enable"}

  packageListFilePath: str = ""

  # Get user list
  userList: Set[str] = set()
  command: str = "adb shell pm list users"
  result = subprocess.run(command, capture_output=True, text=True)
  if result.returncode != 0:
    print("!Error:")
    print(result.stdout.strip())
    sys.exit(1)
  for line in result.stdout.splitlines()[1:]:
    if "UserInfo{" in line:
      userList.add(line[line.index("{") + 1:line.index(":")])

  # Parse parameters
  options, parameters = getopt.getopt(sys.argv[1:], "u:a:i:", longopts=["user", "adb", "input"])
  for option, parameter in options:
    # Check user ID
    if option in ("-u", "--user"):
      if parameter.isdigit() and parameter in userList:
        user = parameter
      else:
        print("!Error: Wrong user ID: " + parameter)
        sys.exit(1)
    elif option in ("-a", "--adb"):
      adbPath = parameter
    elif option in ("-i", "--input"):
      packageListFilePath = parameter

  # Parse option
  if len(parameters) == 0:
    print("!Error: Empty parameter!")
    sys.exit(1)
  pmOption: str = parameters[0]
  if pmOption == "disable":
    pmOption = "disable-user"
  if pmOption not in availablePmOption:
    print("!Error: Wrong option: " + pmOption)
    print("Support option: disable-user(disable), clear, disable-clear, enable")
    sys.exit(1)

  # Get package list
  packageList: set = set()
  if packageListFilePath != "":
    with open(packageListFilePath, "r") as file:
      for line in file.readlines():
        packageList.add(line.strip())
  else:
    packageList = set(parameters[1:])
  if packageList == set():
    print("!Error: Empty package!")
    sys.exit(1)

  # Run command
  adbResult: Dict[str, subprocess.CompletedProcess] = {}
  for package in packageList:
    print(f"{pmOption.capitalize()} {package}...")
    try:
      if pmOption == "disable-clear":
        command = f"{adbPath} shell pm disable-user --user {user} {package}"
        adbResult[f"disable-user {package} for user {user}"] = subprocess.run(command, capture_output=True, text=True)
        command = f"{adbPath} shell pm clear --user {user} {package}"
        adbResult[f"clear {package} for user {user}"] = subprocess.run(command, capture_output=True, text=True)
      else:
        command = f"{adbPath} shell pm {pmOption} --user {user} {package}"
        adbResult[f"{pmOption} {package} for user {user}"] = subprocess.run(command, capture_output=True, text=True)
    except Exception as e:
      print(e)

  # Chcek result
  error = False
  for op, result in adbResult.items():
    # Print ADB output if return code is not 0
    if result.returncode != 0:
      error = True
      print(f"\nError: Fail to {op}:")
      print(result.stderr.strip())
  if error:
    print("\nComplete with error!\n")
  else:
    print("\nComplete!\n")
