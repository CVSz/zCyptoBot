from model import CostModel


def choose_region(regions):
    model = CostModel()
    return min(regions, key=lambda region: model.score(region))
