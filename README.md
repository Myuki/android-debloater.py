# A script to disable Android bloatware

## Requirement

* [Android Debug Bridge](https://developer.android.com/studio/command-line/adb)

## Command

```
android-debloater.py [parameters...] <Option> [packages...]
```

## Parameters

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

## List Files

`list/` has some app list for some device.

Warning! It is a specific purpose list include some maybe necessary app like Google Search and Gmail. You should check the app list before use it.

## Example

```
./android-debloater.py -u 0 disable-clear com.google.android.gm com.google.android.syncadapters.calendar com.google.android.syncadapters.contacts

./android-debloater.py -u 0 -i ./list/lemonade.txt disable-clear 
```
