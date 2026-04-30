from tender_ai.generator.rfp_parser import parse_rfp
from tender_ai.generator.proposal_builder import build


def run(rfp_text):
    req = parse_rfp(rfp_text)
    proposal = build(req)
    return proposal
