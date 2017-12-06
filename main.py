import mp3, readerplayer, webplayer, time


def main():
    try:
        mp3.set_volume(15)
        web_player = webplayer.WebPlayer(mp3)
        reader_player = readerplayer.ReaderPlayer(mp3)
        while True:
            web_player.do()
            reader_player.do()
    except Exception as e:
        f = open("error.log", "w")
        f.write(str(e))
        f.close()
        raise

if __name__ == '__main__':
    main()
        
