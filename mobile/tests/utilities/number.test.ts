import { parseTextAsNumber } from "@/utilities/number";

describe("parseTextAsNumber", () => {
  it("should return the correct formatted number", () => {
    const result = parseTextAsNumber("1234567890");
    expect(result).toEqual({
      numeric: 1234567890,
      formatted: "1,234,567,890",
    });
  });

  it("should return the correct formatted number with decimal place", () => {
    const result = parseTextAsNumber("1234567890.123");
    expect(result).toEqual({
      numeric: 1234567890.123,
      formatted: "1,234,567,890.123",
    });
  });

  it("should return the correct formatted number with decimal place and no decimal", () => {
    const result = parseTextAsNumber("1234567890.");
    expect(result).toEqual({
      numeric: 1234567890.0,
      formatted: "1,234,567,890.",
    });
  });

  it("should return 0 if the input is empty", () => {
    const result = parseTextAsNumber("");
    expect(result).toEqual({
      numeric: 0,
      formatted: "0.00",
    });
  });
});
