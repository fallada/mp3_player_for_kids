# Mp3 Player For Kids #

This music-player for kids can be controlled by my one and a half year old daughter all by herself. It is also unexpensive and the code is in Python, so it can be easily adjusted to your own needs.

Video:

[![MP3 Player For Kids on YouTube](https://img.youtube.com/vi/5Fa26CWGCNk/0.jpg)](https://www.youtube.com/watch?v=5Fa26CWGCNk)

You will need these parts:

 * ESP8266 WeMos D1 Mini WIFI 4M Bytes
 * YX5300 UART Control Serial MP3 Music Player Module
 * RC522 MFRC-522 Card Read Antenna RF Module RFID Reader
 * PAM8403 5V 2 Channel USB Power Audio Amplifier

For the "music-chips" I used second hand poker-chips and put [NFC Sticker-Tags] on them. Also for noise-reduction you will need two 1000μF (35V) capacitors. 

[NFC Sticker-Tags]: https://www.amazon.de/gp/product/B01HZWA0Z0/ref=as_li_tl?ie=UTF8&camp=1638&creative=6742&creativeASIN=B01HZWA0Z0&linkCode=as2&tag=fallada-21&linkId=9c814fe6c1cf8baeb9f46970a6b323f9

## Put Micropython on the Wemos ##

You can download Micropython for the module [here][micropython download]. Instructions for the deployment you find [here][micropython install]. For me this line worked well:

    sudo esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp8266-20171101-v1.9.3.bin

[micropython download]: https://micropython.org/download/#esp8266
[micropython install]: http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html#deploying-the-firmware

You can now connect to the Wemos like this:

    sudo picocom /dev/ttyUSB0 -b115200
    >>> print("hello world")

## Activate WebREPL ##

To connect the Wemos Module to your WiFi you type this:

    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('ssid', 'password')

If you like to upload your code with a browser, you should activate WebREPL:

    import webrepl_setup

Now you can connect with the [WebREPL-Client].

[WebREPL-Client]: https://github.com/micropython/webrepl/archive/master.zip

## Connect the Modules ##

This is how you connect the the Serial MP3 Player with the Wemos D1 Mini:

    D1 Mini <-> MP3-Player
    
    TX <------------->  RX
    RX <------------->  TX
    5V <-------------> VCC
    G  <-------------> GND

Connect the card reader like this:

    D1 Mini <---> MFRC522
    
    D5  <---------->  SDA
    D3  <---------->  SCK
    D4  <----------> MOSI
    D2  <----------> MISO
    G   <---------->  GND
    D1  <---------->  RST
    3v3 <----------> 3.3V

## Audio Amplifier ##

Connecting the PAM8403 is pretty straightforward. You connect "Power +" with the power supply from the Wemos. You can choose the 5V connector or 3.3V. PAM8403 is not choosy. The sound input is labled "L/G/R". "rout/lout" is the output and we connect it with the speaker boxes.

## Denoising ##

At first I could hear a regular tac-tac-tac-sound. Two 1000μF capacitors helped. I put one very close to the power supply between 5V and G at the Wemos. The second one I connected with its long leg to "power +" at the PAM8403 and with its short leg to Ground ("G" at the Wemos D1 Mini).

## MP3-Directory ##

You need to save the files in the directory exactly like [documented by catalex]: /01/001xxx.mp3

[documented by catalex]: http://geekmatic.in.ua/pdf/Catalex_MP3_board.pdf

## Blog ##

More details and pictures [on my blog].

[on my blog]: https://allgaier.org/category/microcontroller.html