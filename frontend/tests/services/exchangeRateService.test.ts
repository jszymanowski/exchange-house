import Big from "big.js";
import ProperDate from "@jszymanowski/proper-date.js";
import { describe, test, expect } from "vitest";

import {
  getAvailableCurrencyPairs,
  getLatestExchangeRate,
} from "@/services/exchangeRateService";

describe("ExchangeRateService", () => {
  describe("#getAvailableCurrencyPairs", () => {
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

  describe("#getLatestExchangeRate", () => {
    test("retrieves the latest exchange rate", async () => {
      const result = await getLatestExchangeRate("EUR", "USD");

      expect(result).toEqual({
        baseCurrencyCode: "EUR",
        quoteCurrencyCode: "USD",
        data: {
          date: new ProperDate("2025-12-25"),
          rate: Big(1.11),
        },
      });
    });
  });
});
