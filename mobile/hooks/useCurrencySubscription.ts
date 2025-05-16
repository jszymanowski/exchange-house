import { useCallback, useEffect, useState } from "react";
import { DEFAULT_CURRENCY_CODES } from "@/constants/defaults";
import type { CurrencyCode } from "@/data/currencies";
import { useStorage } from "./useStorage";

export function useCurrencySubscription() {
  const { getItem, subscribe } = useStorage();
  const [currencies, setCurrencies] = useState<CurrencyCode[]>(DEFAULT_CURRENCY_CODES);

  const loadCurrencies = useCallback(async () => {
    const data = await getItem("selected-currencies");
    if (data) {
      try {
        setCurrencies(JSON.parse(data));
      } catch (error) {
        console.error("Failed to parse selected currencies:", error);
        setCurrencies(DEFAULT_CURRENCY_CODES);
      }
    }
  }, [getItem]);

  useEffect(() => {
    loadCurrencies();
    const unsubscribe = subscribe("selected-currencies", loadCurrencies);
    return unsubscribe;
  }, [loadCurrencies, subscribe]);

  return currencies;
}
