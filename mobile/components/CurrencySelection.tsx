import { Ionicons } from "@expo/vector-icons";
import { useState } from "react";
import { Text, TouchableOpacity, View } from "react-native";
import type { CurrencyCode } from "@/data/currencies";
import { useTheme } from "@/hooks/useThemePreference";
import type { Currency } from "@/models/Currency";
import { CurrencySelectionModal } from "./CurrencySelectionModal";

interface CurrencySelectionProps {
  selectedCurrency: CurrencyCode;
  onCurrencyChange: (currency: CurrencyCode) => void;
  currencies: Currency[];
  last?: boolean;
}

export const CurrencySelection = ({
  selectedCurrency,
  onCurrencyChange,
  currencies,
  last,
}: CurrencySelectionProps) => {
  const { colors } = useTheme();
  const [modalVisible, setModalVisible] = useState(false);

  const selectedCurrencyObj = currencies.find(
    (c) => c.code === selectedCurrency
  );

  return (
    <>
      <TouchableOpacity
        className="flex flex-row items-center justify-between px-4 py-0"
        onPress={() => setModalVisible(true)}
        accessibilityRole="button"
        accessibilityLabel={
          selectedCurrencyObj
            ? `Select currency. Current selection: ${selectedCurrencyObj.name}`
            : "Select currency"
        }
        accessibilityHint="Opens currency selection modal"
        testID="currency-selection-button"
        style={{
          backgroundColor: colors.buttonForeground,
          borderBottomWidth: last ? 0 : 1,
          borderBottomColor: colors.border,
          height: 60,
        }}
      >
        {selectedCurrencyObj ? (
          <View className="flex flex-row items-center justify-between">
            <Text className="mr-4 text-lg">{selectedCurrencyObj.flag}</Text>
            <Text
              className="mr-4 font-bold text-lg"
              style={{ color: colors.buttonBackground }}
            >
              {selectedCurrencyObj.code}
            </Text>
            <Text style={{ color: colors.textMuted }} numberOfLines={1}>
              {selectedCurrencyObj.name}
            </Text>
          </View>
        ) : (
          <Text style={{ color: colors.textMuted }}>Select currency</Text>
        )}
        <Ionicons name="chevron-forward" size={18} color={colors.textMuted} />
      </TouchableOpacity>
      <CurrencySelectionModal
        selectedCurrency={selectedCurrency}
        currencies={currencies}
        modalVisible={modalVisible}
        setModalVisible={setModalVisible}
        onCurrencyChange={onCurrencyChange}
      />
    </>
  );
};
