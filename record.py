#!/usr/bin/env python3
"""Create a recording with arbitrary duration.

PySoundFile (https://github.com/bastibe/PySoundFile/) has to be installed!

"""
import argparse
import tempfile
from Queue import Queue
import sounddevice as sd
import soundfile as sf
from datetime import datetime
import os

recorder_queue = Queue()


class Recorder(object):
    def __init__(self, filename, device_index):
        self.filename = filename
        self.device_index = device_index

        self.file = None
        self.inputStream = None

    @staticmethod
    def query_devices():
        return sd.query_devices()

    def start(self):
        device_info = sd.query_devices(self.device_index, 'input')
        if not device_info:
            print('Could not find device for: {0}'.format(device_index))
            return None

        # soundfile expects an int, sounddevice provides a float:
        samplerate = int(device_info['default_samplerate'])

        def callback(indata, frames, time, status):
            """This is called (from a separate thread) for each audio block."""
            print('Callback {0}'.format(len(indata)))
            if status:
                print(status)
            recorder_queue.put(indata.copy())

        # Make sure the file is opened before recording anything:
        self.file = sf.SoundFile(self.filename, mode='x', samplerate=samplerate,
                                 channels=2, subtype=None)
        self.inputStream = sd.InputStream(samplerate=samplerate, device=self.device_index,
                                          channels=2, callback=callback)

        return True

    def record_until(self,stop_date_time):
        device_info = sd.query_devices(self.device_index, 'input')
        if not device_info:
            print('Could not find device for: {0}'.format(device_index))
            return None

        # soundfile expects an int, sounddevice provides a float:
        samplerate = int(device_info['default_samplerate'])

        q = Queue()

        def callback(indata, frames, time, status):
            """This is called (from a separate thread) for each audio block."""
            if status:
                print(status)
            q.put(indata.copy())

        if os.path.exists(self.filename):
            os.remove(self.filename)

        # Make sure the file is opened before recording anything:
        with sf.SoundFile(self.filename, mode='x', samplerate=samplerate,
                          channels=2, subtype=None) as file:
            with sd.InputStream(samplerate=samplerate, device=self.device_index,
                                channels=2, callback=callback):

                while datetime.now() < stop_date_time:
                    file.write(q.get())

    def loop(self):
        test = recorder_queue.get()
        self.file.write(test)

    def stop(self):
        self.inputStream.close()
        self.file.close()



if __name__ == "__main__":
    def int_or_str(text):
        """Helper function for argument parsing."""
        try:
            return int(text)
        except ValueError:
            return text

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-l', '--list-devices', action='store_true',
        help='show list of audio devices and exit')
    parser.add_argument(
        '-d', '--device', type=int_or_str,
        help='input device (numeric ID or substring)')
    parser.add_argument(
        '-r', '--samplerate', type=int, help='sampling rate')
    parser.add_argument(
        '-c', '--channels', type=int, default=1, help='number of input channels')
    parser.add_argument(
        'filename', nargs='?', metavar='FILENAME',
        help='audio file to store recording to')
    parser.add_argument(
        '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
    args = parser.parse_args()

    try:


        if args.list_devices:
            print(sd.query_devices())
            parser.exit(0)
        if args.samplerate is None:
            device_info = sd.query_devices(args.device, 'input')
            # soundfile expects an int, sounddevice provides a float:
            args.samplerate = int(device_info['default_samplerate'])
        if args.filename is None:
            args.filename = tempfile.mktemp(prefix='rec_unlimited_',
                                            suffix='.wav', dir='')
        q = Queue()


        def callback(indata, frames, time, status):
            """This is called (from a separate thread) for each audio block."""
            if status:
                print(status)
            q.put(indata.copy())


        # Make sure the file is opened before recording anything:
        with sf.SoundFile(args.filename, mode='x', samplerate=args.samplerate,
                          channels=args.channels, subtype=args.subtype) as file:
            with sd.InputStream(samplerate=args.samplerate, device=args.device,
                                channels=args.channels, callback=callback):
                print('#' * 80)
                print('press Ctrl+C to stop the recording')
                print('#' * 80)
                while True:
                    file.write(q.get())

    except KeyboardInterrupt:
        print('\nRecording finished: ' + repr(args.filename))
        parser.exit(0)
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))
