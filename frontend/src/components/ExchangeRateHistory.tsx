import { Skeleton } from "@/components/ui/skeleton";
import { useQuery } from "@tanstack/react-query";
import type ProperDate from "@jszymanowski/proper-date.js";
import { Box, Text } from "@jszymanowski/breeze-primitives";
import { LineChart } from "@jszymanowski/breeze-charts";

import ErrorOverlay from "@/components/ErrorOverlay";

import type { CurrencyCode } from "@/types";
import { getHistoricalExchangeRates } from "@/services/exchangeRateService";

interface Props {
  fromIsoCode: CurrencyCode;
  toIsoCode: CurrencyCode;
  startDate?: ProperDate;
}

export default function ExchangeRateHistory({
  fromIsoCode,
  toIsoCode,
  startDate,
}: Props) {
  const {
    isPending,
    isError,
    error,
    data: response,
  } = useQuery({
    queryKey: ["historical-exchange-rates", fromIsoCode, toIsoCode, startDate],
    queryFn: () =>
      getHistoricalExchangeRates(fromIsoCode, toIsoCode, startDate),
  });

  if (isPending) {
    return <Skeleton className="h-full w-full rounded-xl" />;
  }
  if (isError) return <ErrorOverlay message={error.message} />;

  const timeSeries = response.data.map((d) => ({
    date: d.date,
    value: Number(d.rate),
  }));

  return (
    <Box
      variant="muted"
      rounded="lg"
      width="full"
      height="full"
      className="border-border border"
    >
      {timeSeries.length === 0 && (
        <Text>No historical data available for this currency pair.</Text>
      )}
      {timeSeries.length > 0 && (
        <LineChart data={timeSeries} label={`${fromIsoCode}/${toIsoCode}`} />
      )}
    </Box>
  );
}
