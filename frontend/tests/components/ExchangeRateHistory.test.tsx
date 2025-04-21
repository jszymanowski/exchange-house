import Big from "big.js";
import ProperDate from "@jszymanowski/proper-date.js";
import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, test, vi } from "vitest";
import "@testing-library/jest-dom";

import ExchangeRateHistory from "@/components/ExchangeRateHistory";
import type { LineChartProps } from "@/components/LineChart";

import { createExchangeRate } from "@tests/support/fixtures";
import MockProvider from "@tests/support/MockProvider";

vi.mock("@/components/LineChart", () => ({
  default: ({ data }: LineChartProps) => {
    const startDate = data[0].date.formatted;
    const endDate = data[data.length - 1].date.formatted;
    return (
      <div>
        Mocked LineChart for {startDate} - {endDate}
      </div>
    );
  },
}));

describe("ExchangeRateHistory", () => {
  const mockExchangeRates1 = [
    createExchangeRate({ date: new ProperDate("2022-12-01"), rate: Big(1.2) }),
    createExchangeRate({ date: new ProperDate("2023-10-01"), rate: Big(1.3) }),
    createExchangeRate({ date: new ProperDate("2024-06-01"), rate: Big(1.4) }),
  ];

  const mockExchangeRates2 = [
    createExchangeRate({ date: new ProperDate("2023-10-01"), rate: Big(1.3) }),
    createExchangeRate({ date: new ProperDate("2024-06-01"), rate: Big(1.4) }),
  ];

  test("renders ExchangeRateHistory and fetches data", async () => {
    render(
      <MockProvider
        queryKey={["historical-exchange-rates", "EUR", "USD", undefined]}
        mockData={mockExchangeRates1}
      >
        <ExchangeRateHistory fromIsoCode="EUR" toIsoCode="USD" />
      </MockProvider>,
    );

    await waitFor(() =>
      expect(
        screen.getByText("Mocked LineChart for 2022-12-01 - 2024-06-01"),
      ).toBeInTheDocument(),
    );
  });

  test("renders ExchangeRateHistory with startDate and fetches data", async () => {
    render(
      <MockProvider
        queryKey={["historical-exchange-rates", "EUR", "USD", "2023-01-01"]}
        mockData={mockExchangeRates2}
      >
        <ExchangeRateHistory
          fromIsoCode="EUR"
          toIsoCode="USD"
          startDate={new ProperDate("2023-01-01")}
        />
      </MockProvider>,
    );

    await waitFor(() =>
      expect(
        screen.getByText("Mocked LineChart for 2023-10-01 - 2024-06-01"),
      ).toBeInTheDocument(),
    );
  });
});
