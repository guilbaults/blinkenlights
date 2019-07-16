from sasutils.sas import SASBlockDevice
from sasutils.scsi import EnclosureDevice
from sasutils.ses import ses_get_id_xyratex
from sasutils.sysfs import sysfs
import argparse
import re
import subprocess
import time


def device_to_position(dev):
    blkdev = SASBlockDevice(sysfs.node('block').node(dev).node('device'))
    sasdev = blkdev.end_device.sas_device
    slot = int(sasdev.attrs.bay_identifier)
    ses_sg = blkdev.array_device.enclosure.scsi_generic.sg_name
    jbodid = ses_get_id_xyratex(ses_sg)
    return (jbodid, slot)


def get_jbod_sg(jbodid):
    for node in sysfs.node('class').node('enclosure'):
        enclosure = EnclosureDevice(node.node('device'))
        sg_dev = enclosure.scsi_generic
        if ses_get_id_xyratex(sg_dev.name) == jbodid:
            return sg_dev.name


def jbod_action(sg_dev, slot, action_flag):
    index_str = '--index=%i' % slot
    cmdargs = ['sg_ses', '--page=0x02', index_str, action_flag,
               '/dev/' + sg_dev]
    stdout, stderr = subprocess.Popen(cmdargs,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE).communicate()
    # TODO confirm state instead of sleeping
    time.sleep(1)


def blinkenlight(jbodid, slot, args):
    sg_dev = get_jbod_sg(jbodid)
    if(args.rtr):
        # Ready-to-remove will poweroff the drive and turn on the fault LED
        jbod_action(sg_dev, slot, '--set=devoff')
        jbod_action(sg_dev, slot, '--set=fault')
        print('Ready-to-remove jbod%02d-bay%d' % (jbodid, slot))
    elif(args.insert):
        # Incase a new drive insertion does not spinup or clear the fault LED
        jbod_action(sg_dev, slot, '--clear=devoff')
        jbod_action(sg_dev, slot, '--clear=fault')
        print('Inserting jbod%02d-bay%d' % (jbodid, slot))
    elif(args.locate_on):
        jbod_action(sg_dev, slot, '--set=locate')
        print('Turning on LED on jbod%02d-bay%d' % (jbodid, slot))
    elif(args.locate_off):
        jbod_action(sg_dev, slot, '--clear=locate')
        print('Turning off LED on jbod%02d-bay%d' % (jbodid, slot))
    else:
        return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tool used to managed drive \
LED and power status in a JBOD. \
This tool can accept drive path in 2 format: \
/dev/mapper/jbod00-bay00 or /dev/sdx')
    parser.add_argument('path')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--rtr', help='set a drive in ready-to-remove state',
                       action='store_true')
    group.add_argument('--insert', help='in case a new drive is not detected',
                       action='store_true')
    group.add_argument('--locate-on', help='turn on drive locate LED',
                       action='store_true')
    group.add_argument('--locate-off', help='turn off drive locate LED',
                       action='store_true')

    args = parser.parse_args()
    device_match = re.match('^/dev/(sd[a-z]+)$', args.path)
    jbod_match = re.match('^/dev/mapper/jbod([0-9]{2})-bay([0-9]{2,3})$',
                          args.path)

    if(device_match):
        dev = device_match.group(1)
        position = device_to_position(dev)
        print('Disk is in position jbod%02d-bay%d' % (position))
        blinkenlight(position[0], position[1], args)
    elif(jbod_match):
        jbodid = int(jbod_match.group(1))
        slot = int(jbod_match.group(2))
        blinkenlight(jbodid, slot, args)
    else:
        print('Device path is unrecognised')
