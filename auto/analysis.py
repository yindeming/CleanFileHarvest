#!/usr/bin/python 
from vmauto import VMwareAuto
import os, sys, time
import subprocess

# name of the clean snapshot
snapname = 'clean'

# path to vmware guest's VMX configuration file
vmx = 'data/WindowsXP/WindowsXP.vmx'
disk = 'data/WindowsXP/WindowxXP.vmdk'
nvcc = 'data/scanner/nvcc.exe'

def analyze(vm, sample):
    # copy the malware sample to the VM's hard  drive
    dst = 'C:\\%s' % os.path.basename(sample)
    vm.copytovm(sample, dst)

    # use the script to execute the sample in the guest VM, let it run
    # for 2 minutes
    vm.winexec('C:\\auto_install.exe')
    time.sleep(300)

    # shut down the VM
    vm.stop()

    # mount the disk image
    mount = subprocess.Popen(vmware-mount, disk, '-o', 'ro', 'mount_tmp')
    
    # scan
    scan = subprocess.Popen(wine, nvcc, '/C:0', '/S:0', '/U', '/L:2', 'D:')
    
    # wait for scanning to finish
    time.sleep(1200)
    
    # unmount the disk image
    unmount = subprocess.Popen(vmware-mount, '-x')

    # revert VM to clean snapshot
    vm.revert(clean)
    vm.start()

    
def main():
    vm = VMwareAuto(vmx)
    
if __name__ == '__main__':
    main()
