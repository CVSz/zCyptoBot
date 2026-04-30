class DAO:
    def __init__(self):
        self.proposals = []
        self.votes = {}

    def propose(self, p):
        self.proposals.append(p)

    def vote(self, proposal_id, voter, weight):
        self.votes.setdefault(proposal_id, []).append((voter, weight))
