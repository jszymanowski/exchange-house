import { useEffect, useState } from "react";
import { View } from "react-native";
import { ExchangeRateForm } from "@/components/ExchangeRateForm";
import type { CurrencyCode } from "@/data/currencies";
import { useTheme } from "@/hooks/useThemePreference";
import { Currency } from "@/models/Currency";
import { ExchangeRate } from "@/models/ExchangeRate";
import { ScreenWrapper } from "./ScreenWrapper";
import { Heading, Text } from "./Typography";

interface ExchangeRateScreenProps {
  currencyCode: CurrencyCode;
}

export default function ExchangeRateScreen({ currencyCode }: ExchangeRateScreenProps) {
  const { colors } = useTheme();
  const currency = Currency.getCurrency(currencyCode);
  const [exchangeRate, setExchangeRate] = useState<ExchangeRate | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    setIsLoading(true);
    try {
      const rate = ExchangeRate.getExchangeRate("USD", currencyCode);
      setExchangeRate(rate);
    } catch (error) {
      console.error("Failed to fetch exchange rate:", error);
      // Consider adding error state and UI handling
    } finally {
      setIsLoading(false);
    }
  }, [currencyCode]);

  if (!currency) {
    return <Text>Currency not found</Text>;
  }

  if (isLoading) {
    return <Text>Loading...</Text>;
  }

  return (
    <ScreenWrapper>
      <View
        style={{ backgroundColor: colors.background }}
        className="flex h-36 w-full items-center justify-center"
        testID="exchange-rate-screen-header"
      >
        <Heading level={1} className="font-light">
          {currency.name}
        </Heading>
      </View>

      {exchangeRate && (
        <>
          <ExchangeRateForm currency={currency} exchangeRate={exchangeRate} />

          <View testID="exchange-rate-summary" className="mt-8 flex grow flex-col items-center justify-end pb-[100px]">
            <Text color="muted" className="text-center">
              $1 ≈ {currency.symbol}
              {exchangeRate.formattedRate}
            </Text>
            <Text color="muted" className="text-center">
              as of {exchangeRate.formattedDate}
            </Text>
          </View>
        </>
      )}
    </ScreenWrapper>
  );
}
