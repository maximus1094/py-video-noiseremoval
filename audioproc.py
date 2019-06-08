import os
import shutil
import sox # Audio
import moviepy.editor as mp # Video

TEMP = './temp/'
ORIGINAL_VIDEOS = './Videos/'
NEW_VIDEOS = './NewVideos/'

def create_folders():
    if not os.path.isdir('temp'):
        os.mkdir('temp')

    if not os.path.isdir('NewVideos'):
        os.mkdir('NewVideos')

def get_audio_and_noise(load_path, audio_path, noise_path, duration):
    audio = mp.AudioFileClip(load_path)
    audio.write_audiofile(audio_path)

    noise_sample = audio.set_end(duration)
    noise_sample.write_audiofile(noise_path)
    
    return True

def reduce_noise(input_path, noise_path, output_path):
    prof_path = TEMP + 'noise.prof'

    tfm = sox.Transformer()
    tfm.noiseprof(noise_path, prof_path)
    tfm.noisered(prof_path)
    tfm.build(input_path, output_path)

def replace_audio(video_path, audio_path, save_path):
    video = mp.VideoFileClip(video_path)
    audio = mp.AudioFileClip(audio_path)

    new_video = video.set_audio(audio.set_duration(video.duration))
    new_video.write_videofile(save_path)

# MAIN
if __name__ == "__main__":
    create_folders()
    
    noise_sample_duration = 3
    video_extensions = ['.mp4']
    for i, video in enumerate(os.listdir(ORIGINAL_VIDEOS)):
        name, ext = os.path.splitext(video)

        if ext in video_extensions:
            orig_vid_path = ORIGINAL_VIDEOS + video
            orig_audio_path = TEMP + 'original_audio.wav'
            noise_sample_path = TEMP + 'noise_sample.wav'
            noiseless_audio_path = TEMP + 'audio_noiseless.wav'
            noiseless_video_path = NEW_VIDEOS + name + '_new.mp4'
            
            get_audio_and_noise(orig_vid_path, orig_audio_path, noise_sample_path, noise_sample_duration)
            reduce_noise(orig_audio_path, noise_sample_path, noiseless_audio_path)
            replace_audio(orig_vid_path, noiseless_audio_path, noiseless_video_path)

    shutil.rmtree(TEMP)