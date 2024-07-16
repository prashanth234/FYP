from storages.backends.s3 import S3Storage

class CustomS3Storage(S3Storage):
  def url(self, *args, signed=False, **kwargs):
    # Call the original url method
    url = super().url(*args, **kwargs)
    if signed:
      return url
    else:
      return self._strip_signing_parameters(url)