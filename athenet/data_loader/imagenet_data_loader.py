"""ImageNet data loader."""

import os
import numpy as np
from scipy import misc
from collections import OrderedDict

import theano

from athenet.utils import get_bin_path, get_data_path
from athenet.data_loader import DataLoader, Buffer


class ImageNetDataLoader(DataLoader):
    """ImageNet data loader."""

    name_prefix = 'ILSVRC'
    train_suffix = '_img_train'
    val_suffix = '_img_val'
    mean_rgb = [123, 117, 104]
    verbosity = 0

    def __init__(self, year, image_shape, buffer_size=1, train_data=True,
                 val_data=True, val_size=None, reverse_training=True,
                 reverse_validation=True):
        """Create ImageNet data loader.

        :param year: Specifies which year's data should be loaded.
        :param image_shape: Image shape in format (height, width).
        :param buffer_size: Number of batches to be stored in memory.
        :param train_data: Specifies whether to load training data.
        :param val_data: Specifies whether to load validation data.
        :param val_size: Maximal size of validation data. If None, then all
                         validation data will be used. Otherwise, val_size
                         images will be chosen randomly from the whole set.
        :param reverse: When set on True, reversed copies of images will be
                        attached to train and validaton data
        """
        super(ImageNetDataLoader, self).__init__()
        self.buffer_size = buffer_size
        self.shuffle_train_data = True
        self._height, self._width = image_shape

        base_name = self.name_prefix + str(year)
        self.train_name = base_name + self.train_suffix
        self.val_name = base_name + self.val_suffix

        if train_data:
            index = 0
            answers = []
            train_files = []
            train_dirs = os.listdir(get_bin_path(self.train_name))
            for d in train_dirs:
                path = os.path.join(self.train_name, d)
                files = os.listdir(get_bin_path(path))
                train_files += [(os.path.join(d, f), False) for f in files]
                answers += [index for i in range(len(files))]
                if reverse_training:
                    train_files += [(os.path.join(d, f), True) for f in files]
                    answers += [index for i in range(len(files))]
                index += 1
            self.train_files = np.asarray(train_files)
            self.train_answers = np.asarray(answers)

            self._train_in = Buffer(self)
            self._train_out = theano.shared(self.train_answers, borrow=True)
            self.train_data_available = True
            self.train_set_size = len(answers)

        if val_data:
            answers = OrderedDict()
            with open(get_data_path(self.val_name + '.txt'), 'rb') as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    filename, answer = line.rsplit(' ', 1)
                    answers[filename] = np.array(int(answer), dtype="int32")
            val_files = [(filename, False) for filename in answers.keys()]
            val_answers = answers.values()
            if reverse_validation:
                val_files = [(filename, True) for filename in answers.keys()]
                val_answers *= 2
            val_answers = np.asarray(val_answers)
            self.val_files = np.asarray(val_files)
            self.val_set_size = len(self.val_files)

            # Reduce amount of validation data, if necessary
            if val_size and val_size < self.val_set_size:
                ind = np.random.permutation(self.val_set_size)[:val_size]
                self.val_files = self.val_files[ind]
                val_answers = val_answers[ind]
                self.val_set_size = val_size

            self._val_in = Buffer(self)
            self._val_out = theano.shared(val_answers, borrow=True)
            self.val_data_available = True

        self.batch_size = 1

    def _get_img(self, filename, reverse):
        img = misc.imread(get_bin_path(filename))
        img = np.rollaxis(img, 2)
        img = img.reshape((1, 3, self._height, self._width))
        result = np.asarray(img, dtype=theano.config.floatX)
        if reverse:
            return result[..., ::-1]
        return result

    def _load_imgs(self, dir_name, files):
        imgs = []
        for filename, reverse in files:
            img = self._get_img(os.path.join(dir_name, filename), reverse)
            r, g, b = np.split(img, 3, axis=1)
            r -= self.mean_rgb[0]
            g -= self.mean_rgb[1]
            b -= self.mean_rgb[2]
            img = np.concatenate([r, g, b], axis=1)
            imgs += [img]
        return np.asarray(np.concatenate(imgs, axis=0),
                          dtype=theano.config.floatX)

    def load_val_data(self, batch_index):
        if self._val_in.contains(batch_index):
            return

        files = self._get_subset(self.val_files, batch_index, self.buffer_size)
        imgs = self._load_imgs(self.val_name, files)
        self._set_subset(self._val_in, imgs, batch_index, self.buffer_size)

    def val_input(self, batch_index):
        return self._get_subset(self._val_in, batch_index)

    def val_output(self, batch_index):
        return self._get_subset(self._val_out, batch_index)

    def load_train_data(self, batch_index):
        if self._train_in.contains(batch_index):
            return

        # Shuffle images when starting new epoch
        if batch_index == 0 and self.shuffle_train_data:
            ind = np.random.permutation(self.train_set_size)
            self.train_files = self.train_files[ind]
            self.train_answers = self.train_answers[ind]
            self._train_out.set_value(self.train_answers, borrow=True)

        files = self._get_subset(self.train_files, batch_index,
                                 self.buffer_size)
        imgs = self._load_imgs(self.train_name, files)
        self._set_subset(self._train_in, imgs, batch_index, self.buffer_size)

    def train_input(self, batch_index):
        return self._get_subset(self._train_in, batch_index)

    def train_output(self, batch_index):
        return self._get_subset(self._train_out, batch_index)


class AlexNetImageNetDataLoader(ImageNetDataLoader):
    """ImageNet data loader for AlexNet."""

    def __init__(self, year=2012, image_shape=(227, 227), buffer_size=1,
                 train_data=False, val_data=True, val_size=None,
                 reverse_training=True, reverse_validation=True):
        self.val_suffix = '_img_val_alexnet'
        super(AlexNetImageNetDataLoader, self).__init__(year, image_shape,
              buffer_size, train_data, val_data, val_size, reverse_training,
              reverse_validation)


class GoogleNetImageNetDataLoader(ImageNetDataLoader):
    """ImageNet data loader for GoogleNet."""

    def __init__(self, year=2012, image_shape=(224, 224), buffer_size=1,
                 train_data=False, val_data=True, val_size=None,
                 reverse_training=True, reverse_validation=True):
        self.val_suffix = '_img_val_googlenet'
        super(GoogleNetImageNetDataLoader, self).__init__(year, image_shape,
              buffer_size, train_data, val_data, val_size, reverse_training,
              reverse_validation)
