import Big from "big.js";
import { Text, Heading } from "@still-forest/canopy";
import { Card as BaseCard, CardContent } from "@/components/ui/card";
import color from "@/styles/color";
import type { CurrencyCode, ExchangeRate } from "@/types";
import ProperDate from "@jszymanowski/proper-date.js";

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

const getHeadline = (
  baseDate: ProperDate,
  comparisonDate: ProperDate,
): string => {
  let headline = "vs. ";
  const numDaysDifference = baseDate.difference(comparisonDate, {
    period: "days",
  });

  if (numDaysDifference < 7) {
    headline += `${numDaysDifference} days earlier`;
  } else if (numDaysDifference < 30) {
    const numWeeksDifference = Math.round(numDaysDifference / 7);
    if (numWeeksDifference === 1) headline += "1 week earlier";
    else headline += `${numWeeksDifference} weeks earlier`;
  } else if (numDaysDifference < 365) {
    const numMonthsDifference = Math.round(numDaysDifference / 30);
    if (numMonthsDifference === 1) headline += "1 month earlier";
    else headline += `${numMonthsDifference} months earlier`;
  } else {
    const numYearsDifference = Math.round(numDaysDifference / 365);
    if (numYearsDifference === 1) headline += "1 year earlier";
    else headline += `${Math.round(numDaysDifference / 365)} years earlier`;
  }

  return headline;
};

interface CardProps {
  outlineColor: string;
  title: string;
  changeDisplay: string;
  subtext: string;
}

const Card = ({ outlineColor, title, changeDisplay, subtext }: CardProps) => {
  return (
    <BaseCard
      className="w-full border py-0 outline-6 -outline-offset-8"
      style={{
        outlineColor,
      }}
    >
      <CardContent className="align-center flex flex-col justify-between gap-2 p-6">
        <Text variant="muted">{title}</Text>
        <Heading family="sans" level="2" numeric>
          {changeDisplay}
        </Heading>
        <Text size="xs" variant="muted">
          {subtext}
        </Text>
      </CardContent>
    </BaseCard>
  );
};

interface ChangeCardProps {
  fromIsoCode: CurrencyCode;
  currentExchangeRate: ExchangeRate;
  comparisonDate: ProperDate;
  getExchangeRate: (date: ProperDate) => ExchangeRate | undefined;
}

export const ChangeCard = ({
  fromIsoCode,
  currentExchangeRate,
  comparisonDate,
  getExchangeRate,
}: ChangeCardProps) => {
  const previousExchangeRate = getExchangeRate(comparisonDate);
  const { rate: currentValue, date: currentDate } = currentExchangeRate;

  if (!previousExchangeRate) {
    const headline = getHeadline(currentExchangeRate.date, comparisonDate);
    return (
      <Card
        outlineColor={color["gray"][200]}
        title={headline}
        changeDisplay="N/A"
        subtext="No data available"
      />
    );
  }

  const { rate: previousValue, date: previousDate } = previousExchangeRate;

  const headline = getHeadline(currentDate, previousDate);
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
      outlineColor={
        colorValue[backgroundColorShade] ?? colorValue["500"] ?? "#FFFFFF"
      }
      title={headline}
      changeDisplay={relativeChangeDisplay}
      subtext={subtext}
    />
  );
};
