from src.v1.hello_world.service_example import ServiceExample


class TestServiceExample:

    def test_a_should_be_a(self):
        assert 'a' == 'a'

    def test_add_one_should_return_2(self):
        service: ServiceExample = ServiceExample(a=1)
        service.add_one()
        assert service.a == 2
