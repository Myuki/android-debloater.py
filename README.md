# A script to disable Android bloatware

## Requirements

* [Android Debug Bridge](https://developer.android.com/studio/command-line/adb)

## CLI

```
android-debloater.py [parameters...] <commands> [packages...]
```

## Parameters

```
-u --user
  Default value is 0. Specify Android user ID.

-a --adb
  Default use system environment path. Specify ADB path.

-i --input
  Specify a package list file path to use file instead of command line package list.
```

It supports use `,` separately run for multiple users in order like `0,10`.

## Commands

```
disable - adb shell pm disable-user

clear - adb shell pm clear

enable - adb shell pm enable
```

It supports use `,` separately run multiple commands in order like `disable,clear`.

## Package List File

One package per line.

Example file `package.list`:

```
com.google.android.gm
com.google.android.syncadapters.calendar
com.google.android.syncadapters.contacts
```

## List Files

`lists/` has some app lists for specific device.

**Warning!** It is a specific purpose list include some maybe necessary app like Google Search and Gmail. You should check the app list before use it.

## Example

```
./android-debloater.py -u 0 disable com.google.android.gm com.google.android.syncadapters.calendar com.google.android.syncadapters.contacts

./android-debloater.py -u 0,10 -i ./lists/lemonades.txt disable,clear 
```
