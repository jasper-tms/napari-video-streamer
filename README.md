# napari-video-streamer

A [napari](https://napari.org) plugin for lazily streaming frames from a video file. By only loading the specific frames that you're actively trying to view in napari, load times are fast and memory usage stays low, even for extremely long videos.

## How it works

We connect to the video file via a [`npimage.VideoStreamer`](https://github.com/jasper-tms/npimage) and route data to napari through a Dask array with one chunk per frame. Each chunk (one frame) is read from the video file upon demand via napari making a call to `dask.array.map_blocks`.

Note that requesting a new frame is fast (almost instantaneous) when playing through a video forward, but much slower (~half a second) when stepping backward by even one frame or when jumping to a distant part of a video. (This is an unavoidable consequence of how video decoding works – the price we pay for the amazing compression that video formats provide is that random frame access is not always fast.)

## Installation

```bash
pip install napari-video-streamer
```

- The only python dependencies are `numpyimage[vid]` and `dask[array]`.
- `numpyimage[vid]` relies on `ffmpeg` for video reading, so make sure you have that installed and available in your system path. (You can install `ffmpeg` via your package manager (e.g. `apt`, `brew`, `chocolatey`) or download it from the [official website](https://ffmpeg.org/download.html).)
- We don't list napari as a dependency – you probably already have it installed, but if not, you'll need to do something like `pip install napari[all]` before this plugin can do anything.

## Usage

Open napari and either drag a video file onto the viewer or:

```python
import napari

viewer = napari.Viewer()
viewer.open('path/to/video.mp4')
napari.run()
```

Supported extensions: `.mp4`, `.mkv`, `.avi`, `.mov`, `.webm`.

The resulting image layer carries video metadata on `layer.metadata`, including `fps`, `framerate`, `duration_seconds`, `n_frames`, `source_path`, and the underlying `_video_stream` object for direct access if needed.
