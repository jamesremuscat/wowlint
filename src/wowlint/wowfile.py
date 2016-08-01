from construct import Bytes, MetaArray, Padding, PascalString, Probe, Struct, UBInt8

# ===============================================================================
# /*
#    * Rough structure of a .wsg file:
#    *
#    * === HEADER ===
#    * WoW File
#    *   [junk byte]
#    * Song words
#    *   [0x13 - 0x37 junk bytes]
#    *   [# of blocks in file]
#    *   [0x0 0x0 0x0]
#    *   [0xFF 0xFF]
#    *   [0x3E - 0x41 junk bytes]
#    * CSongDoc::CBlock
#    *   [BLOCKS - see below]
#    *   [Byte count of author]
#    * Author
#    *   [Byte count of copyright]
#    * Copyright
#    *   [LICENSEFLAG]
#    *   [0x0 0x0 0x0]
#    * [EOF]
#    *
#    * === LICENSEFLAG ===
#    * 0 - Covered by CCL
#    * 1 - Author's explicit permission
#    * 2 - Public Domain
#    * 3 - Copyright Expired
#    * 4 - Other
#    * === BLOCKS ===
#    *   [# of lines in block]
#    *   [0x0 0x0 0x0]
#    *   [LINES - see below]
#    *   [BLOCKTYPE]
#    *   [0x0 0x0 0x0]
#    *
#    * Two adjacent blocks will have two bytes of "junk" between them.
#    *
#    * === BLOCKTYPE ===
#    * 0 - verse
#    * 1 - chorus
#    * 2 - bridge
#    *
#    * === LINES ===
#    *   [# of bytes in line]
#    *   Line text
#    *   [LINETYPE]
#    *
#    * === LINETYPE ===
#    * 0 - normal
#    * 1 - minor words


Line = Struct(
    "line",
    PascalString("text"),
    UBInt8("type")
)

Block = Struct(
    "block",
    Padding(2),
    UBInt8("linecount"),
    Padding(3),
    MetaArray(lambda ctx: ctx.linecount, Line),
    UBInt8("blocktype"),
    Padding(3)
)

Song = Struct(
    "song",
    Padding(56),
    UBInt8("blockcount"),
    Padding(23),
    MetaArray(lambda ctx: ctx.blockcount, Block),
    PascalString("author"),
    PascalString("copyright"),
    UBInt8("licenseflag"),
    Padding(3)
)

fi = open("test.wsg", "rb")
print Song.parse(fi.read())
