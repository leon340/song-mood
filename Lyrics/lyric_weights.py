from difflib import SequenceMatcher


def getWeightMap(lyrics):
    lines = lyrics.split("\n")
    while "" in lines:
        lines.remove("")
    total_lines = len(lines)
    # print(SequenceMatcher(None, "Hey I'm feelin like a god", "Hey I'm feeling kinda like a god").ratio())
    for l in lines:
        print(l)
    print(total_lines)
    return None

