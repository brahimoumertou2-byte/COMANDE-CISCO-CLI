import ipaddress


class GeneratorError(ValueError):
    pass


def wildcard_from_network(network: str) -> str:
    try:
        net = ipaddress.ip_network(network, strict=False)
    except ValueError as exc:
        raise GeneratorError("Invalid network or prefix") from exc
    if net.version != 4:
        raise GeneratorError("Wildcard generation currently supports IPv4")
    wildcard = int(net.hostmask)
    return str(ipaddress.IPv4Address(wildcard))


def generate(request) -> tuple[list[str], list[str]]:
    tech = request.technology.strip().lower()
    notes: list[str] = []

    if tech in {"static", "static routing", "ip route"}:
        if not all([request.destination, request.mask, request.next_hop]):
            raise GeneratorError("Static route requires destination, mask and next_hop")
        return [
            f"ip route {request.destination} {request.mask} {request.next_hop}"
        ], ["Run this command from Cisco configuration mode: Router(config)#"]

    if tech in {"default", "default route"}:
        next_hop = request.next_hop or request.interface
        if not next_hop:
            raise GeneratorError("Default route requires next_hop or exit interface")
        return [f"ip route 0.0.0.0 0.0.0.0 {next_hop}"], [
            "Use a next-hop IP or an exit interface appropriate to your topology."
        ]

    if tech == "ospf":
        process_id = request.process_id if request.process_id is not None else 1
        if not request.network:
            raise GeneratorError("OSPF requires an IPv4 network")
        area = request.area if request.area is not None else 0
        wildcard = wildcard_from_network(request.network)
        lines = [f"router ospf {process_id}"]
        if request.router_id:
            lines.append(f" router-id {request.router_id}")
        network = ipaddress.ip_network(request.network, strict=False)
        lines.append(f" network {network.network_address} {wildcard} area {area}")
        notes.append("Verify the chosen OSPF network and area against your topology.")
        return lines, notes

    if tech == "rip":
        if not request.network:
            raise GeneratorError("RIP requires an IPv4 network")
        network = ipaddress.ip_network(request.network, strict=False)
        return ["router rip", " version 2", f" network {network.network_address}", " no auto-summary"], [
            "RIPv2 is legacy technology; use it only for labs or where it is appropriate."
        ]

    raise GeneratorError("Unsupported technology. Use Static, Default, OSPF or RIP.")
