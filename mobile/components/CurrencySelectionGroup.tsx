import { View } from "react-native";
import { CurrencySelection } from "@/components/CurrencySelection";
import type { CurrencyCode } from "@/data/currencies";
import { useTheme } from "@/hooks/useThemePreference";
import type { Currency } from "@/models/Currency";

interface CurrencySelectionGroupProps {
  selectedCurrencies: CurrencyCode[];
  setSelectedCurrencies: (currencies: CurrencyCode[]) => void;
  currencies: Currency[];
}

export const CurrencySelectionGroup = ({
  selectedCurrencies,
  setSelectedCurrencies,
  currencies,
}: CurrencySelectionGroupProps) => {
  const { colors } = useTheme();

  return (
    <View
      className="flex flex-col"
      style={{
        overflow: "hidden",
        backgroundColor: colors.background,
        flexDirection: "column",
        height: null,
        borderColor: colors.border,
        borderWidth: 1,
        borderRadius: 8,
      }}
    >
      <CurrencySelection
        selectedCurrency={selectedCurrencies[0]}
        onCurrencyChange={(currency) => setSelectedCurrencies([currency, selectedCurrencies[1], selectedCurrencies[2]])}
        currencies={currencies}
      />
      <CurrencySelection
        selectedCurrency={selectedCurrencies[1]}
        onCurrencyChange={(currency) => setSelectedCurrencies([selectedCurrencies[0], currency, selectedCurrencies[2]])}
        currencies={currencies}
      />
      <CurrencySelection
        selectedCurrency={selectedCurrencies[2]}
        onCurrencyChange={(currency) => setSelectedCurrencies([selectedCurrencies[0], selectedCurrencies[1], currency])}
        currencies={currencies}
        last={true}
      />
    </View>
  );
};
