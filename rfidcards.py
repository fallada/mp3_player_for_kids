import ujson

class RfidCards:
    
    def __init__(self):
        self.all_cards = []
        self.FILE_NAME = "rfidcards.json"
        self._load_cards()
        
    def _load_cards(self):
        try:
            f = open(self.FILE_NAME)
        except OSError:
            #no file yet
            self._dump_cards()
            f = open(self.FILE_NAME)
        self.all_cards = ujson.loads(f.read())
        f.close()
    
    def _dump_cards(self):
        f = open(self.FILE_NAME, "w")
        f.write(ujson.dumps(self.all_cards))
        f.close()
        
    def add_card(self, card):
        self.all_cards.append(card)
        self._dump_cards()
        self._load_cards()  #just to see bugs early
        
    def card_index(self, card):
        try:
            index = self.all_cards.index(card)
        except ValueError:
            # add new card
            self.add_card(card)
            index = self.all_cards.index(card)
        return index

    def next_card_index(self):
        return len(self.all_cards)