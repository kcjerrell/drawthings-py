from __future__ import annotations

import wave
from pathlib import Path
from typing import cast

import fpzip
import numpy as np


class AudioBuffer:
    """
    Represents audio data with left and right channels.
    """

    length: int
    """Number of audio frames"""
    channels: int
    """Number of audio channels (always 2 for stereo)"""
    data: np.ndarray
    """Audio data as a numpy array of shape (frames, channels)"""
    sample_rate: int
    """Sample rate of the audio"""

    def __init__(self, frames: int, sample_rate: int = 48000, channels: int = 2):
        self.length = frames
        self.channels = channels
        self.sample_rate = sample_rate
        self.data = np.zeros((frames, channels), dtype=np.float32)

    @classmethod
    def from_tensor(cls, data: bytes) -> "AudioBuffer":
        """
        Create an AudioBuffer from a tensor byte string.

        Args:
            data: Byte string containing audio data in Draw Things format

        Returns:
            AudioBuffer with the decoded audio data
        """
        if len(data) < 68:
            raise ValueError(
                f"Audio data is too short: expected at least 68 bytes, got {len(data)}"
            )

        header = np.frombuffer(data, dtype="<u4", count=17)
        length = cast(int, header[6])
        channels = 2  # always stereo for now

        audio = data[68:]

        try:
            if audio.startswith(b"fpy"):
                decompressed: bytes | None = cast(bytes | None, fpzip.decompress(audio))  # pyright: ignore[reportUnknownMemberType]
                if decompressed is not None:
                    audio = decompressed
        except Exception:
            pass

        samples = np.frombuffer(audio, dtype=np.float32)

        if len(samples) != length * channels:
            raise ValueError(
                f"Expected {length * channels} samples, got {len(samples)}"
            )

        # Draw Things stores all left samples followed by all right samples.
        left = samples[:length]
        right = samples[length:]

        buffer = cls(length, channels)
        buffer.data[:, 0] = left
        buffer.data[:, 1] = right

        return buffer

    def to_file(self, file_path: str | Path) -> None:
        """
        Write the audio data to a WAV file.

        Args:
            file_path: Path to the output WAV file
        """
        pcm = np.clip(self.data, -1.0, 1.0)
        pcm = (pcm * 32767).astype(np.int16)

        with wave.open(str(file_path), "wb") as wav:
            wav.setnchannels(self.channels)
            wav.setsampwidth(2)
            wav.setframerate(self.sample_rate)
            wav.writeframes(pcm.tobytes())

    @property
    def duration(self) -> float:
        """the audio duration in seconds"""
        return self.length / self.sample_rate

    @property
    def left(self) -> np.ndarray:
        return self.data[:, 0]

    @property
    def right(self) -> np.ndarray:
        return self.data[:, 1]


def get_sample_rate(audio_frames: int, video_frames: int, fps: float) -> int:
    # there are only two possible sample rates 48000 and 24000
    # and in both cases the fps is 25
    duration = video_frames / fps
    samples_per_second = audio_frames / duration
    if samples_per_second > 36000:
        return 48000
    return 24000
