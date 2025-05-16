import { screen } from "@testing-library/react-native";
import CurrencyThreeTab from "@/app/(tabs)/currency3";
import { renderWithProviders } from "../test-utils";

describe("CurrencyThreeTab", () => {
  test("renders", () => {
    renderWithProviders(<CurrencyThreeTab />);

    const header = screen.getByTestId("exchange-rate-screen-header");
    expect(header).toHaveTextContent("South Korean Won");

    const form = screen.getByTestId("exchange-rate-form");
    expect(form).toHaveTextContent("₩is equivalent toUS$1000");

    const summary = screen.getByTestId("exchange-rate-summary");
    expect(summary).toHaveTextContent("$1 ≈ ₩1,376as of 2025-05-06");
  });
});
