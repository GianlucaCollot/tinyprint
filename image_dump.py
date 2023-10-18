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
        o_file = sys.argv[2]
    except IndexError:
        print(f'[E]', 'Usage: {sys.argv[0]} [wireshark_json_dump]')
        exit(1)

    image = image_from_wireshark_dump(i_file)

    from textwrap import wrap

    image = image.split('ff5178')
    # bytebuf = bytes.fromhex(image)
        #"windows-1252"
        #'ASCII')
        #  #wrap(image, 112)
    # Start to write an image
    print('[I] ', 'Start writing image')
    with open(o_file, 'w') as out_file:
        for l in image:
            print(l)
            out_file.write(l)
        
            out_file.write('\n')

    

