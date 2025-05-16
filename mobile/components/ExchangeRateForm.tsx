import { Input } from "@rneui/themed";
import Big from "big.js";
import { useEffect, useRef, useState } from "react";
import { StyleSheet, TextInput, TouchableOpacity, View } from "react-native";
import { Text } from "@/components/Typography";
import { IconSymbol } from "@/components/ui/IconSymbol.ios";
import { useTheme } from "@/hooks/useThemePreference";
import type { Currency } from "@/models/Currency";
import type { ExchangeRate } from "@/models/ExchangeRate";
import { displayUsd } from "@/utilities/money";
import { parseTextAsNumber } from "@/utilities/number";

const extractCents = (amount: number) => {
  const cents = amount % 1;
  return cents.toFixed(2).slice(2);
};

const exchangeToUsd = (exchangeRate: ExchangeRate, amount: number) => {
  return Big(amount).div(exchangeRate.rate).toNumber();
};

interface ExchangeRateFormProps {
  currency: Currency;
  exchangeRate: ExchangeRate;
}

const DEFAULT_RESULT_USD = 10;

export const ExchangeRateForm = ({
  currency,
  exchangeRate,
}: ExchangeRateFormProps) => {
  const initialValue = exchangeRate.rate
    .times(DEFAULT_RESULT_USD)
    .toFixed(currency.decimalPlaces);
  const { numeric: initialNumericValue, formatted: initialDisplayValue } =
    parseTextAsNumber(initialValue);
  const [numericValue, setNumericValue] = useState(initialNumericValue);
  const [displayValue, setDisplayValue] = useState(initialDisplayValue);
  const [amountUsd, setAmountUsd] = useState<number | null>(
    exchangeToUsd(exchangeRate, numericValue)
  );
  const { colors } = useTheme();

  useEffect(() => {
    const newInitialValue = exchangeRate.rate
      .times(DEFAULT_RESULT_USD)
      .toFixed(currency.decimalPlaces);
    handleChangeText(newInitialValue);
  }, [exchangeRate, currency.decimalPlaces]);

  const isDefaultSelected = numericValue === initialNumericValue;

  const input = useRef<TextInput>(null);

  const { symbol } = currency;

  const handleChangeText = (value: string) => {
    const { numeric: numericValue, formatted: formattedValue } =
      parseTextAsNumber(value);
    setNumericValue(numericValue);
    setDisplayValue(formattedValue);
    setAmountUsd(exchangeToUsd(exchangeRate, numericValue));
  };

  const clearText = () => {
    if (isDefaultSelected) {
      setNumericValue(0);
      setDisplayValue("");
      setAmountUsd(null);
    } else {
      handleChangeText(initialValue.toString());
    }
    input.current?.blur();
  };

  const styles = StyleSheet.create({
    container: {
      backgroundColor: colors.inputBackground,
      borderRadius: 18,
      borderWidth: 1,
      borderColor: colors.inputBorder,
      paddingLeft: 8,
      paddingRight: 8,
      height: 80,
    },
    leftIconContainer: {
      paddingLeft: 10,
    },
    leftIcon: {
      fontSize: 24,
      fontFamily: "Georgia",
      color: colors.inputForeground,
    },
    inputContainer: {
      alignItems: "center",
      borderBottomWidth: 0,
      height: "100%",
    },
    input: {
      flex: 1,
      fontSize: 36,
      textAlign: "center",
      color: colors.inputForeground,
    },
    clearButton: {
      color: colors.accent,
      padding: 5,
    },
  });

  return (
    <View
      className="flex flex-col content-center justify-center gap-8"
      testID="exchange-rate-form"
    >
      <View>
        <Input
          ref={input}
          returnKeyType="done"
          value={displayValue}
          onChangeText={handleChangeText}
          keyboardType="numeric"
          textAlign="center"
          selectTextOnFocus={true}
          containerStyle={styles.container}
          inputContainerStyle={styles.inputContainer}
          inputStyle={styles.input}
          leftIcon={<Text style={styles.leftIcon}>{symbol}</Text>}
          leftIconContainerStyle={styles.leftIconContainer}
          rightIcon={
            <TouchableOpacity
              onPress={clearText}
              style={styles.clearButton}
              accessibilityLabel="Clear text"
            >
              <IconSymbol
                name={
                  isDefaultSelected
                    ? "multiply.circle.fill"
                    : "arrow.trianglehead.2.clockwise.rotate.90.circle.fill"
                }
                size={28}
                color={styles.clearButton.color}
              />
            </TouchableOpacity>
          }
        />
      </View>
      {amountUsd && (
        <>
          <Text family="serif" className="text-center text-2xl italic">
            is equivalent to
          </Text>
          <View className="flex flex-row justify-center gap-1">
            <Text className="font-light text-lg">US</Text>
            <Text className="font-light text-7xl">
              {displayUsd(Math.floor(amountUsd), true)}
            </Text>
            <Text className="font-light text-lg">
              {extractCents(amountUsd)}
            </Text>
          </View>
        </>
      )}
    </View>
  );
};
