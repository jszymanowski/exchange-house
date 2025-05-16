import ExchangeRateScreen from "@/components/ExchangeRateScreen";
import { useCurrencySubscription } from "@/hooks/useCurrencySubscription";

interface Props {
  currencyIndex: number;
}

export default function CurrencyScreen({ currencyIndex }: Props) {
  const currencies = useCurrencySubscription();
  const currencyCode = currencies[currencyIndex];

  return <ExchangeRateScreen currencyCode={currencyCode} />;
}
