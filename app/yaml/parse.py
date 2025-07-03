import yaml
from collections import defaultdict

def parse(path: str):
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    source = config["source"]
    column_map = config["column_map"]
    output_filename = config["output_filename"]
    output_sheetname = config["output_sheetname"]

    categorized = defaultdict(dict)
    for item in column_map:
        tag = item["tag"]
        if tag == "list":
            categorized["list"][item["key"]] = item["column"]
        elif tag == "indivisual":
            categorized["indivisual"][item["key"]] = item["column"]
        elif tag == "research":
            categorized["research"][item["key"]] = item["column"]
        elif tag == "system":
            categorized["system"][item["key"]] = item["column"]
        else:
            raise ValueError(f"Invalid tag detected: {tag}")

    return source, output_filename, output_sheetname, dict(categorized)


{
    "list": {
        "company": "A",
        "people": "B",
        "establishyear": "C",
        "recruitmenturl": "D",
    },
    "indivisual": {
        "company": "E",
        "people": "F",
        "establishyear": "G",
        "recruitmenturl": "H",
    },
    "system": {
        "status": "I",
    }
}