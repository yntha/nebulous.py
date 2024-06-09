import logging
import time
from dataclasses import dataclass, field
from enum import Enum

from nebulous.game.enums import (
    Font,
    GameDifficulty,
    GameMode,
    NameAnimation,
    OnlineStatus,
    Skin,
    SplitMultiplier,
)


@dataclass
class ServerData:
    client_id: int = 0
    client_id2: int = 0
    public_id: int = 0
    private_id: int = 0


@dataclass
class PlayerName:
    name: str
    font: Font = Font.DEFAULT
    colors: list[int] = field(default_factory=([-1] * 6).copy)
    animation: NameAnimation = NameAnimation.NONE


@dataclass
class ClientConfig:
    game_mode: GameMode = GameMode.FFA
    game_difficulty: GameDifficulty = GameDifficulty.EASY
    game_id: int = -1
    online_mode: OnlineStatus = OnlineStatus.ONLINE
    mayhem_mode: bool = False
    skin: Skin = Skin.MISC_NONE
    skin2: Skin = Skin.MISC_NONE
    eject_skin: int = -1
    alias: str = "Blob " + hex(int(time.time() * 1000) & 0xFFFF)[2:].upper()
    alias_font: Font = Font.DEFAULT
    alias_colors: list[int] = field(default_factory=([-1] * 6).copy)
    alias_anim: NameAnimation = NameAnimation.NONE
    hat_type: int = -1
    halo_type: int = 0
    blob_color: int = 0xFF1A69E1
    pet1: int = -1
    pet2: int = -1
    pet1_name: str = ""
    pet2_name: str = ""
    custom_skin: int = 0
    custom_skin2: int = 0
    custom_pet: int = 0
    custom_pet2: int = 0
    custom_particle: int = 0
    particle_type: int = -1
    level_colors: list[int] = field(default_factory=([0x77] * 5).copy)
    skin_interpolation_rate: float = 0.0
    split_multiplier: SplitMultiplier = SplitMultiplier.X8
    log_chat: bool = True
    chat_log_encoding: str = "utf-8"
    chat_log_size: int = 1000
    log_level: int = logging.INFO


class ClientState(Enum):
    CONNECTING = 0
    CONNECTED = 1
    DISCONNECTING = 2
    DISCONNECTED = 3


__all__ = ["ServerData", "ClientState"]
