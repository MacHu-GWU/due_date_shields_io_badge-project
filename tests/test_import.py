# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx


def test():
    import due_date_shields_io_badge
    pass


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])