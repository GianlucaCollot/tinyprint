import sys, os, codecs, json, six, time
from bluepy import btle


printer_mac_addp = '84:05:4E:A7:A8:8E' #X5
MTU = 123

if __name__ == '__main__':
    try:
        i_file = sys.argv[1]
        if not os.path.isfile(i_file):
            raise IndexError
    except IndexError:
        print(f'[E]', 'Usage: {sys.argv[0]} [hex_image_dump]')
        exit(1)

    try:
        print('[I] ', 'Trying to connected to {}...'.format(printer_mac_addp))
        printer = btle.Peripheral(deviceAddr=printer_mac_addp)
        print('[I] ', 'Connected to {}'.format(printer_mac_addp))
    except btle.BTLEDisconnectError as err:
        print('[E] ', err)
        exit(1)

    print('[I] ', 'Setting MTU: {}...'.format(MTU))
    resp = printer.setMTU(MTU)

    # print('[I] ', str(resp))

    print('[I] ', 'Do some nesessery write requests...')
    printer.writeCharacteristic(6, codecs.decode('5178a80001000000ff5178a30001000000ff', 'hex'))
    printer.writeCharacteristic(6, codecs.decode('5178bb0001000107ff', 'hex'))

    text_file = open(i_file, "r")
    image = text_file.readlines()
    image = ['5178' + line[:-1] + 'ff' for line in image]
    # image = ''

    from textwrap import wrap

    # image = wrap(image, 112)
    # Start to write an image
    print('[I] ', 'Start writing image')
    for l in image:
        print(l)
        printer.writeCharacteristic(6, codecs.decode(l, 'hex'))
        time.sleep(0.1)

    print('[I] ', 'Disonnected from {}'.format(printer_mac_addp))
    printer.disconnect()
