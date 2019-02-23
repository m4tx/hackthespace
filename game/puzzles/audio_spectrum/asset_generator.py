import tempfile
import taglib
from PIL import Image
from pydub import AudioSegment

from vendor.spectrology import convert
from game.utils.images import put_text_on_image, fill_image_with_rgb_noise


def __gen_image(out_path, width, height, text, font_name, font_size):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))

    fill_image_with_rgb_noise(img)
    put_text_on_image(img, text, font_name, font_size, (0, 0, 0, 255))

    img.save(out_path)


def __gen_audio(img_path, wav_file, min_freq, max_freq, pixels_per_second):
    convert(img_path, wav_file, min_freq, max_freq, pixels_per_second,
            44100, False, False)


def __combine_audio(in_path1, in_path2, position, gain) -> AudioSegment:
    sound1 = AudioSegment.from_ogg(in_path1)
    sound2 = AudioSegment.from_wav(in_path2)

    sound2 = sound2.apply_gain(gain)
    return sound1.overlay(sound2, position=position)


def __set_metadata(file_path: str, tags: dict):
    """Save given metadata in the file.

    This function uses pytaglib since pydub does not support some MP3 tags
    (e.g. "comment").

    :param file_path: the path to the file to set tags in
    :param tags: the dictionary of tags to set
    """
    song = taglib.File(file_path)
    for k, v in tags.items():
        song.tags[k] = v
    song.save()


def hide_text_in_audio(input_path, out_path, text, font_name, font_size,
                       min_freq, max_freq, pixels_per_second, audio_position,
                       audio_gain, audio_tags):
    """
    Hide some text in given audio file is a way the text is visible on
    the audio spectrogram.

    :param input_path: the WAV file to put the text into
    :param out_path: output file path without extension (.mp3 and .ogg
        files are created)
    :param text: the text to put in the file
    :param font_name: name of the font to use
    :param font_size: size of the font to use
    :param min_freq: the frequency where the image starts on the spectrogram
    :param max_freq: the frequency where the image ends on the spectrogram
    :param pixels_per_second: number of pixels of the image per audio seconds
    :param audio_position: position of the image in milliseconds since the
        start of the audio file
    :param audio_gain: the gain of the added audio stream (you probably want
        this value to be negative)
    :param audio_tags: tags (metadata) to put in the output files
    """
    with tempfile.NamedTemporaryFile(suffix='.png') as img_file, \
            tempfile.NamedTemporaryFile(suffix='.wav') as wav_file:
        print('Generating image')
        __gen_image(img_file.name, 800, 200, text,
                    font_name, font_size)
        print('Generating audio (this may take a while)')
        __gen_audio(img_file.name, wav_file.name,
                    min_freq, max_freq, pixels_per_second)
        print('Mixing audio')
        output = __combine_audio(input_path, wav_file,
                                 audio_position, audio_gain)
        print('Saving the files')
        output.export(out_path + '.mp3', bitrate='256k', format='mp3')
        output.export(out_path + '.ogg', bitrate='256k', format='ogg')
        print('Saving the metadata')
        __set_metadata(out_path + '.mp3', audio_tags)
        __set_metadata(out_path + '.ogg', audio_tags)
        print('Done!')
