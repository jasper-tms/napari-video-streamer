from pathlib import Path

import dask.array as da
from npimage import VideoStreamer

SUPPORTED_EXTENSIONS = {'mp4', 'mkv', 'avi', 'mov', 'webm'}


def napari_get_reader(path):
    if isinstance(path, list):
        path = path[0]
    if isinstance(path, str):
        ext = Path(path).suffix.lower().lstrip('.')
        if ext in SUPPORTED_EXTENSIONS:
            return reader
    return None


def reader(path):
    if isinstance(path, list):
        path = path[0]
    path = str(path)

    video_stream = VideoStreamer(path, cache_index=True)
    n_frames = video_stream.n_frames
    height, width, channels = video_stream.shape[1:]

    def get_frame(block_info=None):
        frame_idx = block_info[None]['chunk-location'][0]
        return video_stream[frame_idx][None, ...]

    frames = da.map_blocks(
        get_frame,
        chunks=((1,) * n_frames, (height,), (width,), (channels,)),
        dtype='uint8',
    )

    metadata = {
        'fps': video_stream.fps,
        'framerate': video_stream.framerate,
        'duration_seconds': video_stream.duration,
        'n_frames': n_frames,
        'source_path': path,
        '_video_stream': video_stream,
    }

    return [(frames, {
        'rgb': True,
        'contrast_limits': (0, 255),
        'name': Path(path).stem,
        'metadata': metadata,
    }, 'image')]
