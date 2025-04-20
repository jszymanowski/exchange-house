import { Box, type BoxProps } from "@jszymanowski/breeze-primitives";

import { cn } from "@/lib/utils";

interface Props extends BoxProps {
  children: React.ReactNode;
  className?: string;
}

export default function Container({ children, className, ...props }: Props) {
  return (
    <Box
      width="full"
      className={cn("align-left max-w-6xl p-12 pt-0", className)}
      {...props}
    >
      {children}
    </Box>
  );
}
