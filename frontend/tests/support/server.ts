import { setupServer } from "msw/node";

import { http, HttpResponse } from "msw";
import { API_URL } from "@/config";

import { createCurrencyPair } from "./fixtures";

export const handlers = [
  http.get(`${API_URL}/api/v1/exchange_rates/available_currency_pairs`, () => {
    const pairs = [
      ["USD", "EUR"],
      ["USD", "GBP"],
      ["USD", "JPY"],
      ["USD", "CHF"],
      ["USD", "CAD"],
      ["USD", "AUD"],
      ["USD", "NZD"],
      ["EUR", "USD"],
      ["GBP", "USD"],
      ["JPY", "USD"],
      ["CHF", "USD"],
      ["CAD", "USD"],
      ["AUD", "USD"],
      ["NZD", "USD"],
    ];

    const data = pairs.map((pair) =>
      createCurrencyPair({
        baseCurrencyCode: pair[0],
        quoteCurrencyCode: pair[1],
      }),
    );

    return HttpResponse.json({
      data,
    });
  }),

  http.get(`${API_URL}/api/v1/exchange_rates/EUR/USD/latest`, () => {
    return HttpResponse.json({
      baseCurrencyCode: "EUR",
      quoteCurrencyCode: "USD",
      data: {
        date: "2025-12-25",
        rate: "1.11",
      },
    });
  }),
];

export const server = setupServer(...handlers);
