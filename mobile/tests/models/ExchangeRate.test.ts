import ProperDate from "@still-forest/proper-date.js";
import { Big } from "big.js";
import { ExchangeRate } from "@/models/ExchangeRate";

describe("ExchangeRate", () => {
  describe("getExchangeRates", () => {
    test("returns an array of ExchangeRate", () => {
      const subject = ExchangeRate.getExchangeRates();
      expect(subject).toBeDefined();
      expect(subject.length).toBe(15);
      expect(subject[0] instanceof ExchangeRate).toBe(true);
      expect(subject[14] instanceof ExchangeRate).toBe(true);

      const codes = subject.map((rate) => rate.quoteCurrency.code);
      expect(codes.sort()).toMatchObject([
        "AUD",
        "CNY",
        "HKD",
        "IDR",
        "INR",
        "JPY",
        "KHR",
        "KRW",
        "LAK",
        "MYR",
        "PHP",
        "SGD",
        "THB",
        "TWD",
        "VND",
      ]);
    });
  });

  describe("getExchangeRate", () => {
    test("returns an ExchangeRate when found", () => {
      const subject = ExchangeRate.getExchangeRate("USD", "HKD");
      expect(subject).toBeDefined();
      expect(subject?.date).toStrictEqual(new ProperDate("2025-05-01"));
      expect(subject?.rate).toStrictEqual(Big(7.7588));
    });

    test("returns null when not found", () => {
      const subject = ExchangeRate.getExchangeRate("XYZ", "JPY");
      expect(subject).toBeNull();
    });
  });

  describe("getQuoteCurrencyCodes", () => {
    test("returns an array of Currency when found", () => {
      const subject = ExchangeRate.getQuoteCurrencyCodes("USD");
      expect(subject).toBeDefined();
      expect(subject.length).toBe(15);

      expect(subject.sort()).toMatchObject([
        "AUD",
        "CNY",
        "HKD",
        "IDR",
        "INR",
        "JPY",
        "KHR",
        "KRW",
        "LAK",
        "MYR",
        "PHP",
        "SGD",
        "THB",
        "TWD",
        "VND",
      ]);
    });
  });

  describe("formattedRate", () => {
    test("returns a formatted rate", () => {
      const _subject = ExchangeRate.getExchangeRate("USD", "HKD");
    });
  });

  describe("formattedDate", () => {
    test("returns a formatted date", () => {
      const subject = ExchangeRate.getExchangeRate("USD", "HKD");
      expect(subject?.formattedDate).toBe("2025-05-01");
    });
  });

  describe("formattedRate", () => {
    test("returns a formatted rate with 2 decimal places by default", () => {
      const subject = ExchangeRate.getExchangeRate("USD", "HKD");
      expect(subject?.formattedRate).toBe("7.76");
    });

    test("returns a formatted rate with 0 decimal places for select currencies", () => {
      const subject = ExchangeRate.getExchangeRate("USD", "VND");
      expect(subject?.formattedRate).toBe("25,957");
    });
  });
});
