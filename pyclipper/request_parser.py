import re

from pyclipper.timestamp import VideoTimestamp


class RequestArgumentException(Exception):
    def __init__(self):
        super(RequestArgumentException, self).__init__(
            self, "We need a Video URL, a start time, and an end time."
        )


class ClipperTextMessageParser:
    def __init__(self, body):
        tokens = [token for token in re.split(r"\s", body) if len(token)]
        if len(tokens) < 3:
            raise RequestArgumentException()

        self._video_url = tokens[0]
        self._start = VideoTimestamp(tokens[1]).seconds
        self._end = VideoTimestamp(tokens[2]).seconds

    @property
    def data(self):
        return {
            "video_url": self._video_url,
            "start": self._start,
            "end": self._end
        }