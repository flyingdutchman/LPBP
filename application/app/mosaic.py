import sys
from PIL import Image
import urllib
import cStringIO
from multiprocessing import Process
from multiprocessing import Queue
from multiprocessing import cpu_count
from multiprocessing import Manager

# Change these 3 config parameters to suit your needs...
TILE_SIZE = 30      # height/width of mosaic tiles in pixels
TILE_MATCH_RES = 1  # tile matching resolution
ENLARGEMENT = 5     # mosaic will be this many times wider and taller

TILE_BLOCK_SIZE = TILE_SIZE / max(min(TILE_MATCH_RES, TILE_SIZE), 1)
WORKER_COUNT = max(cpu_count() - 1, 1)
EOQ_VALUE = None


class TileProcessor:
    def __init__(self, tiles_url):
        self.tiles_url = tiles_url

    def __process_tile(self, URL):
        try:
            file = cStringIO.StringIO(urllib.urlopen(URL).read())
            img = Image.open(file)
            # get the largest square that fits inside the image
            w = img.size[0]
            h = img.size[1]
            min_dimension = min(w, h)
            w_crop = (w - min_dimension) / 2
            h_crop = (h - min_dimension) / 2
            img = img.crop((w_crop, h_crop, w - w_crop, h - h_crop))

            large_tile_img = img.resize((
                                        TILE_SIZE, TILE_SIZE),
                                        Image.ANTIALIAS)
            small_tile_img = img.resize((
                                        TILE_SIZE/TILE_BLOCK_SIZE,
                                        TILE_SIZE/TILE_BLOCK_SIZE),
                                        Image.ANTIALIAS)

            return (
                    large_tile_img.convert('RGB'),
                    small_tile_img.convert('RGB'))
        except Exception:
            return (None, None)

    def get_tiles(self):
        large_tiles = []
        small_tiles = []

        print('Reading tiles from urls...')

        # search the tiles directory recursively
        for url in self.tiles_url:
            large_tile, small_tile = self.__process_tile(url)
            if large_tile:
                large_tiles.append(large_tile)
                small_tiles.append(small_tile)

        print('Processed %s tiles.' % (len(large_tiles),))

        return (large_tiles, small_tiles)


class TargetImage:
    def __init__(self, image_url):
        self.image_url = image_url

    def get_data(self):
        print('Processing main image...')
        file = cStringIO.StringIO(urllib.urlopen(self.image_url).read())
        img = Image.open(file)
        w = img.size[0] * ENLARGEMENT
        h = img.size[1] * ENLARGEMENT
        large_img = img.resize((w, h), Image.ANTIALIAS)
        w_diff = (w % TILE_SIZE)/2
        h_diff = (h % TILE_SIZE)/2

        # if necesary, crop the image
        if w_diff or h_diff:
            large_img = large_img.crop((
                                        w_diff,
                                        h_diff,
                                        w - w_diff,
                                        h - h_diff))

        small_img = large_img.resize((
                                    w / TILE_BLOCK_SIZE,
                                    h / TILE_BLOCK_SIZE),
                                    Image.ANTIALIAS)

        image_data = (large_img.convert('RGB'), small_img.convert('RGB'))

        print('Main image processed.')

        return image_data


class TileFitter:
    def __init__(self, tiles_data):
        self.tiles_data = tiles_data

    def __get_tile_diff(self, t1, t2, bail_out_value):
        diff = 0
        for i in range(len(t1)):
            diff += (
                    (t1[i][0] - t2[i][0])**2
                    + (t1[i][1] - t2[i][1])**2
                    + (t1[i][2] - t2[i][2])**2)
            if diff > bail_out_value:
                # we know already that this isnt going to be the best fit,
                # so no point continuing with this tile
                return diff
        return diff

    def get_best_fit_tile(self, img_data):
        best_fit_tile_index = None
        min_diff = sys.maxint
        tile_index = 0

        for tile_data in self.tiles_data:
            diff = self.__get_tile_diff(img_data, tile_data, min_diff)
            if diff < min_diff:
                min_diff = diff
                best_fit_tile_index = tile_index
            tile_index += 1

        return best_fit_tile_index


