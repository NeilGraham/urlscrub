class Jena:
    def __init__(self, url, default_repository=None):

        if url.endswith("/"):
            url = url[:-1]

        self.url = url
        self.default_repository = default_repository

    def get_repository(self, specified):
        default = self.default_repository

        if all(repo == None for repo in [specified, default]):
            raise ValueError("No repository specified.")

        if specified != None:
            return specified
        else:
            return default

    def upload_file(self, file, repository=None):
        repository = self.get_repository(repository)
        return None
