import { screen } from "@testing-library/react-native";
import CurrencyOneTab from "@/app/(tabs)/currency1";
import { renderWithProviders } from "../test-utils";

describe("CurrencyOneTab", () => {
  test("renders", () => {
    renderWithProviders(<CurrencyOneTab />);

    const header = screen.getByTestId("exchange-rate-screen-header");
    expect(header).toHaveTextContent("Singapore Dollar");

    const form = screen.getByTestId("exchange-rate-form");
    expect(form).toHaveTextContent("S$is equivalent toUS$1000");

    const summary = screen.getByTestId("exchange-rate-summary");
    expect(summary).toHaveTextContent("$1 ≈ S$1.29as of 2025-05-06");
  });
});
