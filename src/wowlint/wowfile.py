from construct import MetaArray, Padding, PascalString, Struct, UBInt8
from construct.core import Adapter
from enum import Enum


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


class LineType(Enum):
    NORMAL = 0
    MINOR = 1


class BlockType(Enum):
    VERSE = 0
    CHORUS = 1
    BRIDGE = 2


class LicenseType(Enum):
    CCL = 0
    AUTHOR_EXPLICIT_PERMISSION = 1
    PUBLIC_DOMAIN = 2
    COPYRIGHT_EXPIRED = 3
    OTHER = 4


class EnumAdapter(Adapter):
    def __init__(self, enumClass, subcon):
        super(Adapter, self).__init__(subcon)
        self.enumClass = enumClass

    def _encode(self, obj, context):
        return obj.value

    def _decode(self, obj, context):
        return self.enumClass(obj)


Line = Struct(
    "line",
    PascalString("text"),
    EnumAdapter(LineType, UBInt8("type"))
)

Block = Struct(
    "block",
    Padding(2),
    UBInt8("linecount"),
    Padding(3),
    MetaArray(lambda ctx: ctx.linecount, Line),
    EnumAdapter(BlockType, UBInt8("type")),
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
    EnumAdapter(LicenseType, UBInt8("licensetype")),
    Padding(3)
)
