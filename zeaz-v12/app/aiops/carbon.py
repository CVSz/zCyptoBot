class CarbonModel:
    REGION_CARBON = {
        "region-a": 400,
        "region-b": 200,
        "region-c": 100,
    }

    def best_region(self, regions):
        return min(regions, key=lambda r: self.REGION_CARBON.get(r, 500))

    def score(self, region, load):
        return self.REGION_CARBON.get(region, 500) * load
