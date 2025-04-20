import { CircleDollarSign } from "lucide-react";

import { Flex, Heading } from "@jszymanowski/breeze-primitives";

interface Props {
  message?: string;
}

export default function PageLoader({ message }: Props) {
  return (
    <Flex align="center" justify="center" className="h-full w-full">
      <Flex direction="col" justify="center">
        <Flex align="center" justify="center" gapX="4" className="my-6">
          <CircleDollarSign size="128" className="text-info animate-bounce" />
        </Flex>
        <Flex direction="col" justify="center" className="max-w-[500px]">
          {message ? (
            <Heading level="4" align="center" weight="normal">
              {message}
            </Heading>
          ) : null}
        </Flex>
      </Flex>
    </Flex>
  );
}
