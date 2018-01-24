# Blinklights
This tool is used to control the LEDs and slot power in a Xyratex 84 slots JBODs, also know as:

* Seagate/Xyratex SP-2584
* Dell MD1280
* Lenovo D3284

This script can be adapted for other types of JBODs, as long as its possible to control the LED/power with a `sg_ses` command. 

## Requirements
* [sasutils (fork for Xyratex 84 slots JBOD)](https://github.com/guilbaults/sasutils) based on [sasutils from Stanford](https://github.com/stanford-rc/sasutils)
* `sg_ses`

## Usage
This tool can control the "ident" LED with `--locate-on` and `--locate-off`, this command will make the LED on the slot blink.

The power going to a drive can also be cut using `--rtr` (ready-to-remove), this will also light up the steady fault LED.

After a disk replacement, the slot should turn off the fault LED by itself and the power to the slot should be restored automatically, in case this does not happen, it can be forced with `--insert`. 

A drive power cycle can be done with `--rtr` and `--insert` with a small pause between theses 2 commands. 

```
blinkenlights.py --help
usage: blinkenlights.py [-h] [--rtr | --insert | --locate-on | --locate-off]
                        path

Tool used to managed drive LED and power status in a JBOD. This tool can
accept drive path in 2 format: /dev/mapper/jbod00-bay00 or /dev/sdx

positional arguments:
  path

optional arguments:
  -h, --help    show this help message and exit
  --rtr         set a drive in ready-to-remove state
  --insert      in case a new drive is not detected
  --locate-on   turn on drive locate LED
  --locate-off  turn off drive locate LED
```
