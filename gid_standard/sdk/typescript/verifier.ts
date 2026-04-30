import { GidTokenPayload } from "./issuer";

export class Verifier {
  constructor(private trustedIssuers: Set<string>, private revoked: Set<string> = new Set()) {}

  verify(payload: GidTokenPayload): GidTokenPayload {
    const now = Math.floor(Date.now() / 1000);

    if (!this.trustedIssuers.has(payload.iss)) {
      throw new Error("untrusted issuer");
    }

    if (now > payload.exp) {
      throw new Error("expired");
    }

    if (!payload.att) {
      throw new Error("missing attestation");
    }

    if (this.revoked.has(payload.jti)) {
      throw new Error("revoked");
    }

    return payload;
  }
}
