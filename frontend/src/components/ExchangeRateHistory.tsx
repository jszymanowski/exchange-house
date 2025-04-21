import { Skeleton } from "@/components/ui/skeleton";
import { useQuery } from "@tanstack/react-query";
import type ProperDate from "@jszymanowski/proper-date.js";

import LineChart from "@/components/charts/LineChart";
import ErrorOverlay from "@/components/ErrorOverlay";

import { Box } from "@jszymanowski/breeze-primitives";
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
    timeSeries.length > 0 && (
      <Box
        variant="muted"
        rounded="lg"
        width="full"
        height="full"
        className="border-border border"
      >
        <LineChart data={timeSeries} label={`${fromIsoCode}/${toIsoCode}`} />
      </Box>
    )
  );
}
