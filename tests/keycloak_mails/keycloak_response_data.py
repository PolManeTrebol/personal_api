GROUP_WITH_ONE_SUBGROUP = {
    "id": "1",
    "name": "SERCOTEL hotel group",
    "path": "/all/external/clients/SERCOTEL hotel group",
    "attributes": {},
    "realmRoles": [],
    "clientRoles": {
        "portal": [
            "/features/clients"
        ]
    },
    "subGroups": [
        {
            "id": "1.1",
            "name": "Todo Sercotel",
            "path": "/all/external/clients/SERCOTEL hotel group/Todo Sercotel",
            "attributes": {},
            "realmRoles": [],
            "clientRoles": {
                "portal": [
                    "/resources/accounts/1157/societies/*"
                ]
            },
            "subGroups": []
        }
    ]
}

GROUP_WITH_MORE_SUBGROUPS = {
    "id": "2",
    "name": "Test",
    "path": "/all/external/clients/Test",
    "attributes": {},
    "realmRoles": [],
    "clientRoles": {
        "portal": [
            "/features/clients"
        ]
    },
    "subGroups": [
        {
            "id": "2.1",
            "name": "Todo Test",
            "path": "/all/external/clients/Test/Todo Test",
            "attributes": {},
            "realmRoles": [],
            "clientRoles": {
                "portal": [
                    "/resources/accounts/1157/societies/*"
                ]
            },
            "subGroups": []
        },
        {
            "id": "2.2",
            "name": "LA RAZON",
            "path": "/all/external/clients/Test/LA RAZON",
            "attributes": {},
            "realmRoles": [],
            "clientRoles": {
                "portal": [
                    "/resources/accounts/1157/societies/5"
                ]
            },
            "subGroups": []
        },
        {
            "id": "2.3",
            "name": "32132334a435",
            "path": "/all/external/clients/Test/32132334a435",
            "attributes": {},
            "realmRoles": [],
            "clientRoles": {
                "portal": [
                    "/resources/accounts/1157/societies/919"
                ]
            },
            "subGroups": []
        }
    ]
}

GROUP_WITH_NO_SUBGROUPS_BUT_ROLE = {
    "id": "3",
    "name": "Catalana Occidente",
    "path": "/all/external/clients/Catalana Occidente",
    "attributes": {},
    "realmRoles": [],
    "clientRoles": {
        "portal": [
            "/resources/accounts/1157/societies/*",
            "/features/clients"
        ]
    },
    "subGroups": []
}

GROUP_WITH_NO_SUBGROUPS_AND_NO_ROLE = {
    "id": "4",
    "name": "Trebol energia",
    "path": "/all/external/clients/Trebol Energia",
    "attributes": {},
    "realmRoles": [],
    "clientRoles": {
        "portal": [
            "/features/clients"
        ]
    },
    "subGroups": []
}

GROUP_WITH_MIXED_SUBRGOUPS = {
    "id": "5",
    "name": "Fi Group",
    "path": "/all/external/clients/Fi Group",
    "attributes": {},
    "realmRoles": [],
    "clientRoles": {
        "portal": [
            "/features/clients"
        ]
    },
    "subGroups": [
        {
            "id": "5.1",
            "name": "Todo Aquaclean",
            "path": "/all/external/clients/Fi Group/Todo Aquaclean",
            "attributes": {},
            "realmRoles": [],
            "clientRoles": {
                "portal": [
                    "/resources/accounts/41782/societies/*"
                ]
            },
            "subGroups": []
        },
        {
            "id": "5.2",
            "name": "Todo Archroma",
            "path": "/all/external/clients/Fi Group/Todo Archroma",
            "attributes": {},
            "realmRoles": [],
            "clientRoles": {
                "portal": [
                    "/resources/accounts/1157/societies/*"
                ]
            },
            "subGroups": []
        },
        {
            "id": "5.3",
            "name": "Todo Budenheim",
            "path": "/all/external/clients/Fi Group/Todo Budenheim",
            "attributes": {},
            "realmRoles": [],
            "clientRoles": {
                "portal": [
                    "/resources/accounts/1164/societies/*"
                ]
            },
            "subGroups": []
        }
    ]
}

CLIENTS_GROUP_RESPONSE = {
    "id": "95edccdf-3538-4287-ba4a-82e9229d33b7",
    "name": "clients",
    "path": "/all/external/clients",
    "attributes": {},
    "realmRoles": [],
    "clientRoles": {
        "portal": [
            "/consulting/read_only"
        ]
    },
    "subGroups": [GROUP_WITH_ONE_SUBGROUP,
                  GROUP_WITH_MORE_SUBGROUPS,
                  GROUP_WITH_NO_SUBGROUPS_BUT_ROLE,
                  GROUP_WITH_NO_SUBGROUPS_AND_NO_ROLE,
                  GROUP_WITH_MIXED_SUBRGOUPS],
    "access": {
        "view": True,
        "manage": True,
        "manageMembership": True
    }
}
