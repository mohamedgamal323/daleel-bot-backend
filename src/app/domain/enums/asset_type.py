from enum import Enum


class AssetType(str, Enum):
    DOCUMENT = "document"
    LINK = "link"
    AUDIO = "audio"
    IMAGE = "image"
