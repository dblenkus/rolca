from rest_framework import parsers


class ImageUploadParser(parsers.FileUploadParser):
    media_type = 'image/jpeg'
