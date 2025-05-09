import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import Big from "big.js";
import { useQuery } from "@tanstack/react-query";
import ProperDate from "@jszymanowski/proper-date.js";
import {
  Box,
  Flex,
  Grid,
  Text,
  Heading,
} from "@jszymanowski/breeze-primitives";

import ExchangeRateHistory from "@/components/ExchangeRateHistory";
import ErrorOverlay from "@/components/ErrorOverlay";
import Container from "@/components/Container";
import PageLoader from "@/components/PageLoader";
import CurrencyPairSelection from "@/components/CurrencyPairSelection";
import { ChangeCard } from "@/components/ChangeCard";

import type { CurrencyCode, ExchangeRate } from "@/types";
import { CURRENCIES } from "@/currencies";
import {
  getAvailableCurrencyPairs,
  getHistoricalExchangeRates,
} from "@/services/exchangeRateService";

interface InitialProps {
  defaultFromIsoCode: CurrencyCode;
  defaultToIsoCode: CurrencyCode;
}

interface SingleRateCardProps {
  fromIsoCode: CurrencyCode;
  toIsoCode: CurrencyCode;
  exchangeRate: ExchangeRate;
}

const SingleRateCard = ({
  fromIsoCode,
  toIsoCode,
  exchangeRate,
}: SingleRateCardProps) => {
  return (
    <Card className="w-full py-0">
      <CardContent>
        <Flex align="center" justify="center" gap="4">
          <Text>
            {fromIsoCode}/{toIsoCode}
          </Text>
          <Heading level="1" family="sans" variant="info" numeric>
            {exchangeRate.rate.toFixed(4)}
          </Heading>
          <Text size="xs" variant="muted" family="sans">
            {CURRENCIES[fromIsoCode].symbol}1 ≈ {CURRENCIES[toIsoCode].symbol}
            {exchangeRate.rate.toFixed(4)}
          </Text>
        </Flex>
      </CardContent>
    </Card>
  );
};

