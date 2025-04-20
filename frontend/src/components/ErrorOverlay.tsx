import { CircleX } from "lucide-react";

import { Flex, Heading } from "@jszymanowski/breeze-primitives";

interface Props {
  message?: string;
}

export default function ErrorOverlay({ message }: Props) {
  return (
    <Flex align="center" justify="center" className="h-full w-full">
      <Flex direction="col" justify="center">
        <div className="mx-auto my-12">
          <CircleX className="text-info" size={128} />
        </div>
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
