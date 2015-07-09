import collections
from glob import iglob
import io
import os
import pkgutil
import random
import sys

import pydub

class Instrument:
    def __init__(self, name, *,
                 files=None,
                 glob=None,
                 min_length=1000,
                 max_length=1500,
                 min_notes=4,
                 max_polyphony=3,
                 min_pulse_interval=100,
                 max_pulse_interval=500,
                 volume_adjustment=0):
        self._files = files
        self._glob = glob
        self.name = name
        self.min_length = min_length
        self.max_length = max_length
        self.min_notes = min_notes
        self.max_polyphony = max_polyphony
        self.min_pulse_interval = min_pulse_interval
        self.max_pulse_interval = max_pulse_interval
        self._volume_adjustment = volume_adjustment

        self._samples = None

    def __repr__(self):
        return '<Instrument {s.name}>'.format(s=self)

    @property
    def samples(self):
        if self._samples is None:
            if self._files:
                audio_segments = (
                    pydub.AudioSegment.from_file(
                        io.BytesIO(
                            pkgutil.get_data('pchyme', os.path.join('sounds', name))
                        ),
                        format='flac',
                    )
                    for name in self._files)
            elif self._glob:
                audio_segments = (pydub.AudioSegment.from_file(path, format='flac') for path in self._glob)
            self._samples = tuple(segment + self._volume_adjustment for segment in audio_segments)
        return self._samples

    @property
    def longest_sample(self):
        return max(self.samples, key=len)

    def jingle(self, *, print_debug_info=False, seed=None):
        r = random.Random()
        if seed is not None:
            r.seed(seed)

        length = r.randrange(self.min_length, self.max_length)
        pulse_interval = min(r.randrange(self.min_pulse_interval, self.max_pulse_interval),
                             length - 1)
        pulses = range(0, length, pulse_interval)
        note_count_target = len(pulses)
        note_count_standard_deviation = (length / self.min_pulse_interval -
                                         length / self.max_pulse_interval)
        note_count = max(self.min_notes,
                         int(r.gauss(note_count_target, note_count_standard_deviation)))

        buckets = {time: collections.deque(maxlen=self.max_polyphony)
                   for time in range(0, length, pulse_interval)}
        for _ in range(note_count):
            time, bucket = r.choice(list(buckets.items()))
            sample = r.choice(self.samples)
            if sample not in bucket:
                bucket.append(sample)

        if print_debug_info:
            print('"{}" {:.2}s {} with {} buckets'
                      .format(seed, length/1000, self.name, len(buckets)),
                  file=sys.stderr)

        canvas = pydub.AudioSegment.silent(duration=length + len(self.longest_sample))
        for time, bucket in buckets.items():
            for sample in bucket:
                canvas = canvas.overlay(sample, position=time)
        canvas = canvas.strip_silence(silence_thresh=-70, padding=250)
        return canvas


high = Instrument(
    'high',
    files=[
        'high1.flac',
        'high2.flac',
        'high3.flac',
        'high4.flac',
        'high5.flac',
        'high6.flac',
    ],
    min_pulse_interval=130,
    volume_adjustment=-3,
)
metal = Instrument(
    'metal',
    files=[
        'metal1.flac',
        'metal2.flac',
        'metal3.flac',
        'metal4.flac',
        'metal5.flac',
    ],
    min_pulse_interval=200,
    volume_adjustment=-5,
)
rhodes = Instrument(
    'rhodes',
    files=[
        'rhodes1.flac',
        'rhodes2.flac',
        'rhodes3.flac',
        'rhodes4.flac',
        'rhodes5.flac',
        'rhodes6.flac',
        'rhodes7.flac',
        'rhodes8.flac',
        'rhodes9.flac',
    ],
    min_pulse_interval=180,
    volume_adjustment=-1,
)
tiny = Instrument(
    'tiny',
    files=[
        'tiny1.flac',
        'tiny2.flac',
        'tiny3.flac',
        'tiny4.flac',
        'tiny5.flac',
        'tiny6.flac',
    ],
    min_pulse_interval=120,
)
tuna = Instrument(
    'tuna',
    files=[
        'tuna1.flac',
        'tuna2.flac',
        'tuna3.flac',
        'tuna4.flac',
        'tuna5.flac',
    ],
    min_length=1500,
    max_length=3000,
    min_notes=3,
    max_polyphony=2,
    min_pulse_interval=1000,
    max_pulse_interval=4000,
    volume_adjustment=-3,
)
wood = Instrument(
    'wood',
    files=[
        'wood1.flac',
        'wood2.flac',
        'wood3.flac',
        'wood4.flac',
        'wood5.flac',
        'wood6.flac',
    ],
)
