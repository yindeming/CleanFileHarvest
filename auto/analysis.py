#!/usr/bin/python 
from vmauto import VMwareAuto
import os, sys, time
import hashlib
import subprocess

# name of the clean snapshot
snapname = 'clean'

# path to vmware guest's VMX configuration file
vmx = 'vmware/WindowsXP/WindowsXP.vmx'

def analyze(vm, sample):
    # copy the malware sample to the VM's hard  drive
    dst = 'C:\\%s' % os.path.basename(sample)
    vm.copytovm(sample, dst)

    # use the script to execute the sample in the guest VM, let it run
    # for 2 minutes
    vm.winexec('C:\\auto.exe')
    time.sleep(120)

    # shut down the VM
    vm.stop()

    # mount the disk and scan
    

    # revert VM to clean snapshot
    vm.revert(clean)
    vm.start()

    
def main():
