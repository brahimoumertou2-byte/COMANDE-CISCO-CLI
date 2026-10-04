from types import SimpleNamespace

import pytest

from backend.services.generator_service import GeneratorError, generate, wildcard_from_network


def test_wildcard():
    assert wildcard_from_network("192.168.10.0/24") == "0.0.0.255"


def test_static_route():
    req = SimpleNamespace(
        technology="Static Routing",
        destination="192.168.20.0",
        mask="255.255.255.0",
        next_hop="192.168.10.2",
        interface=None,
        network=None,
        area=0,
        process_id=1,
        router_id=None,
    )
    commands, _ = generate(req)
    assert commands == ["ip route 192.168.20.0 255.255.255.0 192.168.10.2"]


def test_ospf():
    req = SimpleNamespace(
        technology="OSPF",
        destination=None,
        mask=None,
        next_hop=None,
        interface=None,
        network="192.168.10.0/24",
        area=0,
        process_id=1,
        router_id="1.1.1.1",
    )
    commands, _ = generate(req)
    assert commands == [
        "router ospf 1",
        " router-id 1.1.1.1",
        " network 192.168.10.0 0.0.0.255 area 0",
    ]


def test_ospf_requires_network():
    req = SimpleNamespace(
        technology="OSPF", destination=None, mask=None, next_hop=None,
        interface=None, network=None, area=0, process_id=1, router_id=None,
    )
    with pytest.raises(GeneratorError):
        generate(req)
