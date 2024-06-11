from __future__ import annotations

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
    """
    Represents the server data for a client.

    Attributes:
        client_id (int): The client's ID.
        client_id2 (int): Another client ID.
        public_id (int): The public ID.
        private_id (int): The private ID.
    """
    client_id: int = 0
    client_id2: int = 0
    public_id: int = 0
    private_id: int = 0


@dataclass
class PlayerName:
    """
    Represents the name of a player in the game.

    Attributes:
        name (str): The name of the player.
        font (Font, optional): The font used for displaying the player's name. Defaults to Font.DEFAULT.
        colors (list[int], optional): The colors used for displaying the player's name. Defaults to
            [-1, -1, -1, -1, -1, -1].
        animation (NameAnimation, optional): The animation style for the player's name. Defaults to NameAnimation.NONE.
    """
    name: str
    font: Font = Font.DEFAULT
    colors: list[int] = field(default_factory=([-1] * 6).copy)
    animation: NameAnimation = NameAnimation.NONE


@dataclass
class ScreenDimensions:
    """
    Represents the dimensions of a screen. Nebulous game servers use this to calculate how much surrounding
    data to send to the client.

    Attributes:
        width (int): The width of the screen.
        height (int): The height of the screen.
    """

    width: int
    height: int

    def as_aspect_ratio(self) -> float:
        """
        Calculates the aspect ratio of the screen.

        Returns:
            float: The aspect ratio of the screen.
        """
        smallest = min(self.width, self.height)
        return max(self.width, self.height) / smallest

    @classmethod
    def default(cls) -> ScreenDimensions:
        """
        Returns the default screen dimensions.

        Returns:
            ScreenDimensions: The default screen dimensions.
        """
        return cls(1920, 1080)


@dataclass
class ClientConfig:
    """
    Represents the client configuration for the game. All fields have default values, allowing you to
    set only specific options for the client. E.g `ClientConfig(mayhem_mode=True, alias="Blub")`.

    Attributes:
        game_mode (GameMode): The game mode.
        game_difficulty (GameDifficulty): The game difficulty.
        game_id (int): The game ID.
        online_mode (OnlineStatus): The online status.
        mayhem_mode (bool): Indicates if mayhem mode is enabled.
        skin (Skin): The main skin.
        skin2 (Skin): The secondary skin.
        eject_skin (int): The eject skin.
        alias (str): The player's alias.
        alias_font (Font): The font for the alias.
        alias_colors (list[int]): The colors for the alias.
        alias_anim (NameAnimation): The animation for the alias.
        hat_type (int): The hat type.
        halo_type (int): The halo type.
        blob_color (int): The color of the blob.
        pet1 (int): The first pet.
        pet2 (int): The second pet.
        pet1_name (str): The name of the first pet.
        pet2_name (str): The name of the second pet.
        custom_skin (int): The custom skin.
        custom_skin2 (int): The custom secondary skin.
        custom_pet (int): The custom pet.
        custom_pet2 (int): The custom secondary pet.
        custom_particle (int): The custom particle.
        particle_type (int): The particle type.
        level_colors (list[int]): The colors for the levels.
        skin_interpolation_rate (float): The skin interpolation rate.
        split_multiplier (SplitMultiplier): The split multiplier.
        log_chat (bool): Indicates if chat logging is enabled.
        chat_log_encoding (str): The encoding for the chat log.
        chat_log_size (int): The size of the chat log.
        log_level (int): The log level.
        screen (ScreenDimensions): The screen dimensions.
    """
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
    screen: ScreenDimensions = field(default_factory=ScreenDimensions.default)


class ClientState(Enum):
    """
    Represents the state of the client connection.

    Attributes:
        CONNECTING (int): The client is in the process of connecting.
        CONNECTED (int): The client is connected.
        DISCONNECTING (int): The client is in the process of disconnecting.
        DISCONNECTED (int): The client is disconnected.
    """
    CONNECTING = 0
    CONNECTED = 1
    DISCONNECTING = 2
    DISCONNECTED = 3


__all__ = ["ServerData", "ClientState", "ClientConfig", "ScreenDimensions", "PlayerName"]
