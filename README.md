# A script to disable Android bloatware

## Requirement

* [Android Debug Bridge](https://developer.android.com/studio/command-line/adb)

## Command

```
android-debloater.py [arguments...] [package...]
```

## Arguments

```
-u --user
  Specify Android user ID, default value is 0.

-a --adb
  Specify ADB path, default use system environment path.

-i --input
  Specify a package list file path to use file instead of command line package list.
```

## Options

```
disable, disable-user - adb shell pm disable-user

clear - adb shell pm clear

disable-clear - run both disable and clear

enable - adb shell pm enable
```

## Package List File

One package per line.

Example file `package.list`:

```
com.google.android.gm
com.google.android.syncadapters.calendar
com.google.android.syncadapters.contacts
```

## Example

```
python.exe .\android-debloater.py -u 0 disable-clear com.google.android.gm com.google.android.syncadapters.calendar com.google.android.syncadapters.contacts

python.exe .\android-debloater.py -u 0 -i package.list disable-clear 
```
