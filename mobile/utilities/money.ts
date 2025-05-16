import type { CurrencyCode } from "@/data/currencies";

export const displayCcy = (amount: number, currencyCode: CurrencyCode, round?: boolean): string => {
  const locale = currencyCode === "IDR" ? "id-ID" : "en-US";

  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency: currencyCode,
    maximumFractionDigits: round ? 0 : 2,
  }).format(amount);
};

export const displayUsd = (amount: number, round?: boolean): string => {
  return displayCcy(amount, "USD", round);
};
