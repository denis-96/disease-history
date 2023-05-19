const decodeTokenPayload = (token) => {
  const tokenPayload = token.split(".")[1];
  const decodedTokenPayload = window.atob(tokenPayload);
  return JSON.parse(decodedTokenPayload);
};

const isTokenExpired = (token) => {
  if (!token) return true;
  try {
    const { exp, iat } = decodeTokenPayload(token);
    const tokenLeftTime = exp - Math.round(+new Date() / 1000);
    return tokenLeftTime < (exp - iat) * 0.5;
  } catch (error) {
    console.error(error);
    return true;
  }
};

export { decodeTokenPayload, isTokenExpired };
