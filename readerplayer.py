import mfrc522, rfidcards, time
from machine import Pin

DEBUG = False

def _debug(*args):
    if DEBUG:
        print(*args)


class ReaderPlayer:
    """ Has state (paused, playing, stopped).
         Keeps the state of reader and player in sync without much feebback from the player.
         The User sets the state by placing rfid cards on the reader. Is a card on the reader, the 
         player is playing the corresponding mp3. Is the card removed, the player will pause.
    """
    #STOPPED = 0   #no need yet
    PLAYING = 1 #tag placed on reader
    PAUSED = 2  #no tag on reader
    LED_PIN = 15 #D8
    BUTTON_PIN = 12 #D6
    SPECIAL_CARDS = {
        'end_program': '0xc0c92583',
        #'next_song': '0xc0125e7a',
        'next_unassigned_folder': '0x1206be59', #preview the next folder that is not yet assigned to a card, to 'program' the next tag
        }
    
    def __init__(self, mp3Player):
        self.led = Pin(self.LED_PIN, Pin.OUT)
        self.button = Pin(self.BUTTON_PIN, Pin.IN, Pin.PULL_UP)
        self.button_last_pressed = time.time()
        self.mp3Player = mp3Player
        self.status = None
        self.current_folder = None
        self.pause()
        self.rdr = mfrc522.MFRC522(0, 2, 4, 5, 14)
        self.rfid_cards = rfidcards.RfidCards()

    def song_just_finished(self):
        """ Is true, if a song just finished playing
             The mp3-player returns a specific code, after ending a song.
        """
        uart_return_code = self.mp3Player.uart.readline()
        _debug("uart_return_code", uart_return_code)
        # uart_return_code == b'~\xff\x06=\x00\x00\x12\xfe\xac\xef~\xff\x06=\x00\x00\x12\xfe\xac\xef'
        return uart_return_code and b'\x06=' in uart_return_code 

    def _uid(self, raw_uid):
        return "0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
        
    def get_card_id(self):
        """ Return the UID (Unique Identification Number) assigned to the current card
        """
        (stat, tag_type) = self.rdr.request(self.rdr.REQIDL)
        _debug('rdr.request', stat)
        if stat == self.rdr.OK:
            (stat, raw_uid) = self.rdr.anticoll()
            _debug('anticoll_2', stat)
            if stat == self.rdr.OK:
                return self._uid(raw_uid)
        return None    
    
    def card_still_there(self):
        # still current card? this is veryfast compared to rdr.request()
        stat, raw_uid = self.rdr.anticoll()
        _debug('card still there', stat)
        return stat == self.rdr.OK

    def do(self):
        """ called regularly from the main loop
        """
        try:
            self._do()
        except KeyboardInterrupt:
            # thrown from time to time from the reader...  no idea why.
            return
        
    def _do(self):
        if self.status == self.PLAYING:
            if self.song_just_finished():
                _debug("next")
                self.mp3Player.next()
            if not self.card_still_there():
                self.pause()
                #sometimes pause gets ignored by the player, so lets pause again, can't harm.
                time.sleep(0.1)
                self.pause()
            else:
                if not self.button.value():
                    #button pressed
                    if time.time() - self.button_last_pressed >= 2:
                        #mind. 2 Sekunde seit letztem mal
                        self.mp3Player.next()
                        self.button_last_pressed = time.time()
                return

        elif self.status == self.PAUSED:
            #resume folder or play new one
            #also check special cards
            uid = self.get_card_id()
            _debug("uid", uid)
            if not uid:
                #still no card, still paused
                #auskommentiert wegen webplayer
                #self.pause() #sometimes pause gets ignored by the player, so lets pause again, can't harm.
                return
            if uid == self.SPECIAL_CARDS["end_program"]:
                self.mp3Player.stop()
                raise SystemExit('Stop program')
            elif uid == self.SPECIAL_CARDS["next_unassigned_folder"]:
                self.play_folder(self.rfid_cards.next_card_index())
                return
            folder_id = self.rfid_cards.card_index(uid)
            _debug("folder_id", folder_id)
            if folder_id == self.current_folder:
                _debug("same folder", folder_id)
                #user put same card back
                self.resume()
            else: #new card
                self.play_folder(folder_id)
                _debug("new card", folder_id)
                
    def play_folder(self, folder_id):
        #folder_id starting from zero, mp3 player from one
        self.mp3Player.play_folder(folder_id + 1)
        _debug("play_folder", folder_id)
        self.status = self.PLAYING
        self.led.on()
        self.current_folder = folder_id
        
    def resume(self):
        self.mp3Player.resume()
        _debug("resume")
        self.status = self.PLAYING
        self.led.on()
        
    def pause(self):
        self.mp3Player.pause()
        _debug("pause")
        self.status = self.PAUSED
        self.led.off()    
