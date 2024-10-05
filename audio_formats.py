from dataclasses import dataclass

@dataclass
class AudioFormat:
    name: str
    extension: str
    ydl_format: str
    ffmpeg_codec: str

AUDIO_FORMATS = [
    AudioFormat("M4A", "m4a", "bestaudio[ext=m4a]/best", "aac"),
    AudioFormat("MP3", "mp3", "bestaudio/best", "libmp3lame"),
    AudioFormat("WAV", "wav", "bestaudio/best", "pcm_s16le"),
    AudioFormat("FLAC", "flac", "bestaudio/best", "flac"),
    AudioFormat("AAC", "aac", "bestaudio/best", "aac"),
    AudioFormat("OPUS", "opus", "bestaudio/best", "libopus"),
    AudioFormat("VORBIS", "ogg", "bestaudio/best", "libvorbis"),
    AudioFormat("ALAC", "m4a", "bestaudio/best", "alac"),
    AudioFormat("AC3", "ac3", "bestaudio/best", "ac3"),
    AudioFormat("DTS", "dts", "bestaudio/best", "dts"),
]

def get_format_by_index(index):
    if 1 <= index <= len(AUDIO_FORMATS):
        return AUDIO_FORMATS[index - 1]
    return AUDIO_FORMATS[0]

def get_format_names():
    return [f"{i+1}. {format.name}" for i, format in enumerate(AUDIO_FORMATS)]