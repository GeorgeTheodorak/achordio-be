# maj: Major chord
# min: Minor chord
# dim: Diminished chord
# aug: Augmented chord
# sus2: Suspended 2nd chord
# sus4: Suspended 4th chord
# maj7: Major 7th chord
# min7: Minor 7th chord
# 7: Dominant 7th chord
# dim7: Diminished 7th chord
# aug7: Augmented 7th chord
# m7b5: Half-diminished 7th chord (minor 7th flat 5)


NOTES = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G'
]

NOTATIONS = [
    '',  # base note
    'maj', 'min', 'dim', 'aug', 'sus2', 'sus4',
    'maj7', 'min7', '7', 'dim7', 'aug7', 'm7b5'
]


def isValidChordNotion(chordToCheck: str):
    for note in NOTES:
        for notation in NOTATIONS:
            noteNotation = note + notation
            if chordToCheck == noteNotation:
                return True
    return False
