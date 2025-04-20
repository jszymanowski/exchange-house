import { describe, test, expect } from "vitest";

import { getAvailableCurrencyPairs } from "@/services/api";

describe("ExchangeHouse API", () => {
  test("retrieves the available currency pairs", async () => {
    const result = await getAvailableCurrencyPairs();

    expect(result.data.length).toBe(14);

    expect(result.data).toContainEqual({
      baseCurrencyCode: "USD",
      quoteCurrencyCode: "EUR",
    });

    expect(result.data).toContainEqual({
      baseCurrencyCode: "NZD",
      quoteCurrencyCode: "USD",
    });
  });
});
