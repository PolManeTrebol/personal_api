from typing import Any

import pytest

from src.v1.keycloak_mails_account.domain.groups_by_account_extractor import GroupsByAccountExtractor
from tests.keycloak_mails.keycloak_response_data import GROUP_WITH_MORE_SUBGROUPS, GROUP_WITH_ONE_SUBGROUP, \
    GROUP_WITH_NO_SUBGROUPS_BUT_ROLE, GROUP_WITH_NO_SUBGROUPS_AND_NO_ROLE, GROUP_WITH_MIXED_SUBRGOUPS, \
    CLIENTS_GROUP_RESPONSE


class TestGroupsByAccountExtractor:

    @pytest.mark.parametrize("input_group,input_id_account, expected_list", [
        (GROUP_WITH_ONE_SUBGROUP, 1157, ['1.1']),
        (GROUP_WITH_MORE_SUBGROUPS, 1157, ['2.1', '2.2', '2.3']),
        (GROUP_WITH_NO_SUBGROUPS_BUT_ROLE, 1157, ['3']),
        (GROUP_WITH_NO_SUBGROUPS_AND_NO_ROLE, 1157, []),
        (GROUP_WITH_MIXED_SUBRGOUPS, 1157, ['5.2'])

    ])
    def test_recurse_subgroups(self, input_group: dict[str, Any], input_id_account: int, expected_list: list[str]):
        # Arrange
        extractor: GroupsByAccountExtractor = GroupsByAccountExtractor()

        # Act
        result = extractor._recurse_subgroups(group=input_group, id_account=input_id_account)

        # Assert
        assert result == expected_list

    def test_extract_groups_with_idaccount(self):
        # Arrange
        keycloak_response = CLIENTS_GROUP_RESPONSE
        expected_group_ids_from_test_account = ['1.1', '2.1', '2.2', '2.3', '3', '5.2']

        extractor: GroupsByAccountExtractor = GroupsByAccountExtractor()

        # Act
        result = extractor.extract_groups_with_idaccount(clients_group=keycloak_response, idaccount=1157)

        # Assert
        assert result == expected_group_ids_from_test_account

    @pytest.mark.parametrize("input_id_account,input_role,expected_match", [
        (None, '', False),
        (1157, '', False),
        (None, '/resources/accounts', False),
        (1157, '/resources/accounts/110', False),
        (1157, '/resources/accounts/1157', True),
        (1157, '/resources/accounts/110/societies/*', False),
        (1157, '/resources/accounts/1157/societies/*', True),
    ])
    def test_matching_roles(self, input_id_account: int, input_role: str, expected_match: bool):
        # Arrange
        extractor: GroupsByAccountExtractor = GroupsByAccountExtractor()

        # Act
        result = extractor.matching_roles(id_account=input_id_account, role=input_role)

        # Assert
        assert result == expected_match
