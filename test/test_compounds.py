import pytest
from src.pipeline import Pipeline


@pytest.mark.parametrize("initial_input, target", [
    (["ADP"], {"ADP": 17}),
    (["incorrect_name"], dict()),
    (None, {"ATP": 22, "STI": 11, "ZID": 1, "DPM": 4, "XP9": 3, "18W": 2, "29P": 2}),
])
def test_compounds_name_cross_links_count(initial_input, target):
    pipeline = Pipeline(initial_input)
    result = pipeline.run()
    result = {compound["compound"]: compound["cross_links_count"] for compound in result}
    assert result == target
