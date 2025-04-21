import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, type Mock, test, vi } from "vitest";
import "@testing-library/jest-dom";
import Big from "big.js";
import Dashboard from "@/components/Dashboard";
import MockProvider from "@tests/support/MockProvider";

import exchangeHouseClient from "@/integrations/exchangeHouseClient";
import { createExchangeRate } from "../support/fixtures";
import ProperDate from "@jszymanowski/proper-date.js";

vi.mock("@/integrations/exchangeHouseClient");

describe("Dashboard", () => {
  const mockExchangeRates = [
    createExchangeRate({
      // 5 years earlier
      date: new ProperDate("2018-10-01"),
      rate: Big(1.333),
    }),
    createExchangeRate({
      // 2 years earlier
      date: new ProperDate("2021-10-01"),
      rate: Big(1.305),
    }),
    createExchangeRate({
      // 1 year earlier
      date: new ProperDate("2022-10-01"),
      rate: Big(1.288),
    }),
    createExchangeRate({
      // 6 months earlier
      date: new ProperDate("2023-04-01"),
      rate: Big(1.199),
    }),
    createExchangeRate({
      // 3 months earlier
      date: new ProperDate("2023-07-01"),
      rate: Big(1.087),
    }),
    createExchangeRate({
      // 1 month earlier
      date: new ProperDate("2023-09-01"),
      rate: Big(1.188),
    }),
    createExchangeRate({
      // 14 days earlier
      date: new ProperDate("2023-09-17"),
      rate: Big(1.102),
    }),
    createExchangeRate({
      // 7 days earlier
      date: new ProperDate("2023-09-24"),
      rate: Big(1.243),
    }),
    createExchangeRate({
      date: new ProperDate("2023-10-01"),
      rate: Big(1.244),
    }),
  ];

  test("renders Dashboard", async () => {
    render(
      <MockProvider
        queryKey={["historical-exchange-rates", "CAD", "USD"]}
        mockData={mockExchangeRates}
      >
        <Dashboard defaultFromIsoCode="CAD" defaultToIsoCode="USD" />
      </MockProvider>,
    );

    await waitFor(() => {
      expect(screen.getByText("CAD/USD")).toBeInTheDocument();
    });

    expect(screen.getByText("1.2440")).toBeInTheDocument();
    expect(screen.getByText("C$1 ≈ $1.2440")).toBeInTheDocument();

    expect(screen.getByText("USD/CAD")).toBeInTheDocument();
    expect(screen.getByText("0.8039")).toBeInTheDocument();
    expect(screen.getByText("$1 ≈ C$0.8039")).toBeInTheDocument();

    expect(screen.getByText(/1 week earlier/)).toBeInTheDocument();
    expect(screen.getByText("+0.08%")).toBeInTheDocument();
    expect(screen.getByText("No material change")).toBeInTheDocument();

    expect(screen.getByText(/2 weeks earlier/)).toBeInTheDocument();
    expect(screen.getByText("+12.89%")).toBeInTheDocument();
    expect(screen.getByText("CAD stronger by +12.89%")).toBeInTheDocument();

    expect(screen.getByText(/1 month earlier/)).toBeInTheDocument();
    expect(screen.getByText("+4.71%")).toBeInTheDocument();
    expect(screen.getByText("CAD stronger by +4.71%")).toBeInTheDocument();

    expect(screen.getByText(/3 months earlier/)).toBeInTheDocument();
    expect(screen.getByText("+14.44%")).toBeInTheDocument();
    expect(screen.getByText("CAD stronger by +14.44%")).toBeInTheDocument();

    expect(screen.getByText(/6 months earlier/)).toBeInTheDocument();
    expect(screen.getByText("+3.75%")).toBeInTheDocument();
    expect(screen.getByText("CAD stronger by +3.75%")).toBeInTheDocument();

    expect(screen.getByText(/1 year earlier/)).toBeInTheDocument();
    expect(screen.getByText("-3.42%")).toBeInTheDocument();
    expect(screen.getByText("CAD weaker by -3.42%")).toBeInTheDocument();

    expect(screen.getByText(/2 years earlier/)).toBeInTheDocument();
    expect(screen.getByText("-4.67%")).toBeInTheDocument();
    expect(screen.getByText("CAD weaker by -4.67%")).toBeInTheDocument();

    expect(screen.getByText(/5 years earlier/)).toBeInTheDocument();
    expect(screen.getByText("-6.68%")).toBeInTheDocument();
    expect(screen.getByText("CAD weaker by -6.68%")).toBeInTheDocument();
  });
});
