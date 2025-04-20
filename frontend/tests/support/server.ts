import { setupServer } from "msw/node";
import ProperDate from "@jszymanowski/proper-date.js";

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

  http.get(
    `${API_URL}/api/v1/exchange_rates/EUR/USD/historical`,
    ({ request }: { request: Request }) => {
      const url = new URL(request.url);
      const startDate = new ProperDate(
        url.searchParams.get("start_date") || "2010-01-01",
      );
      const mockYesterday = new ProperDate("2025-04-10");

      const data = [];
      for (
        let date = startDate;
        date <= mockYesterday;
        date = date.add(1, "day")
      ) {
        // Calculate mock rate that gradually increases from ~1.001 based on days from start date
        const rate = 1.001 + date.difference(startDate) / 100 / 2;
        data.push({
          date: date.toString(),
          rate: rate.toString(),
        });
      }

      return HttpResponse.json({
        baseCurrencyCode: "EUR",
        quoteCurrencyCode: "USD",
        data,
      });
    },
  ),
];

export const server = setupServer(...handlers);
