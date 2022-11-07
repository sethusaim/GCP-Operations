from os import listdir
from os.path import join
from pickle import loads

from google.cloud.storage import Client

from src.constant import SAVE_FORMAT


class GCSOperation:
    def __init__(self):
        pass

    def get_storage_client(self):
        try:
            storage_client = Client()

            return storage_client

        except Exception as e:
            raise e

    def get_bucket(self, bucket):
        try:
            storage_client = self.get_storage_client()

            bucket = storage_client.bucket(bucket)

            return bucket

        except Exception as e:
            raise e

    def get_file_object(self, fname, bucket):
        try:
            blob = bucket.blob(fname)

            return blob

        except Exception as e:
            raise e

    def read_file_object(self, f_obj, decode=False):
        try:
            conv_func = (
                lambda: f_obj.download_as_bytes()
                if decode is False
                else f_obj.download_as_string()
            )

            return conv_func()

        except Exception as e:
            raise e

    def upload_file(self, bucket, src_fname, dest_fname):
        try:
            bucket = self.get_bucket(bucket)

            blob = self.get_file_object(dest_fname, bucket)

            blob.upload_from_filename(src_fname)

        except Exception as e:
            raise e

    def load_model(self, model_name, bucket, model_dir=None):
        try:
            func = (
                lambda: model_name + SAVE_FORMAT
                if model_dir is None
                else model_dir + "/" + model_name + SAVE_FORMAT
            )

            model_file = func()

            bucket = self.get_bucket(bucket)

            f_obj = self.get_file_object(model_file, bucket)

            model_content = self.read_file_object(f_obj, decode=True)

            model = loads(model_content)

            return model

        except Exception as e:
            raise e

    def upload_folder(self, folder, bucket):
        try:
            files = listdir(folder)

            for f in files:
                src_f = join(folder, f)

                dest_f = folder + "/" + f

                self.upload_file(bucket, src_f, dest_f)

        except Exception as e:
            raise e
