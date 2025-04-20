import { describe, test, expect } from "vitest";

import { getAvailableCurrencyPairs } from "@/services/api";

describe("ExchangeHouse API", () => {
  test("retrieves the available currency pairs", async () => {
    const result = await getAvailableCurrencyPairs();

    expect(result.data.length).toBe(14);

    expect(result.data[0]).toEqual({
      baseCurrencyCode: "USD",
      quoteCurrencyCode: "EUR",
    });

    expect(result.data[13]).toEqual({
      baseCurrencyCode: "NZD",
      quoteCurrencyCode: "USD",
    });
  });
});
