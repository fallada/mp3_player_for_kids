import mp3, time, readerplayer


def main():
    mp3.set_volume(15)
    reader_player = readerplayer.ReaderPlayer(mp3)
    while True:
        reader_player.do()
        time.sleep(0.1) # give the cpu some time for other stuff
        
if __name__ == '__main__':
    main()
        
