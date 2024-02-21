import pytest
from pydantic import ValidationError
from backend.src.api.models.schemas.references import ReferenceRangeLow, ReferenceRangeHigh, ReferenceRange


def test_reference_range_low() -> None:
    """
    # Checks pandantic model ReferenceRangeLow.

    # :param value: ReferenceRangeLow value.
    # :param comparator: ReferenceRangeLow comparator.
    # :param unit: ReferenceRangeLow unit.
    # :param system: ReferenceRangeLow system.
    # :param code: ReferenceRangeLow code.
    """
    low = ReferenceRangeLow(value=2.1, comparator='>', unit='mmHg', system='http://unitsofmeasure.org', code='mm[Hg]')

    assert low.value == 2.1
    assert low.comparator == '>'
    assert low.unit == 'mmHg'
    assert low.system == 'http://unitsofmeasure.org'
    assert low.code == 'mm[Hg]'
    
    with pytest.raises(ValidationError):
        ReferenceRangeLow(value=2.1, unit='mmHg', system='http://unitsofmeasure.com', code='mm[Hg]')


def test_reference_range_high() -> None:
    """
    # Checks pandantic model ReferenceRangeHigh.

    # :param value: ReferenceRangeHigh value.
    # :param unit: ReferenceRangeHigh unit.
    # :param system: ReferenceRangeHigh system.
    # :param code: ReferenceRangeHigh code.
    """
    high = ReferenceRangeHigh(value=4.2, unit='mmHg', system='http://unitsofmeasure.org', code='mm[Hg]')

    assert high.value == 4.2
    assert high.unit == 'mmHg'
    assert high.system == 'http://unitsofmeasure.org'
    assert high.code == 'mm[Hg]'
    
    with pytest.raises(ValidationError):
        ReferenceRangeHigh(value=4.2, unit='mmHg', system='http://unitsofmeasure.com', code='mm[Hg]')


def test_reference_range() -> None:
    """
    # Checks pandantic model ReferenceRange.

    # :param low: ReferenceRange low unit.
    # :param hgih: ReferenceRange high value.
    # :param normalValue: ReferenceRange normal value
    # :param type: ReferenceRange type.
    # :param appliesTo: ReferenceRange applied to.
    # :param age: ReferenceRange age.   
    """
    low = ReferenceRangeLow(value=2.0, unit='mmHg', system='http://unitsofmeasure.org', code='mm[Hg]')
    high = ReferenceRangeHigh(value=3.0, unit='mmHg', system='http://unitsofmeasure.org', code='mm[Hg]')
    reference_range = ReferenceRange(low=low, high=high)

    assert reference_range.low == low
    assert reference_range.high == high

