export type GidTokenPayload = {
  sub: string;
  iss: string;
  aud: string;
  tenant: string;
  region: string;
  att: string;
  iat: number;
  exp: number;
  jti: string;
};

export class Issuer {
  constructor(private issuer: string, private ttlSeconds: number = 600) {
    if (ttlSeconds > 600) throw new Error("TTL must be <= 10 minutes");
  }

  mint(payload: Omit<GidTokenPayload, "iss" | "iat" | "exp">): GidTokenPayload {
    const now = Math.floor(Date.now() / 1000);
    return { ...payload, iss: this.issuer, iat: now, exp: now + this.ttlSeconds };
  }
}
