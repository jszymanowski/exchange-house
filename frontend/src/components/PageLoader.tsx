import { CircleDollarSign } from "lucide-react";

import { PageLoader as PageLoaderBase } from "@still-forest/canopy";

interface Props {
  message?: string;
}

const IconComponent = () => (
  <CircleDollarSign size={128} className="text-info animate-bounce" />
);

export default function PageLoader({ message }: Props) {
  return <PageLoaderBase message={message} iconComponent={IconComponent} />;
}
