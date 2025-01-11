import mido

def write_lyrics(lyrics, title, artist, lyric_filename):
    with open(lyric_filename, "w", encoding="latin-1") as f:
        f.write(f"{title}\n")
        f.write(f"{artist}\n\n")
        for line in lyrics:
            f.write(f"{line}\n")

def write_cursor(timestamps, ticks_per_beat, cursor_filename):
    with open(cursor_filename, "wb") as f:
        previous_absolute_timestamp = 0
        for delta_time in timestamps:
            absolute_timestamp = previous_absolute_timestamp + delta_time
            absolute_timestamp /= (ticks_per_beat / 24)
            f.write(struct.pack("<H", int(absolute_timestamp)))
            previous_absolute_timestamp = absolute_timestamp

def extract_from_kar(kar_filename, midi_filename, lyric_filename, cursor_filename):
    midi = mido.MidiFile(kar_filename)

    # Extract ticks per beat
    ticks_per_beat = midi.ticks_per_beat

    # Extract lyrics and cursor timestamps
    lyrics = []
    timestamps = []
    title = ""
    artist = ""

    for track in midi.tracks:
        absolute_time = 0
        for msg in track:
            if msg.type == 'meta':
                absolute_time += msg.time
                if msg.type == 'text':
                    if msg.text.startswith("@T"):
                        if not title:
                            title = msg.text[2:]
                        else:
                            artist = msg.text[2:]
                    else:
                        continue
                elif msg.type == 'lyrics':
                    timestamps.append(msg.time)
                    lyrics.append(msg.text)

    # Write extracted data to files
    write_lyrics(lyrics, title, artist, lyric_filename)
    write_cursor(timestamps, ticks_per_beat, cursor_filename)

    # Save the MIDI file without karaoke track
    midi.save(midi_filename)
    print(f"บันทึกไฟล์ .mid, .lyr, และ .cur เสร็จสิ้น: {midi_filename}, {lyric_filename}, {cursor_filename}")

extract_from_kar("input.kar", "extracted_song.mid", "extracted_song.lyr", "extracted_song.cur")
