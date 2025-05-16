import { Currency } from "@/models/Currency";

describe("Currency", () => {
  describe("getCurrencies", () => {
    test("returns an array of Currency", () => {
      const subject = Currency.getCurrencies();
      expect(subject).toBeDefined();
      expect(subject.length).toBe(156);
      expect(subject[0] instanceof Currency).toBe(true);
      expect(subject[155] instanceof Currency).toBe(true);
    });
  });

  describe("getCurrency", () => {
    test("returns a Currency when found", () => {
      const subject = Currency.getCurrency("USD");
      expect(subject).toBeDefined();
      expect(subject instanceof Currency).toBe(true);
      expect(subject.code).toBe("USD");
      expect(subject.name).toBe("US Dollar");
      expect(subject.symbol).toBe("$");

      const subject2 = Currency.getCurrency("JPY");
      expect(subject2).toBeDefined();
      expect(subject2 instanceof Currency).toBe(true);
      expect(subject2.code).toBe("JPY");
      expect(subject2.name).toBe("Japanese Yen");
      expect(subject2.symbol).toBe("¥");
    });

    test("returns null when not found", () => {
      const subject = Currency.getCurrency("XYZ");
      expect(subject).toBeNull();
    });
  });
});
