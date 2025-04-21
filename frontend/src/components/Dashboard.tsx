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

import type { CurrencyCode, ExchangeRate } from "@/types";
import { CURRENCIES } from "@/currencies";
import color from "@/styles/color";
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

interface ChangeCardProps {
  fromIsoCode: CurrencyCode;
  toIsoCode: CurrencyCode;
  currentExchangeRate: ExchangeRate;
  previousExchangeRate: ExchangeRate | undefined;
}

const getBackgroundColorShade = (
  relativeChangePercent: number,
): 100 | 200 | 300 | 400 | 500 | 600 | 700 => {
  const shadeBounds = [100, 700];
  const changePercentBounds = [0.01, 5];

  const interpolatedShade = Math.abs(
    ((shadeBounds[1] - shadeBounds[0]) /
      (changePercentBounds[1] - changePercentBounds[0])) *
      (Math.abs(relativeChangePercent) - changePercentBounds[0]) +
      shadeBounds[0],
  );

  const clamped = Math.min(
    shadeBounds[1],
    Math.max(shadeBounds[0], Math.round(interpolatedShade / 100) * 100),
  ) as 100 | 200 | 300 | 400 | 500 | 600 | 700;

  return clamped;
};

const ChangeCard = ({
  fromIsoCode,
  currentExchangeRate,
  previousExchangeRate,
}: ChangeCardProps) => {
  if (!previousExchangeRate)
    return <Text variant="danger">Data unavailable</Text>;

  const { rate: currentValue, date: currentDate } = currentExchangeRate;
  const { rate: previousValue, date: previousDate } = previousExchangeRate;

  const numDaysDifference = currentDate.difference(previousDate, {
    period: "days",
  });

  let headline = "";
  if (numDaysDifference < 7) {
    headline = `${numDaysDifference} days earlier`;
  } else if (numDaysDifference < 30) {
    const numWeeksDifference = Math.round(numDaysDifference / 7);
    if (numWeeksDifference === 1) headline = "1 week earlier";
    else headline = `${numWeeksDifference} weeks earlier`;
  } else if (numDaysDifference < 365) {
    const numMonthsDifference = Math.round(numDaysDifference / 30);
    if (numMonthsDifference === 1) headline = "1 month earlier";
    else headline = `${numMonthsDifference} months earlier`;
  } else {
    const numYearsDifference = Math.round(numDaysDifference / 365);
    if (numYearsDifference === 1) headline = "1 year earlier";
    else headline = `${Math.round(numDaysDifference / 365)} years earlier`;
  }

  const relativeChangePercent: Big = currentValue
    .minus(previousValue)
    .div(previousValue)
    .times(100);

  const relativeChangeDisplay = relativeChangePercent.gt(0)
    ? `+${relativeChangePercent.toFixed(2)}%`
    : `${relativeChangePercent.toFixed(2)}%`;

  let subtext = "";

  if (relativeChangePercent.abs().lt(0.1)) {
    subtext = "No material change";
  } else if (relativeChangePercent.gt(0)) {
    subtext = `${fromIsoCode} stronger by ${relativeChangeDisplay}`;
  } else if (relativeChangePercent.lt(0)) {
    subtext = `${fromIsoCode} weaker by ${relativeChangeDisplay}`;
  } else {
    subtext = "N/A";
  }

  const backgroundColor = relativeChangePercent.gte(0) ? "green" : "red";
  const backgroundColorShade = getBackgroundColorShade(
    relativeChangePercent.toNumber(),
  );

  const colorValue = color[backgroundColor];

  return (
    <Card
      className="w-full border py-0 outline-6 -outline-offset-8"
      style={{
        outlineColor: colorValue[backgroundColorShade] ?? colorValue["500"],
      }}
    >
      <CardContent className="align-center flex flex-col justify-between gap-2 p-6">
        <Text variant="muted">vs. {headline}</Text>
        <Heading family="sans" level="2" numeric>
          {relativeChangeDisplay}
        </Heading>
        <Text size="xs" variant="muted">
          {subtext}
        </Text>
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
                toIsoCode={toIsoCode}
                currentExchangeRate={lastExchangeRate}
                previousExchangeRate={getExchangeRate(
                  lastExchangeRate.date.subtract(7, "days"),
                )}
              />
              <ChangeCard
                fromIsoCode={fromIsoCode}
                toIsoCode={toIsoCode}
                currentExchangeRate={lastExchangeRate}
                previousExchangeRate={getExchangeRate(
                  lastExchangeRate.date.subtract(14, "days"),
                )}
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
                toIsoCode={toIsoCode}
                currentExchangeRate={lastExchangeRate}
                previousExchangeRate={getExchangeRate(
                  lastExchangeRate.date.subtract(1, "month"),
                )}
              />
              <ChangeCard
                fromIsoCode={fromIsoCode}
                toIsoCode={toIsoCode}
                currentExchangeRate={lastExchangeRate}
                previousExchangeRate={getExchangeRate(
                  lastExchangeRate.date.subtract(3, "months"),
                )}
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
                toIsoCode={toIsoCode}
                currentExchangeRate={lastExchangeRate}
                previousExchangeRate={getExchangeRate(
                  lastExchangeRate.date.subtract(6, "months"),
                )}
              />
              <ChangeCard
                fromIsoCode={fromIsoCode}
                toIsoCode={toIsoCode}
                currentExchangeRate={lastExchangeRate}
                previousExchangeRate={getExchangeRate(
                  lastExchangeRate.date.subtract(12, "months"),
                )}
              />
              <ChangeCard
                fromIsoCode={fromIsoCode}
                toIsoCode={toIsoCode}
                currentExchangeRate={lastExchangeRate}
                previousExchangeRate={getExchangeRate(
                  lastExchangeRate.date.subtract(2, "years"),
                )}
              />
              <ChangeCard
                fromIsoCode={fromIsoCode}
                toIsoCode={toIsoCode}
                currentExchangeRate={lastExchangeRate}
                previousExchangeRate={getExchangeRate(
                  lastExchangeRate.date.subtract(5, "years"),
                )}
              />
            </Grid>
          </>
        )}

        <Separator className="my-8" />

        <Heading level="2" className="mb-6">
          Since 2010
        </Heading>
        <Box className="max-h[300px]">
          <ExchangeRateHistory
            fromIsoCode={fromIsoCode}
            toIsoCode={toIsoCode}
            startDate={new ProperDate("2009-12-31")}
          />
        </Box>
      </>
    </Container>
  );
}
