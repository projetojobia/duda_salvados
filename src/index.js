export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/health") {
      return Response.json({
        ok: true,
        service: "duda-salvados",
        timestamp: new Date().toISOString()
      });
    }

    if (url.pathname === "/drop") {
      url.pathname = "/drop.html";
      return env.ASSETS.fetch(new Request(url, request));
    }

    return env.ASSETS.fetch(request);
  }
};
