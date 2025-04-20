import Big from "big.js";
import ProperDate from "@jszymanowski/proper-date.js";
import { describe, test, expect, vi } from "vitest";

import {
  getAvailableCurrencyPairs,
  getHistoricalExchangeRates,
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

  describe("#getHistoricalExchangeRates", () => {
    vi.mock("@jszymanowski/proper-date.js", async () => {
      const actual = await vi.importActual("@jszymanowski/proper-date.js");
      return {
        ...actual,
        getYesterday: vi.fn(() => new ProperDate("2025-04-10")),
      };
    });

    test("retrieves the historical exchange rates", async () => {
      const result = await getHistoricalExchangeRates(
        "EUR",
        "USD",
        new ProperDate("2024-12-25"),
      );

      expect(result.baseCurrencyCode).toBe("EUR");
      expect(result.quoteCurrencyCode).toBe("USD");

      expect(result.data.length).toBe(107);

      expect(result.data[0]).toEqual({
        date: new ProperDate("2024-12-25"),
        rate: Big(1.001),
      });

      expect(result.data[106]).toEqual({
        date: new ProperDate("2025-04-10"),
        rate: Big(1.531),
      });
    });
  });
});
