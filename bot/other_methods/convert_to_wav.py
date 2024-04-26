from pydub import AudioSegment
import os

def convert_to_wav(filename):
    # Load the audio file
    audio = AudioSegment.from_file(filename, format="ogg")

    # Set the output file path and format
    file_name, file_extension = os.path.splitext(filename)
    output_filename = file_name + ".wav"

    # Export the audio file in wav format
    audio.export(output_filename, format="wav")

    return output_filename