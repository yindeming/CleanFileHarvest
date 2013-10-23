from vmauto import VMwareAuto
import os, sys, time, analysis


"""

# path to vmware guest's VMX configuration file
guest_vmx = '/auto/VM/WindowsXP.vmx'

# select the VM
vm = VMwareAuto('/auto/VM/WindowsXP.vmx')

"""


def analyze(vm, sample, rdir, nvcc):
    # scan the sample with nvcc scanner

    # revert to the base snapshot 'cleanimg'
    vm.revert('cleanimg')
    vm.start()
    time.sleep(15)

    # copy the sample to a path on the VM
    dst = 'C:\\%s' % os.path.basename(sample)
    vm.copytovm(sample, dst)

    # exexute the malware

    # take a screen shot of the guest VM's desktop
    vm.scrshot(rdir + 'shot.bmp')

    # suspend the VM
    vm.suspend()

def main(argv):
    vm = VMwareAuto(guest_vmx)

    if os.path.isfile(sys.argv[1]):
        rdir = report_path + \
            os.path.sep + \
            hashlib.md5(open(sys.argv[1]).read()).hexdigest()

        try:
            os.mkdir(rdir)
        except:
            pass

        analyze(vm, sys.argv[1], rdir, nvcc)
    else:
        print 'You must provide a valid file to analyze'
        return

if __name__ == '__main__':
    main(sys.argv)
