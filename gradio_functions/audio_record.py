from call_to_text.record import AudioRecorder

audio_recorder = AudioRecorder()


def start_or_resume_recording():
    """Starts or resumes an audio recording session.

    Returns:
        str: Message indicating the status of the recording (started or resumed).
    """
    return audio_recorder.start_or_resume_recording()


def pause_recording():
    """Pauses the current audio recording session.

    Returns:
        str: Message indicating that the recording has been paused.
    """
    return audio_recorder.pause_recording()


def stop_recording():
    """Stops the current audio recording session and saves the recording.

    Returns:
        str: Message indicating the recording has been stopped and saved.
    """
    return audio_recorder.stop_recording()
