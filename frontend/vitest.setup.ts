import { afterAll, afterEach, beforeAll } from "vitest";
import { server } from "./tests/support/server";

beforeAll(() => server.listen({ onUnhandledRequest: "error" }));

afterEach(() => {
  server.resetHandlers();
});

afterAll(() => {
  server.close();
});
