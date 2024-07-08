class PortalTestValidator:
    def has_test_access(self, resources: list) -> bool:
        test_path = '/environments/test'
        return test_path in resources

    def is_request_from_portal_test(self, origin: str) -> bool:
        test_host = ['https://portal-test.grupotrebolenergia.es', 'https://clientes-test.grupotrebolenergia.es']
        return origin in test_host