def fit_tiles(work_queue, result_queue, tiles_data):
    # this function gets run by the worker processes, one on each CPU core
    tile_fitter = TileFitter(tiles_data)

    while True:
        try:
            img_data, img_coords = work_queue.get(True)
            if img_data == EOQ_VALUE:
                break
            tile_index = tile_fitter.get_best_fit_tile(img_data)
            result_queue.put((img_coords, tile_index))
        except KeyboardInterrupt:
            pass

    # let the result handler know that this worker has finished everything
    result_queue.put((EOQ_VALUE, EOQ_VALUE))


class ProgressCounter:
    def __init__(self, total):
        self.total = total
        self.counter = 0

    def update(self):
        self.counter += 1
        sys.stdout.write(
                        "Progress: %s%% %s" %
                        (100 * self.counter / self.total, "\r"))
        sys.stdout.flush()


class MosaicImage:
    def __init__(self, original_img):
        self.image = Image.new(original_img.mode, original_img.size)
        self.x_tile_count = original_img.size[0] / TILE_SIZE
        self.y_tile_count = original_img.size[1] / TILE_SIZE
        self.total_tiles = self.x_tile_count * self.y_tile_count

    def add_tile(self, tile_data, coords):
        img = Image.new('RGB', (TILE_SIZE, TILE_SIZE))
        img.putdata(tile_data)
        self.image.paste(img, coords)

    def get_image(self):
        return self.image

    def save(self, path):
        print "DEBUG: entered function save()"
        self.image.save(path)


def build_mosaic(
                result_queue,
                all_tile_data_large,
                original_img_large,
                result_placeholder):
    _mosaic = MosaicImage(original_img_large)

    active_workers = WORKER_COUNT
    while True:
        try:
            img_coords, best_fit_tile_index = result_queue.get()

            if img_coords == EOQ_VALUE:
                active_workers -= 1
                if not active_workers:
                    break
            else:
                tile_data = all_tile_data_large[best_fit_tile_index]
                _mosaic.add_tile(tile_data, img_coords)

        except KeyboardInterrupt:
            pass

    print('\nFinished building!')
    result_placeholder[0] = _mosaic.image


def compose(original_img, tiles):
    print('Building mosaic, press Ctrl-C to abort...')
    original_img_large, original_img_small = original_img
    tiles_large, tiles_small = tiles

    _mosaic = MosaicImage(original_img_large)

    all_tile_data_large = map(lambda tile: list(tile.getdata()), tiles_large)
    all_tile_data_small = map(lambda tile: list(tile.getdata()), tiles_small)

    work_queue = Queue(WORKER_COUNT)
    result_queue = Queue()

    result_placeholder = Manager().dict()

    try:
        # start the worker processes that will build the mosaic image
        p = Process(
                    target=build_mosaic,
                    args=(
                        result_queue,
                        all_tile_data_large,
                        original_img_large,
                        result_placeholder))
        p.start()

        # start the worker processes that will perform the tile fitting
        for n in range(WORKER_COUNT):
            Process(
                    target=fit_tiles,
                    args=(
                        work_queue,
                        result_queue,
                        all_tile_data_small)).start()

        progress = ProgressCounter(_mosaic.x_tile_count * _mosaic.y_tile_count)
        for x in range(_mosaic.x_tile_count):
            for y in range(_mosaic.y_tile_count):
                large_box = (
                            x * TILE_SIZE,
                            y * TILE_SIZE,
                            (x + 1) * TILE_SIZE,
                            (y + 1) * TILE_SIZE)
                small_box = (
                            x * TILE_SIZE/TILE_BLOCK_SIZE,
                            y * TILE_SIZE/TILE_BLOCK_SIZE,
                            (x + 1) * TILE_SIZE/TILE_BLOCK_SIZE,
                            (y + 1) * TILE_SIZE/TILE_BLOCK_SIZE)
                work_queue.put(
                            (list(
                                original_img_small
                                .crop(small_box)
                                .getdata()),
                                large_box))
                progress.update()

    except KeyboardInterrupt:
        print('\nHalting, saving partial image please wait...')

    finally:
        for n in range(WORKER_COUNT):
            work_queue.put((EOQ_VALUE, EOQ_VALUE))
        p.join()

    return result_placeholder[0]


def mosaic(img_url, tiles_url):

    tiles_data = TileProcessor(tiles_url).get_tiles()
    image_data = TargetImage(img_url).get_data()
    return compose(image_data, tiles_data)
