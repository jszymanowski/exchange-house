import { PageLoader as PageLoaderBase } from "@still-forest/canopy";
import { CircleDollarSign } from "lucide-react";

interface Props {
  message?: string;
}

const IconComponent = () => <CircleDollarSign size={128} className="animate-bounce text-info" />;

export default function PageLoader({ message }: Props) {
  return <PageLoaderBase message={message} iconComponent={IconComponent} />;
}
