# tinyprint
Printing from linux on cheap portable thermal printers

## Scope
This project is aimed to reverse engineer the protocol used by cheap portable thermal printers such 
[this](https://www.amazon.it/Stampante-Fotografica-Istantanea-Portatile-Bluetooth/dp/B09W2KLS2J)

These printers have proprietary apps for android line Tinyprint or iprint

## Steps
### 1. Sniff the bluetooth traffic between the android app and the printer and create example traffic files
*This work has aleready been done in repository [lisp3r/bluetooth-thermal-printer](https://github.com/lisp3r/bluetooth-thermal-printer) and we have the recording of 2 working prints of different images:
 - [RFID_METKA](<Reverse Engineering/Sniffed data/rfid-metka-picture.pichex>)
 - [black_knight](<Reverse Engineering/Sniffed data/black_knight_pic.pichex_bkp>)

### 2. Write a working program that prints from the recorded files
In order to reverse engineer the meaning of the commands sent to the printer we need a program that sends the recording file to the printer.

This is performed by [print_from_hex.py](print_from_hex.py)

### 3. Tweak the files in order to understand the record structure
There seems to be a standard record format:

```5178bf000e000c8101810a8108815d817f7e8101e3ff```

(in hex)

there is starting sequence: `5178` (first 2 bytes)

and an ending byte: `ff`

In this way you can divide the message into single records (let's call them rows)

This is a piec of a message wth different rows:
```
5178a2003000aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa4dff
5178bf000600108171817f7e33ff
5178a2003000aa2a545555555555555555555555555551555555555555555555555555555555555555555555555555555555555555558fff
5178bf000a000e810181088167817f7fc3ff
5178a2003000aa0aaaa8aaaaaaaaaaaaaaaaaaaaaaaaa8aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa2a75ff
5178bf000e000c8101810a8108815d817f7e8101e3ff

5178a2003000aa8aaaa85255555555555555555555b55455555555555555555555555555555555555555555555555555555555a5aa0af7ff
5178a20030000020000200000000000000000000a0aeaa0800a89492029000528a0000000000000000000000000000000000001000a0e9ff
5178a2003000aa8aaaa8aaaaaaaaaaaaaaaaaaaa4aab5d6b5559adb4ad36a9d675adaaaaaaaaaaaaaaaaaaaaaaaaaaaa4aa95282940a56ff
5178a20030000020000200000000000000000000905db75600b2bb6f036882adab4b00000000000000000000000000001004042942200eff
```