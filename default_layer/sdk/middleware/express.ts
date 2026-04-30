export const gidMiddleware = (verifyFn: any) => async (req: any, res: any, next: any) => {
  try {
    const token = (req.headers.authorization || "").replace("Bearer ", "");
    req.claims = await verifyFn(token);
    next();
  } catch {
    res.status(401).send("unauthorized");
  }
};
