import { screen } from "@testing-library/react-native";
import CurrencyTwoTab from "@/app/(tabs)/currency2";
import { renderWithProviders } from "../test-utils";

describe("CurrencyTwoTab", () => {
  test("renders", () => {
    renderWithProviders(<CurrencyTwoTab />);

    const header = screen.getByTestId("exchange-rate-screen-header");
    expect(header).toHaveTextContent("Malaysian Ringgit");

    const form = screen.getByTestId("exchange-rate-form");
    expect(form).toHaveTextContent("RMis equivalent toUS$1000");

    const summary = screen.getByTestId("exchange-rate-summary");
    expect(summary).toHaveTextContent("$1 ≈ RM4.24as of 2025-05-07");
  });
});
