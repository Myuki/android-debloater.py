#!/usr/bin/env python3

import getopt
import os
import subprocess
import sys

availableCommands: set[str] = {"clear", "disable", "enable"}
availableUsers: set[int] = set()

# Default args
adbPath: str = "adb"
inputUsers: list[int] = [0]
inputCommands: list[str] = []
inputPackages: list[str] = []


# Exit after print error
def criticalError(inlineOutput: str = "", moreOutput: str = ""):
  print(f"!Error: {inlineOutput}")
  if moreOutput:
    print(moreOutput)
  sys.exit(1)


def clenCliLine(override: str = "", lf: bool = True, width: int = 90):
  print("\r" + " " * width, end="")
  if override:
    if lf:
      print("\r" + override)
    else:
      print("\r" + override, end="")


def checkCliExist(path: str) -> bool:
  try:
    result = subprocess.run(path, capture_output=True)
  except FileNotFoundError:
    return False
  else:
    return True


def checkUser(inputId: int) -> bool:
  # Get user list
  global availableUsers
  if not availableUsers:
    command: str = "adb shell pm list users"
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
      criticalError("Can't retrieve the user list", result.stderr.strip())
    for line in result.stdout.splitlines()[1:]:
      if "UserInfo{" in line:
        id: int = int(line[line.index("{") + 1:line.index(":")])
        availableUsers.add(id)

  if inputId in availableUsers:
    return True
  else:
    return False


def parseCli():
  cliHint = "usage: android-debloater.py [-u | --user <id>] [-a | --adb <path>] [-i | --input <path>] <clear | disable | enable> [packages...]"

  opts, args = getopt.getopt(
      sys.argv[1:], "u:a:i:", longopts=["user", "adb", "input"])
  if not args or not opts:
    criticalError("Wrong parameter!", cliHint)

  for opt, arg in opts:
    # Check user ID
    global inputUsers
    if opt in ("-u", "--user"):
      inputUsers = []
      # Support multiple users
      if "," in arg:
        for id in arg.split(","):
          if id.isdigit() and checkUser(int(id)):
            inputUsers.append(int(id))
          else:
            criticalError(f"Wrong user ID: {id}",
                          f"Available Users: {availableUsers}")
      else:
        if arg.isdigit() and checkUser(int(arg)):
          inputUsers.append(int(arg))
        else:
          criticalError(f"Wrong user ID: {arg}",
                        f"Available Users: {availableUsers}")

    # Check ADB
    elif opt in ("-a", "--adb"):
      global adbPath
      if checkCliExist(arg):
        adbPath = arg
      else:
        criticalError(f"Can't find adb! in {arg}")

    # Check package List file
    elif opt in ("-i", "--input"):
      global inputPackages
      if os.path.exists(arg):
        with open(arg, "r") as file:
          for line in file.readlines():
            inputPackages.append(line.strip())
      else:
        criticalError(f"Can't find {arg}!")

    else:
      criticalError("Wrong parameter!", cliHint)

  # Check option
  cmds: str = args[0]
  # Support multiple options
  if "," in cmds:
    for cmd in cmds.split(","):
      if cmd in availableCommands:
        if cmd == "disable":
          inputCommands.append("disable-user")
        else:
          inputCommands.append(cmd)
      else:
        criticalError(f"Wrong command: {cmd}",
                      "Support command: clear, disable, enable")
  else:
    if cmds in availableCommands:
      if cmds == "disable":
        inputCommands.append("disable-user")
      else:
        inputCommands.append(cmds)
    else:
      criticalError(f" Wrong command: {cmds}",
                    "Support command: clear, disable, enable")

  # Get package list
  inputPackages = inputPackages + args[1:]
  if not inputPackages:
    criticalError("Empty package!")


if __name__ == "__main__":
  parseCli()

  adbResult: dict[str, subprocess.CompletedProcess] = {}
  total: int = len(inputUsers) * len(inputCommands) * len(inputPackages)
  count: int = 0

  for user in inputUsers:
    for package in inputPackages:
      for cmd in inputCommands:
        count = count + 1
        clenCliLine(f"{count}/{total}: User {user}, {cmd} {package}...", False)
        try:
          command = f"{adbPath} shell pm {cmd} --user {user} {package}"
          adbResult[f"User {user}: {cmd} {package}"] = subprocess.run(
              command, capture_output=True, text=True)
        except Exception as e:
          print(e)
          count = count - 1
  clenCliLine(f"{count}/{total}")

  # Chcek result
  error = False
  for cmd, result in adbResult.items():
    # Print ADB output if return code is not 0
    if result.returncode != 0:
      error = True
      print(f"\n!Error: {cmd}:")
      print(result.stderr.strip())
  if error:
    print("\nComplete with error!\n")
  else:
    print("\nComplete!\n")
