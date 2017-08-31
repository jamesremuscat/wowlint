# -*- coding: utf-8 -*-
import io
import os
import sys

from wowlint.wowfile import Resource, BlockType


def song_to_text(song):
    result = u''
    verse_counter = 1
    bridge_counter = 1
    chorus_counter = 1

    for block in song.content.block:
        if block.type == BlockType.VERSE:
            result += "Verse {}\n".format(verse_counter)
            verse_counter += 1
        elif block.type == BlockType.CHORUS:
            result += "Chorus {}\n".format(chorus_counter)
            chorus_counter += 1
        elif block.type == BlockType.BRIDGE:
            result += "Bridge {}\n".format(bridge_counter)
            bridge_counter += 1

        for line in block.line:
            result += line.text
            result += '\n'

        result += '\n'

    if song.content.author or song.content.copyright:
        result += 'CCLI Song # 0 FOR PP IMPORT\n'

        if song.content.author:
            result += song.content.author
            result += '\n'
        if song.content.copyright:
            result += u'© {}\n'.format(song.content.copyright)
            result += '\n'

    return result


def liturgy_to_text(liturgy):
    result = u''
    for line in liturgy.content.line:
        result += line.text
        result += '\n'
    return result


_RESOURCE_MAPPING = {
    'Song Words': song_to_text,
    'Liturgy': liturgy_to_text
}


def main():
    for wowfile in sys.argv[1:]:
        with open(wowfile, 'rb') as f:
            resource = Resource.parse(f.read())
            outfile = '{}.txt'.format(os.path.splitext(wowfile)[0])
            print '{} ({}) => {}'.format(wowfile, resource.filetype, outfile)

            if resource.filetype in _RESOURCE_MAPPING:
                as_text = _RESOURCE_MAPPING[resource.filetype](resource)
                with io.open(outfile, 'w', encoding='utf-8') as of:
                    of.write(as_text)
            else:
                print "Unknown file type {}".format(resource.filetype)


if __name__ == '__main__':
    main()
