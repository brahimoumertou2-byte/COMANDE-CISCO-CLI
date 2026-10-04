import re


def analyze(output: str, context: str | None = None):
    text = output.lower()
    findings = []

    if "administratively down" in text:
        findings.append(("HIGH", "Interface administratively down", "An interface is shut down. Check the relevant interface and use 'no shutdown' when appropriate."))
    elif "down/down" in text or "down down" in text:
        findings.append(("MEDIUM", "Interface link problem", "An interface appears down at both status and protocol level. Check cable, peer interface and interface configuration."))

    if "unassigned" in text and "ip address" in text:
        findings.append(("MEDIUM", "Missing interface IP", "One or more interfaces appear to have no IP address assigned."))

    if "% invalid input" in text or "% incomplete command" in text:
        findings.append(("HIGH", "CLI command error", "Cisco IOS reported an invalid or incomplete command. Re-check the command syntax and configuration mode."))

    if "gateway of last resort is not set" in text:
        findings.append(("LOW", "No default route", "The router does not currently show a gateway of last resort. This is only a problem if Internet/unknown-destination routing is required."))

    if re.search(r"ospf.*down|neighbor.*down|full\s+/-", text):
        findings.append(("MEDIUM", "Possible OSPF adjacency issue", "The pasted output contains indicators that an OSPF neighbor may not be fully established. Check interfaces, area, network statements and authentication if configured."))

    if not findings:
        findings.append(("INFO", "No obvious issue detected", "The pasted output does not contain one of the simple patterns this offline rule-based helper checks."))

    summary = f"Analyzed {len(findings)} finding(s)" + (f" for context '{context}'" if context else "") + "."
    return summary, findings
