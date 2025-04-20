import { useEffect, useState } from "react";
import { Heading, Text } from "@jszymanowski/breeze-primitives";

import { getAvailableCurrencyPairs } from "@/services/api";
import { CurrencyPair } from "@/types";
import { API_URL } from "@/config";

export default function Home() {
  const [currencyPairs, setCurrencyPairs] = useState<CurrencyPair[]>([]);

  useEffect(() => {
    getAvailableCurrencyPairs().then((response) => {
      setCurrencyPairs(response.data);
    });
  }, []);

  return (
    <div>
      <Heading level="1">Exchange House</Heading>
      <a href={`${API_URL}/docs`}><Text>Docs</Text></a>
      <ul>
        {currencyPairs.map((currencyPair) => (
          <li key={`${currencyPair.baseCurrencyCode}-${currencyPair.quoteCurrencyCode}`}>
            {currencyPair.baseCurrencyCode}
            {currencyPair.quoteCurrencyCode}
          </li>
        ))}
      </ul>
    </div>
  );
}
