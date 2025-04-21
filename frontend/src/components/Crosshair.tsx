import { Line } from "@visx/shape";

import chartStyle from "@/styles/charts";
import color from "@/styles/color";

interface CrosshairProps {
  left: number;
  top: number;
  xOffset?: number;
  yOffset?: number;
  width: number;
  height: number;
  strokeColor?: string;
  pointColor?: string;
}

export default function Crosshair({
  left,
  top,
  xOffset = 0,
  yOffset = 0,
  width,
  height,
  strokeColor = color.gray["800"],
  pointColor = chartStyle.colors.primary,
}: CrosshairProps) {
  return (
    <g>
      <Line
        from={{ x: left, y: yOffset }}
        to={{ x: left, y: height }}
        stroke={strokeColor}
        strokeWidth={1}
        strokeOpacity={0.7}
        pointerEvents="none"
        strokeDasharray="5,3"
      />
      <Line
        from={{ x: xOffset, y: top }}
        to={{ x: width, y: top }}
        stroke={strokeColor}
        strokeWidth={1}
        strokeOpacity={0.7}
        pointerEvents="none"
        strokeDasharray="5,3"
      />
      <circle
        cx={left}
        cy={top}
        r={6}
        fill={pointColor}
        stroke="white"
        strokeWidth={2}
        pointerEvents="none"
      />
    </g>
  );
}