export default function Dashboard({
  defaultFromIsoCode,
  defaultToIsoCode,
}: InitialProps) {
  const {
    isPending: isPendingCurrencyPairs,
    isError: isErrorCurrencyPairs,
    error: errorCurrencyPairs,
    data: dataCurrencyPairs,
  } = useQuery({
    queryKey: ["currency-pairs"],
    queryFn: getAvailableCurrencyPairs,
    staleTime: 1000 * 60 * 60 * 2, // 12h
  });

  const [fromIsoCode, setFromIsoCode] =
    useState<CurrencyCode>(defaultFromIsoCode);
  const [toIsoCode, setToIsoCode] = useState<CurrencyCode>(defaultToIsoCode);

  const {
    isPending: isPendingHistoricalExchangeRates,
    isError: isErrorHistoricalExchangeRates,
    error: errorHistoricalExchangeRates,
    data: dataHistoricalExchangeRates,
  } = useQuery({
    queryKey: ["historical-exchange-rates", fromIsoCode, toIsoCode],
    queryFn: () => getHistoricalExchangeRates(fromIsoCode, toIsoCode),
  });

  if (isPendingCurrencyPairs || isPendingHistoricalExchangeRates) {
    return <PageLoader message="Loading exchange rates" />;
  }
  if (isErrorCurrencyPairs)
    return <ErrorOverlay message={errorCurrencyPairs.message} />;
  if (isErrorHistoricalExchangeRates)
    return <ErrorOverlay message={errorHistoricalExchangeRates.message} />;

  const timeSeries = new Map(
    dataHistoricalExchangeRates.data.map((d) => [
      d.date.formatted,
      { date: d.date, rate: Big(d.rate) } as ExchangeRate,
    ]),
  );

  const latestDate =
    dataHistoricalExchangeRates.data[
      dataHistoricalExchangeRates.data.length - 1
    ].date;
  const lastDataPoint = timeSeries.get(latestDate.formatted);
  const lastExchangeRate = lastDataPoint && {
    ...lastDataPoint,
    rate: Big(lastDataPoint.rate),
  };

  const getExchangeRate = (date: ProperDate): ExchangeRate | undefined => {
    const key = date.formatted;
    const dataPoint = timeSeries.get(key);
    if (!dataPoint) {
      console.error(`Rate not found for Dashboard ${date.formatted}`);
    }
    return (
      dataPoint && {
        ...dataPoint,
        rate: Big(dataPoint.rate),
      }
    );
  };

  const inverseExchangeRate: ExchangeRate | undefined = lastExchangeRate && {
    ...lastExchangeRate,
    rate: Big(1).div(lastExchangeRate.rate),
  };

  const onCurrencyPairChange = (
    fromIsoCode: CurrencyCode,
    toIsoCode: CurrencyCode,
  ) => {
    setFromIsoCode(fromIsoCode);
    setToIsoCode(toIsoCode);
  };

  return (
    <Container>
      <>
        <div className="mb-16">
          <CurrencyPairSelection
            currencyPairs={dataCurrencyPairs.data}
            initialValues={{ fromIsoCode, toIsoCode }}
            handleSubmit={onCurrencyPairChange}
          />
        </div>
        {lastExchangeRate && (
          <>
            <Grid gap="4" className="md:grid-cols-2">
              <SingleRateCard
                fromIsoCode={fromIsoCode}
                toIsoCode={toIsoCode}
                exchangeRate={lastExchangeRate}
              />
              {inverseExchangeRate && (
                <SingleRateCard
                  fromIsoCode={toIsoCode}
                  toIsoCode={fromIsoCode}
                  exchangeRate={inverseExchangeRate}
                />
              )}
            </Grid>
            <Separator className="my-8" />
            <Grid cols="2" gap="4" className="md:grid-cols-4">
              <ChangeCard
                fromIsoCode={fromIsoCode}
                currentExchangeRate={lastExchangeRate}
                comparisonDate={lastExchangeRate.date.subtract(7, "days")}
                getExchangeRate={getExchangeRate}
              />
              <ChangeCard
                fromIsoCode={fromIsoCode}
                currentExchangeRate={lastExchangeRate}
                comparisonDate={lastExchangeRate.date.subtract(14, "days")}
                getExchangeRate={getExchangeRate}
              />
              <div className="col-span-2 md:row-span-2">
                <ExchangeRateHistory
                  fromIsoCode={fromIsoCode}
                  toIsoCode={toIsoCode}
                  startDate={lastExchangeRate.date.subtract(3, "months")}
                />
              </div>
              <ChangeCard
                fromIsoCode={fromIsoCode}
                currentExchangeRate={lastExchangeRate}
                comparisonDate={lastExchangeRate.date.subtract(1, "month")}
                getExchangeRate={getExchangeRate}
              />
              <ChangeCard
                fromIsoCode={fromIsoCode}
                currentExchangeRate={lastExchangeRate}
                comparisonDate={lastExchangeRate.date.subtract(3, "months")}
                getExchangeRate={getExchangeRate}
              />
            </Grid>
            <Separator className="my-8" />
            <Grid cols="2" gap="4" className="md:grid-cols-4">
              <div className="col-span-2 md:row-span-2">
                <ExchangeRateHistory
                  fromIsoCode={fromIsoCode}
                  toIsoCode={toIsoCode}
                  startDate={lastExchangeRate.date.subtract(5, "years")}
                />
              </div>
              <ChangeCard
                fromIsoCode={fromIsoCode}
                currentExchangeRate={lastExchangeRate}
                comparisonDate={lastExchangeRate.date.subtract(6, "months")}
                getExchangeRate={getExchangeRate}
              />
              <ChangeCard
                fromIsoCode={fromIsoCode}
                currentExchangeRate={lastExchangeRate}
                comparisonDate={lastExchangeRate.date.subtract(12, "months")}
                getExchangeRate={getExchangeRate}
              />
              <ChangeCard
                fromIsoCode={fromIsoCode}
                currentExchangeRate={lastExchangeRate}
                comparisonDate={lastExchangeRate.date.subtract(2, "years")}
                getExchangeRate={getExchangeRate}
              />
              <ChangeCard
                fromIsoCode={fromIsoCode}
                currentExchangeRate={lastExchangeRate}
                comparisonDate={lastExchangeRate.date.subtract(5, "years")}
                getExchangeRate={getExchangeRate}
              />
            </Grid>
          </>
        )}

        <Separator className="my-8" />

        <Heading level="2" className="mb-6">
          Since 1999
        </Heading>
        <Box className="max-h[300px]">
          <ExchangeRateHistory
            fromIsoCode={fromIsoCode}
            toIsoCode={toIsoCode}
            startDate={new ProperDate("1999-12-31")}
          />
        </Box>
      </>
    </Container>
  );
}
