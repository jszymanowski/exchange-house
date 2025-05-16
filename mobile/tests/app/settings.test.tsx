import SettingsTab from "@/app/(tabs)/settings";
import { renderWithProviders } from "../test-utils";
import { waitFor } from "@testing-library/react-native";

describe("SettingsTab", () => {
  test("renders", () => {
    const { getByText, getByTestId } = renderWithProviders(<SettingsTab />);

    expect(getByText("Currencies")).toBeOnTheScreen();
    expect(getByText("Loading currencies...")).toBeOnTheScreen();

    expect(getByText("Theme")).toBeOnTheScreen();
    expect(getByTestId("theme-selection")).toBeOnTheScreen();
  });
});
