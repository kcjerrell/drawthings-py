"""
Assists with creating the model metadata types 
"""

import json
from urllib.request import urlopen

class KVTrack:
    key: str
    values: list[object]
    not_hashable: bool = False
    types: set[str]
    
    def __init__(self, key: str):
        self.key = key
        self.values = []
        self.types = set()

    @property
    def count(self):
        return len(self.values)

    @property
    def unique(self) -> set[object]:
        try:
            return set(self.values)
        except:
            self.not_hashable = True
            return set()

    @property
    def unique_count(self):
        unique = self.unique
        if self.not_hashable:
            return len(self.values)
        return len(unique)

    def record(self, model: dict[str, object]):
        if (self.key in model):
            self.values.append(model[self.key])
            self.types.add(type(model[self.key]).__name__)


def main():
    resp = urlopen("https://kcjerrell.github.io/dt-models/combined_models.json")
    data = json.loads(resp.read().decode("utf-8"))

    mmodels = [*data["officialModels"], *data["communityModels"], *data["uncuratedModels"]]
    print(len(mmodels), "total models")
    loras = [*data["officialLoras"], *data["communityLoras"]]
    print(len(loras), "total loras")
    cnets = [*data["officialCnets"], *data["communityCnets"]]
    print(len(cnets), "total controlnets")
    tis = [*data["communityEmbeddings"]]
    print(len(tis), "total textual inversions")

    print(data.keys())

    # 4 types of models: mmodels, loras, cnets, tis
    # TODO: print a list of every model key that appears in more than one type
    model_types = {
        "mmodels": mmodels,
        "loras": loras,
        "cnets": cnets,
        "tis": tis,
    }

    # Track keys across all types with counts
    key_info: dict[str, dict[str, KVTrack]] = {}
    for type_name, models in model_types.items():
        for model in models:
            for key in model.keys():
                if key not in key_info:
                    key_info[key] = {}
                if type_name not in key_info[key]:
                    key_info[key][type_name] = KVTrack(key)
                key_info[key][type_name].record(model)

    # Print detailed key information
    print("\nKey information across all model types:")
    for key in sorted(key_info.keys()):
        tracks = key_info[key]
        total_count = sum(t.count for t in tracks.values())
        types_str = ", ".join(sorted(tracks.keys()))
        print(f"  {key}: {total_count} total ({types_str})")

    # Print unique values for specific keys
    for key in ["version", "modifier", "prefix"]:
        if key in key_info:
            print(f"\n{key} unique values:")
            for type_name, track in key_info[key].items():
                unique_vals = list(track.unique)
                print(f"  {type_name}: {track.count} total, {sorted(unique_vals)}")

if __name__ == "__main__":
    main()
