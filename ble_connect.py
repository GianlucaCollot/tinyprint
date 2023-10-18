import sys, os, codecs, json, six, time
from bluepy import btle


printer_mac_addp = '84:05:4E:A7:A8:8E' #X5
MTU = 123


def image_from_wireshark_dump(i_file):
    with open(i_file) as j_file:
        pic_json = json.load(j_file)
    pic_hex = [val['_source']['layers']['btatt']['btatt.value'] for val in pic_json]
    pic_hex = [val.replace(':', '') for val in pic_hex]
    pic_hex = ''.join(pic_hex)
    return pic_hex


def image_from_file(i_file):
    with open(i_file) as j_file:
        rfid_metka_json = json.load(j_file)


if __name__ == '__main__':
    try:
        i_file = sys.argv[1]
        if not os.path.isfile(i_file):
            raise IndexError
    except IndexError:
        print(f'[E]', 'Usage: {sys.argv[0]} [wireshark_json_dump]')
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

    image = image_from_wireshark_dump(i_file)
    # image = ''

    from textwrap import wrap

    image = wrap(image, 112)
    # Start to write an image
    print('[I] ', 'Start writing image')
    for l in image:
        printer.writeCharacteristic(6, codecs.decode(l, 'hex'))
        time.sleep(0.1)

    print('[I] ', 'Disonnected from {}'.format(printer_mac_addp))
    printer.disconnect()
