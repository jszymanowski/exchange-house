import { useEffect, useState } from "react";

import { getAvailableCurrencyPairs } from "@/services/api";
import { CurrencyPair } from "@/types";


export default function Home() {
  const [currencyPairs, setCurrencyPairs] = useState<CurrencyPair[]>([]);

  useEffect(() => {
    getAvailableCurrencyPairs().then(setCurrencyPairs);
  }, []);

  return (
    <div>
      <ul>
        {currencyPairs.map((currencyPair) => (
          <li key={currencyPair.baseCurrencyCode}>
            {currencyPair.baseCurrencyCode}
            {currencyPair.quoteCurrencyCode}
          </li>
        ))}
      </ul>
    </div>
  );
}
