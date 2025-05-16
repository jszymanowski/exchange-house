import { Currency } from "@/models/Currency";
import { CurrencyService } from "@/services/CurrencyService";

describe("CurrencyService", () => {
  describe("getSelectableCurrencies", () => {
    test("returns an array of Currency", () => {
      const subject = CurrencyService.getSelectableCurrencies();
      expect(subject).toBeDefined();
      expect(subject.length).toBe(15);
      expect(subject[0] instanceof Currency).toBe(true);
      expect(subject[14] instanceof Currency).toBe(true);
    });
  });
});
