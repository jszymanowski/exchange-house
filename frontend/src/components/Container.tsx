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
      className={cn("max-w-6xl p-4 pt-0 text-left md:p-8 lg:p-12", className)}
      {...props}
    >
      {children}
    </Box>
  );
}
