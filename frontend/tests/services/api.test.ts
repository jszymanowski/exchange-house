import { beforeEach, describe, test, expect } from "vitest";

import { getAvailableCurrencyPairs } from "@/services/api";

describe("ExchangeHouse API", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  test("retrieves the current user", async () => {
    localStorage.setItem("authToken", "FAKE-TOKEN");

    const result = await getAvailableCurrencyPairs();
    console.log(result);
  });
});
