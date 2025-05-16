import { Divider } from "@rneui/themed";
import { useCallback, useEffect, useState } from "react";
import { View } from "react-native";
import { CurrencySelectionGroup } from "@/components/CurrencySelectionGroup";
import { ScreenWrapper } from "@/components/ScreenWrapper";
import { ThemeSelection } from "@/components/ThemeSelection";
import { Heading, Text } from "@/components/Typography";
import type { CurrencyCode } from "@/data/currencies";
import { useStorage } from "@/hooks/useStorage";
import { CurrencyService } from "@/services/CurrencyService";

const SectionHeader = ({ title }: { title: string }) => {
  return <Heading level={4}>{title}</Heading>;
};

export default function SettingsTab() {
  const { getItem, setItem } = useStorage();

  const [currenciesLoaded, setCurrenciesLoaded] = useState(false);
  const [selectedCurrencies, setSelectedCurrencies] = useState<CurrencyCode[]>(
    []
  );

  const loadCurrencies = useCallback(async () => {
    const data = await getItem("selected-currencies");
    if (data) {
      try {
        setSelectedCurrencies(JSON.parse(data));
      } catch (error) {
        console.error("Error parsing stored currencies:", error);
        setSelectedCurrencies(["USD", "EUR", "GBP"]); // Set default currencies
      }
    } else {
      // No stored currencies, set defaults
      setSelectedCurrencies(["USD", "EUR", "GBP"]);
    }
    setCurrenciesLoaded(true);
  }, [getItem]);

  useEffect(() => {
    loadCurrencies();
  }, [loadCurrencies]);

  const handleSave = useCallback(
    async (newSelectedCurrencies: CurrencyCode[]) => {
      await setItem(
        "selected-currencies",
        JSON.stringify(newSelectedCurrencies)
      );
      // This will trigger updates in any components subscribed to this key
    },
    [setItem]
  );

  useEffect(() => {
    if (currenciesLoaded) {
      handleSave(selectedCurrencies);
    }
  }, [selectedCurrencies, handleSave, currenciesLoaded]);

  const currencies = CurrencyService.getSelectableCurrencies();

  return (
    <ScreenWrapper>
      <View className="flex flex-col content-center justify-center gap-4 pt-8">
        <SectionHeader title="Currencies" />
        {!currenciesLoaded && <Text>Loading currencies...</Text>}
        {currenciesLoaded && (
          <CurrencySelectionGroup
            selectedCurrencies={selectedCurrencies}
            setSelectedCurrencies={setSelectedCurrencies}
            currencies={currencies}
          />
        )}
        <Divider className="my-4" />
        <SectionHeader title="Theme" />
        <ThemeSelection />
      </View>
    </ScreenWrapper>
  );
}
