import { useEffect, useState } from "react";
import { ArrowLeftRight } from "lucide-react";

import { Button, SelectPicker } from "@jszymanowski/breeze-forms";
import type { CurrencyPair, CurrencyCode } from "@/types";
import { CURRENCIES } from "@/currencies";

import { Flex, Text } from "@jszymanowski/breeze-primitives";

const buildCurrencyOptions = (currencyCodes: CurrencyCode[]) => {
  const options = currencyCodes.map((isoCode) => {
    const currencyMetadata = CURRENCIES[isoCode];
    const icon = currencyMetadata?.icon || "";
    const label = currencyMetadata
      ? `${isoCode} (${CURRENCIES[isoCode]?.name})`
      : isoCode;

    return {
      icon: icon,
      value: isoCode,
      label: label,
    };
  });
  return options;
};

const cleanCurrencyList = (
  isoCodes: CurrencyCode[],
  prioritizedCurrency: CurrencyCode = "USD",
) => {
  return Array.from(new Set(isoCodes)).sort((a, b) => {
    if (a === prioritizedCurrency) return -1;
    if (b === prioritizedCurrency) return 1;
    return a.localeCompare(b);
  });
};

interface SelectOption {
  icon?: string;
  value: CurrencyCode;
  label: CurrencyCode | string;
}

interface Props {
  currencyPairs: CurrencyPair[];
  initialValues?: {
    fromIsoCode: CurrencyCode | null;
    toIsoCode: CurrencyCode | null;
  };
  handleSubmit: (
    baseCurrency: CurrencyCode,
    quoteCurrency: CurrencyCode,
  ) => void;
}

const buildQuoteCurrencyOptions = (
  baseCurrency: CurrencyCode | null,
  currencyPairs: CurrencyPair[],
) => {
  if (!baseCurrency) {
    return [];
  }

  const quoteCurrencies = cleanCurrencyList(
    currencyPairs
      .filter((pair) => pair.baseCurrencyCode === baseCurrency)
      .map((pair) => pair.quoteCurrencyCode),
  );

  const options = buildCurrencyOptions(quoteCurrencies);
  return options;
};

export default function CurrencyPairSelection({
  currencyPairs,
  initialValues = { fromIsoCode: null, toIsoCode: null },
  handleSubmit,
}: Props) {
  const [selectedBaseCurrency, setSelectedBaseCurrency] =
    useState<CurrencyCode | null>(initialValues.fromIsoCode);
  const [selectedQuoteCurrency, setSelectedQuoteCurrency] =
    useState<CurrencyCode | null>(initialValues.toIsoCode);

  const [quoteCurrencyOptions, setQuoteCurrencyOptions] = useState<
    SelectOption[]
  >(buildQuoteCurrencyOptions(initialValues.fromIsoCode, currencyPairs));

  const baseCurrencies = cleanCurrencyList(
    currencyPairs.map((pair) => pair.baseCurrencyCode),
  );

  const baseCurrencyOptions = buildCurrencyOptions(baseCurrencies);

  const handleSelectBaseOption = (selected: CurrencyCode) => {
    setSelectedBaseCurrency(selected);
    setSelectedQuoteCurrency(null);

    const options = buildQuoteCurrencyOptions(selected, currencyPairs);
    setQuoteCurrencyOptions(options);

    if (options.length === 1) {
      const { value } = options[0];
      setSelectedQuoteCurrency(value);
    }
  };

  const handleSelectQuoteOption = (selected: CurrencyCode) => {
    setSelectedQuoteCurrency(selected);
  };

  // Submit when both values selected
  useEffect(() => {
    if (selectedBaseCurrency && selectedQuoteCurrency) {
      handleSubmit(selectedBaseCurrency, selectedQuoteCurrency);
    }
  }, [selectedBaseCurrency, selectedQuoteCurrency, handleSubmit]);

  const handleSwap = () => {
    if (selectedBaseCurrency && selectedQuoteCurrency) {
      // Store current values
      const tempBase = selectedBaseCurrency;
      const tempQuote = selectedQuoteCurrency;

      // Reset both to prevent intermediate state submission
      setSelectedBaseCurrency(null);
      setSelectedQuoteCurrency(null);

      // Update quote options for the new base
      const options = buildQuoteCurrencyOptions(tempQuote, currencyPairs);
      setQuoteCurrencyOptions(options);

      // Set new values
      setSelectedBaseCurrency(tempQuote);
      setSelectedQuoteCurrency(tempBase);
    }
  };

  const buildRenderSelected = (label: string) => {
    return ({ value, icon }: SelectOption) => {
      return (
        <>
          <Text>{label}</Text>
          <div>
            {icon ? <span className="mx-1 my-auto">{icon}</span> : null}
            {value && (
              <Text variant="info" className="inline">
                {value}
              </Text>
            )}
            {!value && (
              <Text variant="muted" className="inline">
                Select
              </Text>
            )}
          </div>
        </>
      );
    };
  };

  return (
    <Flex wrap="wrap" gap="4">
      <div className="w-full md:w-auto">
        <SelectPicker
          placeholder="Base currency"
          options={baseCurrencyOptions}
          value={selectedBaseCurrency || ""}
          onSelect={handleSelectBaseOption}
          className="w-full min-w-[250px]"
          renderSelected={buildRenderSelected("Base currency:")}
        />
      </div>
      <div className="w-full md:w-auto">
        <Button
          icon={<ArrowLeftRight size={20} />}
          onClick={handleSwap}
          className="w-full"
        />
      </div>
      <div className="w-full md:w-auto">
        <SelectPicker
          placeholder="Quote currency"
          options={quoteCurrencyOptions}
          value={selectedQuoteCurrency || ""}
          onSelect={handleSelectQuoteOption}
          className="w-full min-w-[250px]"
          renderSelected={buildRenderSelected("Quote currency:")}
        />
      </div>
    </Flex>
  );
}
