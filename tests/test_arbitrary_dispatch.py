from django.test import TestCase

from core.arbitrary_dispatch import arbitrary_dispatch


@arbitrary_dispatch
def test(d):
    return d["type"]


@test.register("fake")
def fake_test(d):
    return "Got some fake test"


@test.register("real")
def real_test(d):
    return "Got some real test!"


@test.register("__default__")
def default_test(d):
    return "Default handler"


class TestArbitraryDispatch(TestCase):
    def test_fake_dispatch(self):
        self.assertEqual(
            test({"type": "fake"}),
            "Got some fake test"
        )

    def test_real_dispatch(self):
        self.assertEqual(
            test({"type": "real"}),
            "Got some real test!"
        )

    def test_default_dispatch(self):
        self.assertEqual(
            test({"type": "jabberwocky"}),
            "Default handler"
        )
