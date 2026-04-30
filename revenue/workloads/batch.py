def run_batch(jobs):
    return [j() for j in jobs]
