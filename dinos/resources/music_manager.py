from dinos.resources.asset_manager_abstract import AssetManagerAbstract


class MusicManager(AssetManagerAbstract):

    def __init__(self):
        super().__init__(("assets", "music"))

    def _load_asset(self, asset_path, options={}):
        return asset_path
